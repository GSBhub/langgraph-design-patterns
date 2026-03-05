from typing import Optional, TypedDict


class State(TypedDict):
    """Minimal state for “one LLM call”."""

    user_query: str
    answer: Optional[str]

