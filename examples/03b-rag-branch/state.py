from typing import Literal, Optional, TypedDict

Route = Literal["normal_chat", "rag_chat"]


class State(TypedDict):
    """
    State for a minimal “RAG branch” workflow.

    Keys
    ----
    user_query:
        Raw user input.
    route:
        "normal_chat" or "rag_chat".
    docs:
        A small list of retrieved docs (strings).
    notes:
        A short synthesized context from docs.
    answer:
        Final response.
    """

    user_query: str
    route: Optional[Route]
    docs: Optional[list[str]]
    notes: Optional[str]
    answer: Optional[str]

