from typing import Optional, TypedDict


class State(TypedDict):
    """
    State for a simple tool-then-answer workflow.

    Keys
    ----
    user_query:
        Raw user input.
    order_id:
        Extracted order ID (or None if not present).
    order_info:
        Tool output (or None if tool not called).
    answer:
        Final response.
    """

    user_query: str
    order_id: Optional[str]
    order_info: Optional[str]
    answer: Optional[str]

