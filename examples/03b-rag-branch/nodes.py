import re

from langchain_core.messages import HumanMessage, SystemMessage

from .llm import get_llm, get_router_llm
from .state import Route, State

# 1) Router (normal chat vs RAG)


def router_node(state: State) -> dict:
    """
    Decide whether this query needs retrieval.

    Reads
    -----
    - state["user_query"]

    Writes
    ------
    - state["route"]
    """

    llm = get_router_llm()
    # Prompt template (role + task + constraints + few-shot)
    router_prompt = f"""
Role:
You are a routing classifier for a chat assistant.

Task:
Choose the single best route for the user query.

Routes:
- normal_chat: general help, no docs needed
- rag_chat: needs docs/policy/knowledge-base lookup

Output constraints:
- Output EXACTLY one token: normal_chat OR rag_chat
- Do not answer the user.

Examples:
User: "How long does shipping take according to the policy?"
Route: rag_chat

User: "Help me rewrite this paragraph."
Route: normal_chat
""".strip()
    messages = [
        SystemMessage(content=router_prompt),
        HumanMessage(content=state["user_query"]),
    ]
    route = llm.invoke(messages).content.strip()
    if route not in ("normal_chat", "rag_chat"):
        route = "normal_chat"

    return {"route": route}


def pick_route(state: State) -> Route:
    """Return the route label for `add_conditional_edges`."""

    return state["route"] or "normal_chat"


# 2) Retrieval (toy stub)

KNOWLEDGE_BASE = [
    "Refund policy: refunds are available within 30 days of purchase.",
    "Shipping policy: standard shipping takes 3-5 business days.",
    "Support policy: include your order ID for faster support.",
]


def retrieve_node(state: State) -> dict:
    """
    Retrieve relevant docs.

    This is a simple keyword-overlap retriever so the example stays readable.
    Replace this with your real vector search.

    Writes
    ------
    - state["docs"]
    """

    query_words = _words(state["user_query"])
    scored = []
    for doc in KNOWLEDGE_BASE:
        overlap = len(query_words & _words(doc))
        scored.append((overlap, doc))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    docs = [doc for score, doc in scored if score > 0][:2]
    return {"docs": docs}


def synthesize_node(state: State) -> dict:
    """
    Synthesize retrieved docs into a short notes block.

    Writes
    ------
    - state["notes"]
    """

    docs = state.get("docs") or []
    notes = "\n".join(f"- {doc}" for doc in docs) if docs else ""
    return {"notes": notes}


# 3) Drafting


def normal_chat_node(state: State) -> dict:
    """Answer directly without retrieval."""

    llm = get_llm()
    response = llm.invoke([HumanMessage(content=state["user_query"])])
    return {"answer": response.content}


def draft_answer_node(state: State) -> dict:
    """Answer using retrieved notes."""

    llm = get_llm()
    notes = state.get("notes") or ""
    # Prompt template (role + task + context + constraints)
    system_prompt = f"""
Role:
You answer user questions using a small docs notes block.

Task:
Answer the user. Use the notes when relevant.

Constraints:
- If the notes do not contain the needed info, say what is missing and ask ONE clarifying question.
- Be concise.

Docs notes:
{notes}
""".strip()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["user_query"]),
    ]
    response = llm.invoke(messages)
    return {"answer": response.content}


def _words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) >= 3}
