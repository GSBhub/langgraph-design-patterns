import os

from langchain_openai import ChatOpenAI


def get_router_llm():
    """
    Return a small/cheap model for routing.

    Beginner rule:
      Use a smaller model for routers than for drafting.
    """

    model = os.getenv("OPENAI_ROUTER_MODEL", os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    return ChatOpenAI(model=model, temperature=0)


def get_drafting_llm():
    """Return your main model for writing the final answer."""

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    return ChatOpenAI(model=model, temperature=0)

