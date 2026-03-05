import os

from langchain_openai import ChatOpenAI


def get_router_llm():
    model = os.getenv("OPENAI_ROUTER_MODEL", os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    return ChatOpenAI(model=model, temperature=0)


def get_llm():
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    return ChatOpenAI(model=model, temperature=0)

