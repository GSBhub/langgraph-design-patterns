from langchain_core.messages import HumanMessage, SystemMessage

from .llm import get_llm
from .state import State


def answer_with_llm_node(state: State) -> dict:
    """
    Call the LLM and write the answer into state.

    Reads
    -----
    - state["user_query"]

    Writes
    ------
    - state["answer"]
    """

    llm = get_llm()

    system_prompt = """
Role:
You are a concise, helpful assistant.

Task:
Answer the user clearly and directly.
""".strip()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["user_query"]),
    ]
    response = llm.invoke(messages)

    return {"answer": response.content}
