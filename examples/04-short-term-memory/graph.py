from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from .nodes import chat_node
from .state import State


def build_graph():
    """
    Build a graph with short-term memory enabled via a checkpointer.

    The checkpointer stores state per thread:
      config = {"configurable": {"thread_id": "<id>"}}
    """

    graph = StateGraph(State)
    graph.add_node("chat", chat_node)
    graph.add_edge(START, "chat")
    graph.add_edge("chat", END)

    checkpointer = InMemorySaver()
    return graph.compile(checkpointer=checkpointer)

