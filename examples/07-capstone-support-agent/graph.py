from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.store.memory import InMemoryStore

from .nodes import (
    draft_answer_node,
    escalate_human_node,
    maybe_summarize_node,
    normal_chat_node,
    pick_route,
    precheck_node,
    recall_facts_node,
    router_llm_node,
    tool_order_lookup_node,
)
from .state import Context, State


def build_graph():
    """
    Compile the capstone graph with:
    - short-term memory (checkpointer)
    - long-term memory (store)
    """

    graph = StateGraph(State, context_schema=Context)

    # 1) Nodes
    graph.add_node("precheck", precheck_node)
    graph.add_node("router_llm", router_llm_node)

    graph.add_node("normal_chat", normal_chat_node)
    graph.add_node("tool_order_lookup", tool_order_lookup_node)
    graph.add_node("escalate_human", escalate_human_node)

    graph.add_node("maybe_summarize", maybe_summarize_node)
    graph.add_node("recall_facts", recall_facts_node)
    graph.add_node("draft_answer", draft_answer_node)

    # 2) Edges
    graph.add_edge(START, "precheck")

    def precheck_decision(state: State) -> str:
        return pick_route(state) if state.get("route") else "router_llm"

    graph.add_conditional_edges(
        "precheck",
        precheck_decision,
        ["router_llm", "normal_chat", "tool_order_lookup", "escalate_human"],
    )
    graph.add_conditional_edges("router_llm", pick_route, ["normal_chat", "escalate_human"])

    # Route → pipeline
    graph.add_edge("normal_chat", "maybe_summarize")
    graph.add_edge("tool_order_lookup", "maybe_summarize")

    graph.add_edge("maybe_summarize", "recall_facts")
    graph.add_edge("recall_facts", "draft_answer")
    graph.add_edge("draft_answer", END)

    # Escalation ends early
    graph.add_edge("escalate_human", END)

    checkpointer = InMemorySaver()
    store = InMemoryStore()
    return graph.compile(checkpointer=checkpointer, store=store)
