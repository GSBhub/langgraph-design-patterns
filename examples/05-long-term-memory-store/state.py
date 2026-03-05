from dataclasses import dataclass
from typing import Literal, Optional, TypedDict

Intent = Literal["remember", "answer"]


@dataclass
class Context:
    """Runtime context provided by the caller (not stored in state)."""

    user_id: str


class State(TypedDict):
    """
    State for long-term memory with a store.

    Keys
    ----
    user_query:
        Raw user input.
    intent:
        "remember" or "answer".
    fact_text:
        The fact we want to store (only for remember intent).
    recalled_facts:
        Short list of facts recalled from the store (only for answer intent).
    answer:
        Final response.
    """

    user_query: str
    intent: Optional[Intent]
    fact_text: Optional[str]
    recalled_facts: Optional[list[str]]
    answer: Optional[str]
