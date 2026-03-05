from langgraph.graph import END, START, StateGraph

from .nodes import (
    draft_answer_node,
    normal_chat_node,
    pick_route,
    retrieve_node,
    router_node,
    synthesize_node,
)
from .state import State


def build_graph():
    """
    Build a minimal RAG branch:
    - route first
    - retrieve only for `rag_chat`
    - draft using docs
    """

    graph = StateGraph(State)

    # 1) Nodes
    graph.add_node("router", router_node)
    graph.add_node("normal_chat", normal_chat_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("synthesize", synthesize_node)
    graph.add_node("draft_answer", draft_answer_node)

    # 2) Edges
    graph.add_edge(START, "router")
    graph.add_conditional_edges("router", pick_route, {"normal_chat": "normal_chat", "rag_chat": "retrieve"})

    graph.add_edge("normal_chat", END)

    graph.add_edge("retrieve", "synthesize")
    graph.add_edge("synthesize", "draft_answer")
    graph.add_edge("draft_answer", END)

    return graph.compile()

