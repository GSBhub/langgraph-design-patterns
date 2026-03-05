from langgraph.graph import END, START, StateGraph

from .nodes import (
    escalate_human_node,
    normal_chat_node,
    pick_route,
    precheck_node,
    rag_chat_node,
    router_llm_node,
    url_tool_first_node,
)
from .state import State


def build_graph():
    """Build and compile the router graph."""

    graph = StateGraph(State)

    # 1) Nodes
    graph.add_node("precheck", precheck_node)
    graph.add_node("router_llm", router_llm_node)
    graph.add_node("normal_chat", normal_chat_node)
    graph.add_node("rag_chat", rag_chat_node)
    graph.add_node("url_tool_first", url_tool_first_node)
    graph.add_node("escalate_human", escalate_human_node)

    # 2) Edges
    graph.add_edge(START, "precheck")

    def precheck_decision(state: State) -> str:
        return pick_route(state) if state.get("route") else "router_llm"

    graph.add_conditional_edges(
        "precheck",
        precheck_decision,
        ["router_llm", "normal_chat", "rag_chat", "url_tool_first", "escalate_human"],
    )
    graph.add_conditional_edges("router_llm", pick_route)

    graph.add_edge("normal_chat", END)
    graph.add_edge("rag_chat", END)
    graph.add_edge("url_tool_first", END)
    graph.add_edge("escalate_human", END)

    return graph.compile()

