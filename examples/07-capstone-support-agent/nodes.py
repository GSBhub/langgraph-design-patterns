import re

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from langgraph.store.base import BaseStore

from .llm import get_llm, get_router_llm
from .state import Context, Route, State
from .tools import lookup_order

# 1) Deterministic prechecks

ESCALATION_KEYWORDS = ["talk to a human", "representative", "not happy", "complaint"]


def precheck_node(state: State) -> dict:
    """
    Cheap checks that skip the router LLM.

    - Human escalation keywords
    - Order lookup trigger ("order" + a number)
    """

    last_user_text = _latest_user_text(state)
    lowered = last_user_text.lower()

    if any(keyword in lowered for keyword in ESCALATION_KEYWORDS):
        return {"route": "escalate_human", "reason": "User asked for a human."}

    order_id = _extract_order_id(lowered)
    if "order" in lowered and order_id:
        return {"route": "tool_order_lookup", "reason": "Order lookup requested.", "order_id": order_id}

    return {}


# 2) Router LLM (fallback)


def router_llm_node(state: State) -> dict:
    """
    Router fallback for everything else.

    For this capstone we keep routing small:
    - normal_chat
    - escalate_human
    """

    llm = get_router_llm()
    last_user_text = _latest_user_text(state)

    # Prompt template (role + task + constraints + few-shot)
    router_prompt = f"""
Role:
You are a routing classifier for a customer support assistant.

Task:
Choose the single best route for the user's latest message.

Routes:
- normal_chat: general help, questions, or guidance
- escalate_human: user is upset, explicitly wants a human, or the situation needs handoff

Output constraints:
- Output EXACTLY one token: normal_chat OR escalate_human
- Do not explain your choice.

Examples:
User: "I'm really frustrated. I want to talk to a human."
Route: escalate_human

User: "Can you help me rewrite this message?"
Route: normal_chat
""".strip()

    messages = [
        SystemMessage(content=router_prompt),
        HumanMessage(content=last_user_text),
    ]
    route = llm.invoke(messages).content.strip()
    if route not in ("normal_chat", "escalate_human"):
        route = "normal_chat"

    reason = "User seems to need a human handoff." if route == "escalate_human" else "General help."
    return {"route": route, "reason": reason}


def pick_route(state: State) -> Route:
    return state.get("route") or "normal_chat"


# 3) Route nodes (named exactly like routes)


def normal_chat_node(state: State) -> dict:
    """No-op route node for `normal_chat`."""

    return {}


def tool_order_lookup_node(state: State) -> dict:
    """Call the order lookup tool and store its output."""

    order_id = state.get("order_id")
    if not order_id:
        return {"order_info": None}

    order_info = lookup_order.invoke({"order_id": order_id})
    return {"order_info": order_info}


def escalate_human_node(state: State) -> dict:
    """Return a handoff response."""

    return {"answer": "I’m handing this off to a human agent."}


# 4) Context window (summary)

MAX_MESSAGES = 10
KEEP_LAST = 8


def maybe_summarize_node(state: State) -> dict:
    """Summarize older messages into `summary` and keep only the recent window."""

    messages = state.get("messages", [])
    if len(messages) <= MAX_MESSAGES:
        return {}

    older = messages[: -KEEP_LAST]
    recent = messages[-KEEP_LAST:]

    llm = get_llm()
    prior_summary = state.get("summary") or ""

    # Prompt template (role + task + constraints)
    prompt = f"""
Role:
You summarize support conversations.

Task:
Summarize the conversation so far in 3–6 bullet points.

Constraints:
- Keep only important details (names, preferences, goals, decisions).
- Be compact; no extra commentary.

Prior summary (may be empty):
{prior_summary}

Older messages to summarize:
{chr(10).join(f"- {m.type}: {getattr(m, 'content', '')}" for m in older)}
""".strip()
    summary = llm.invoke([HumanMessage(content=prompt)]).content
    return {"summary": summary, "messages": recent}


# 5) Long-term memory (facts store)


def recall_facts_node(state: State, runtime: Runtime[Context]) -> dict:
    """
    Recall user facts from the store.

    Requires runtime.context["user_id"] to be provided by the caller.
    """

    store: BaseStore = runtime.store
    user_id = runtime.context.user_id
    namespace = ("user_facts", user_id)

    last_user_text = _latest_user_text(state)
    items = store.search(namespace, query=last_user_text, limit=3)
    recalled_facts = [item.value.get("text", "") for item in items]

    return {"recalled_facts": recalled_facts}


# 6) Draft final answer


def draft_answer_node(state: State) -> dict:
    """
    Draft the final user response using:
    - summary (if present)
    - recalled facts (if any)
    - tool output (if any)
    """

    llm = get_llm()

    summary = state.get("summary") or ""
    recalled = state.get("recalled_facts") or []
    facts_block = "\n".join(f"- {f}" for f in recalled) or "- (none)"
    order_info = state.get("order_info") or ""

    # Prompt template (role + task + context + constraints)
    system_prompt = f"""
Role:
You are a helpful customer support assistant.

Task:
Reply to the user using the context provided below when it is relevant.

Constraints:
- Be concise.
- If information is missing, ask one clarifying question.

Context (summary):
{summary}

Context (user facts):
{facts_block}

Context (tool output):
{order_info}
""".strip()
    messages = [SystemMessage(content=system_prompt)] + state.get("messages", [])
    response = llm.invoke(messages)

    updated_messages = list(state.get("messages", [])) + [AIMessage(content=response.content)]
    return {"answer": response.content, "messages": updated_messages}


def _latest_user_text(state: State) -> str:
    for message in reversed(state.get("messages", [])):
        if getattr(message, "type", None) == "human":
            return getattr(message, "content", "")
    return ""


def _extract_order_id(text: str):
    match = re.search(r"\b(\d{5,})\b", text)
    return match.group(1) if match else None
