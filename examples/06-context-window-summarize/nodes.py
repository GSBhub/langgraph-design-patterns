from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from .llm import get_llm
from .state import State

# 1) Context window rules (keep these as small constants)

MAX_MESSAGES = 8
KEEP_LAST = 6


def maybe_summarize_node(state: State) -> dict:
    """
    If the conversation is getting long, summarize older messages.

    Reads
    -----
    - state["messages"]
    - state.get("summary")

    Writes
    ------
    - state["summary"]
    - state["messages"] (trimmed window)
    """

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
You summarize conversations.

Task:
Summarize the conversation so far in 3–6 bullet points.

Constraints:
- Keep names, preferences, goals, and decisions.
- Do not include filler or quotes.

Prior summary (may be empty):
{prior_summary}

Older messages to summarize:
{chr(10).join(f"- {m.type}: {getattr(m, 'content', '')}" for m in older)}
""".strip()
    summary = llm.invoke([HumanMessage(content=prompt)]).content

    return {"summary": summary, "messages": recent}


def chat_node(state: State) -> dict:
    """
    Chat using the rolling summary + recent messages.

    Reads
    -----
    - state["summary"]
    - state["messages"]

    Writes
    ------
    - state["messages"] (appends an AI message)
    """

    llm = get_llm()
    summary = state.get("summary") or ""

    messages = []
    if summary:
        system_prompt = f"""
Role:
You are a helpful assistant.

Context:
Conversation summary so far:
{summary}
""".strip()
        messages.append(SystemMessage(content=system_prompt))

    messages.extend(state.get("messages", []))
    response = llm.invoke(messages)

    new_messages = list(state.get("messages", [])) + [AIMessage(content=response.content)]
    return {"messages": new_messages}
