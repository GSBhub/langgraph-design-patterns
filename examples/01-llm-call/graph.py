from langgraph.graph import END, START, StateGraph

from .nodes import answer_with_llm_node
from .state import State


def build_graph():
    """Return a compiled LangGraph app for this example."""

    graph = StateGraph(State)

    graph.add_node("answer_with_llm", answer_with_llm_node)
    graph.add_edge(START, "answer_with_llm")
    graph.add_edge("answer_with_llm", END)

    return graph.compile()

