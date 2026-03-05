from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from langgraph.store.base import BaseStore

from .llm import get_llm
from .state import Context, State


def classify_intent_node(state: State) -> dict:
    """
    Very small intent classifier for this example.

    Rule
    ----
    If the query starts with "remember:", we store a fact.
    Otherwise, we answer and optionally recall facts.
    """

    query = state["user_query"].strip()
    if query.lower().startswith("remember:"):
        return {"intent": "remember", "fact_text": query.split(":", 1)[1].strip()}
    return {"intent": "answer", "fact_text": None}


def save_fact_node(state: State, runtime: Runtime[Context]) -> dict:
    """
    Save a fact into the store.

    Reads
    -----
    - state["fact_text"]
    - runtime.context["user_id"]

    Writes
    ------
    - (no state keys required; side effect is the store write)
    """

    store: BaseStore = runtime.store
    user_id = runtime.context.user_id

    namespace = ("user_facts", user_id)
    key = f"fact:{abs(hash(state.get('fact_text') or ''))}"
    store.put(namespace, key, {"text": state.get("fact_text") or ""})

    return {}


def confirm_node(state: State) -> dict:
    """Confirm that the fact was stored."""

    fact_text = state.get("fact_text") or ""
    return {"answer": f"Got it — I’ll remember: {fact_text}"}


def recall_facts_node(state: State, runtime: Runtime[Context]) -> dict:
    """
    Recall facts from the store.

    Reads
    -----
    - state["user_query"]
    - runtime.context["user_id"]

    Writes
    ------
    - state["recalled_facts"]
    """

    store: BaseStore = runtime.store
    user_id = runtime.context.user_id
    namespace = ("user_facts", user_id)

    items = store.search(namespace, query=state["user_query"], limit=3)
    recalled_facts = [item.value.get("text", "") for item in items]

    return {"recalled_facts": recalled_facts}


def answer_node(state: State) -> dict:
    """Answer using recalled facts when available."""

    llm = get_llm()

    recalled = state.get("recalled_facts") or []
    facts_block = "\n".join(f"- {f}" for f in recalled) or "- (no facts found)"

    system_prompt = f"""
Role:
You are a helpful assistant.

Task:
Answer the user.

Constraints:
- Use user facts when they are relevant.
- If facts are empty or not relevant, answer normally.

User facts (may be empty):
{facts_block}
""".strip()
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=state["user_query"])]
    response = llm.invoke(messages)
    return {"answer": response.content}
