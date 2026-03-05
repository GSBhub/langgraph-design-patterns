from langchain_core.messages import AIMessage

from .llm import get_llm
from .state import State


def chat_node(state: State) -> dict:
    """
    Respond to the conversation.

    Reads
    -----
    - state["messages"]

    Writes
    ------
    - state["messages"] (appends an AI message)
    """

    llm = get_llm()
    response = llm.invoke(state["messages"])
    return {"messages": [AIMessage(content=response.content)]}

