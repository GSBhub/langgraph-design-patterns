"""
One place for your LLM configuration.

Beginner rule:
  If you need to change model/provider later, you should only touch this file.
"""

import os

from langchain_openai import ChatOpenAI


def get_llm():
    """
    Return a configured OpenAI chat model.

    Environment
    -----------
    - OPENAI_API_KEY: required by the OpenAI SDK
    - OPENAI_MODEL: optional (defaults to gpt-4.1-mini)
    """

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    return ChatOpenAI(model=model, temperature=0)

