from typing import Optional, TypedDict


class State(TypedDict):
    """
    The *state contract* for this example.

    LangGraph nodes read from this dict and return partial updates to it.

    Keys
    ----
    user_query:
        Raw user input.
    normalized_query:
        A cleaned version of the query used by downstream logic.
    answer:
        The final answer text.
    """

    user_query: str
    normalized_query: Optional[str]
    answer: Optional[str]

