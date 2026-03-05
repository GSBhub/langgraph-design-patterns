from dataclasses import dataclass
from typing import Literal, Optional, TypedDict

from langchain_core.messages import BaseMessage

Route = Literal["normal_chat", "tool_order_lookup", "escalate_human"]


@dataclass
class Context:
    """Runtime context provided by the caller (not stored in state)."""

    user_id: str


class State(TypedDict):
    """
    Capstone state contract.

    Keep the contract boring:
      a few stable keys that every node agrees on.
    """

    # Conversation
    messages: list[BaseMessage]
    summary: Optional[str]

    # Routing
    route: Optional[Route]
    reason: Optional[str]

    # Tools
    order_id: Optional[str]
    order_info: Optional[str]

    # Long-term memory (facts)
    recalled_facts: Optional[list[str]]

    # Output
    answer: Optional[str]
