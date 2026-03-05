from langgraph.graph import END, START, StateGraph

from .nodes import chat_node, maybe_summarize_node
from .state import State


def build_graph():
    """Build a graph that summarizes when context grows."""

    graph = StateGraph(State)

    graph.add_node("maybe_summarize", maybe_summarize_node)
    graph.add_node("chat", chat_node)

    graph.add_edge(START, "maybe_summarize")
    graph.add_edge("maybe_summarize", "chat")
    graph.add_edge("chat", END)

    return graph.compile()

