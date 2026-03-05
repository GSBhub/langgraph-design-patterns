from langgraph.graph import END, START, StateGraph

from .nodes import call_tool_node, draft_answer_node, extract_order_id_node
from .state import State


def build_graph():
    """
    A minimal “tool gating” graph:
    - extract an order ID
    - call the tool only when the ID exists
    - draft the answer
    """

    graph = StateGraph(State)

    # 1) Nodes
    graph.add_node("extract_order_id", extract_order_id_node)
    graph.add_node("call_tool", call_tool_node)
    graph.add_node("draft_answer", draft_answer_node)

    # 2) Edges
    graph.add_edge(START, "extract_order_id")

    def needs_tool(state: State) -> str:
        return "call_tool" if state.get("order_id") else "draft_answer"

    graph.add_conditional_edges("extract_order_id", needs_tool, ["call_tool", "draft_answer"])
    graph.add_edge("call_tool", "draft_answer")
    graph.add_edge("draft_answer", END)

    return graph.compile()

