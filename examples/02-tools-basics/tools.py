from langchain_core.tools import tool


@tool
def lookup_order(order_id: str) -> str:
    """
    Look up basic order information.

    This is a tiny “toy tool” so you can focus on the pattern.
    Replace this with your real database/API call.
    """

    return f"Order {order_id}: status=SHIPPED, eta=2 days"

