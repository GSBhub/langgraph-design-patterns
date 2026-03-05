from typing import Literal, Optional, TypedDict

Route = Literal["normal_chat", "rag_chat", "url_tool_first", "escalate_human"]


class State(TypedDict):
    """
    State for routing.

    Keys
    ----
    user_query:
        Raw user input.
    route:
        One of the Route labels, once decided.
    reason:
        One sentence explaining why this route was chosen.
    answer:
        The final response for the user.
    """

    user_query: str
    route: Optional[Route]
    reason: Optional[str]
    answer: Optional[str]

