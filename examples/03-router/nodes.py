import re

from langchain_core.messages import HumanMessage, SystemMessage

from .llm import get_drafting_llm, get_router_llm
from .state import Route, State

# 1) Deterministic checks (cheap, fast)

URL_RE = r"https?://\S+"
ESCALATION_KEYWORDS = [
    "talk to a human",
    "talk to an agent",
    "representative",
    "not happy",
    "complaint",
]


def precheck_node(state: State) -> dict:
    """
    Deterministic routing rules that do not require an LLM.

    Reads
    -----
    - state["user_query"]

    Writes (sometimes)
    ------------------
    - state["route"]
    - state["reason"]
    """

    query = state["user_query"].lower()

    if any(keyword in query for keyword in ESCALATION_KEYWORDS):
        return {"route": "escalate_human", "reason": "User asked for a human."}

    if re.search(URL_RE, query):
        return {"route": "url_tool_first", "reason": "URL detected; tool-first flow."}

    return {}


# 2) Router LLM (only when deterministic checks didn't decide)


def router_llm_node(state: State) -> dict:
    """
    Choose between normal chat vs RAG.

    Router rule:
      Prefer `normal_chat` unless retrieval is clearly required.
    """

    llm = get_router_llm()

    # Prompt template (role + task + constraints + few-shot)
    router_prompt = f"""
Role:
You are a routing classifier for a chat assistant.

Task:
Choose the single best route for the user query.

Routes:
- normal_chat: casual conversation or general advice
- rag_chat: needs a doc/policy/knowledge-base lookup

Output constraints:
- Output EXACTLY one token: normal_chat OR rag_chat
- Do not answer the user.

Examples:
User: "What is your refund policy according to the docs?"
Route: rag_chat

User: "Help me write a better subject line."
Route: normal_chat
""".strip()

    messages = [
        SystemMessage(content=router_prompt),
        HumanMessage(content=state["user_query"]),
    ]
    response = llm.invoke(messages)

    route = response.content.strip()
    if route not in ("normal_chat", "rag_chat"):
        route = "normal_chat"

    reason = "Doc-grounded question; retrieval likely needed." if route == "rag_chat" else "General conversation."
    return {"route": route, "reason": reason}


# 3) Route targets (keep these simple)


def normal_chat_node(state: State) -> dict:
    """Draft a normal chat answer."""

    llm = get_drafting_llm()
    response = llm.invoke([HumanMessage(content=state["user_query"])])
    return {"answer": response.content}


def rag_chat_node(state: State) -> dict:
    """
    Placeholder RAG path.

    In the capstone, this node becomes a small RAG pipeline.
    """

    llm = get_drafting_llm()
    system_prompt = """
Role:
You are a helpful assistant.

Task:
Answer the user. If you need missing context (docs/product/version), ask ONE clarifying question.

Constraints:
- Be concise.
""".strip()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["user_query"]),
    ]
    response = llm.invoke(messages)
    return {"answer": response.content}


def url_tool_first_node(state: State) -> dict:
    """Placeholder URL tool-first path."""

    llm = get_drafting_llm()
    system_prompt = """
Role:
You are a helpful assistant.

Task:
The user provided a URL. In a real app you would:
1) extract content with a URL tool
2) answer using the extracted content

Constraints:
- Be concise.
""".strip()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["user_query"]),
    ]
    response = llm.invoke(messages)
    return {"answer": response.content}


def escalate_human_node(state: State) -> dict:
    """Return a human handoff response."""

    return {
        "answer": (
            "I’m going to hand this off to a human support agent.\n\n"
            f"Reason: {state.get('reason') or 'Escalation requested.'}"
        )
    }


def pick_route(state: State) -> Route:
    """Return the route label for `add_conditional_edges`."""

    return state["route"] or "normal_chat"
