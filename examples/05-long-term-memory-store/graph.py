from langgraph.graph import END, START, StateGraph
from langgraph.store.memory import InMemoryStore

from .nodes import (
    answer_node,
    classify_intent_node,
    confirm_node,
    recall_facts_node,
    save_fact_node,
)
from .state import Context, State


def build_graph():
    """Build a graph that reads/writes long-term memory via a store."""

    graph = StateGraph(State, context_schema=Context)

    graph.add_node("classify_intent", classify_intent_node)
    graph.add_node("save_fact", save_fact_node)
    graph.add_node("confirm", confirm_node)
    graph.add_node("recall_facts", recall_facts_node)
    graph.add_node("answer", answer_node)

    graph.add_edge(START, "classify_intent")

    def intent_to_next(state: State) -> str:
        return "save_fact" if state.get("intent") == "remember" else "recall_facts"

    graph.add_conditional_edges("classify_intent", intent_to_next, ["save_fact", "recall_facts"])
    graph.add_edge("save_fact", "confirm")
    graph.add_edge("confirm", END)

    graph.add_edge("recall_facts", "answer")
    graph.add_edge("answer", END)

    store = InMemoryStore()
    return graph.compile(store=store)
