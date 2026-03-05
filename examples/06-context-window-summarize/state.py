from typing import Optional, TypedDict

from langchain_core.messages import BaseMessage


class State(TypedDict):
    """
    State for context-window management.

    Keys
    ----
    messages:
        The recent conversation window (you decide how big).
    summary:
        A compact “so far” summary of older conversation.
    """

    messages: list[BaseMessage]
    summary: Optional[str]

