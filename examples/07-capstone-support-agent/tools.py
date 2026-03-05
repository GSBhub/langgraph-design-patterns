from langchain_core.tools import tool


@tool
def lookup_order(order_id: str) -> str:
    """Toy order lookup tool (replace with your real API call)."""

    return f"Order {order_id}: status=SHIPPED, eta=2 days"

