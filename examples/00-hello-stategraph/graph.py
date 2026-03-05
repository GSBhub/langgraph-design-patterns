"""
Graph wiring for: 00 — Hello StateGraph.

This is intentionally tiny so you can see the exact LangGraph shape:
- define a State
- add nodes
- connect edges
- compile()
"""

from langgraph.graph import END, START, StateGraph

from .nodes import draft_answer_node, normalize_query_node
from .state import State


def build_graph():
    """Return a compiled LangGraph app for this example."""

    graph = StateGraph(State)

    # 1) Nodes
    graph.add_node("normalize_query", normalize_query_node)
    graph.add_node("draft_answer", draft_answer_node)

    # 2) Edges
    graph.add_edge(START, "normalize_query")
    graph.add_edge("normalize_query", "draft_answer")
    graph.add_edge("draft_answer", END)

    # 3) Compile
    return graph.compile()

