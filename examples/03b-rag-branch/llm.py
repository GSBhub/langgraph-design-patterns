import os

from langchain_openai import ChatOpenAI


def get_router_llm():
    """Small/cheap model for routing."""

    model = os.getenv("OPENAI_ROUTER_MODEL", os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    return ChatOpenAI(model=model, temperature=0)


def get_llm():
    """Main model for drafting."""

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    return ChatOpenAI(model=model, temperature=0)

