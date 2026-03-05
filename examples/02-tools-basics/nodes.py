import re

from langchain_core.messages import HumanMessage, SystemMessage

from .llm import get_llm
from .state import State
from .tools import lookup_order


def extract_order_id_node(state: State) -> dict:
    """
    Extract an order ID from the user query.

    Reads
    -----
    - state["user_query"]

    Writes
    ------
    - state["order_id"]
    """

    match = re.search(r"\b(\d{5,})\b", state["user_query"])
    return {"order_id": match.group(1) if match else None}


def call_tool_node(state: State) -> dict:
    """
    Call the tool and store its result.

    Reads
    -----
    - state["order_id"]

    Writes
    ------
    - state["order_info"]
    """

    order_id = state.get("order_id")
    if not order_id:
        return {"order_info": None}

    order_info = lookup_order.invoke({"order_id": order_id})
    return {"order_info": order_info}


def draft_answer_node(state: State) -> dict:
    """
    Draft the final answer using tool output when available.

    Reads
    -----
    - state["user_query"]
    - state["order_info"]

    Writes
    ------
    - state["answer"]
    """

    llm = get_llm()

    tool_context = state.get("order_info") or "No order info was available."
    # Prompt template (role + task + context + constraints)
    system_prompt = f"""
Role:
You are a customer support assistant.

Task:
Answer the user.

Constraints:
- Be concise.
- Use tool context when it is relevant.
- If tool context is missing but needed, ask ONE clarifying question.

Tool context:
{tool_context}
""".strip()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["user_query"]),
    ]
    response = llm.invoke(messages)

    return {"answer": response.content}
