from .state import State


def normalize_query_node(state: State) -> dict:
    """
    Normalize the query so later nodes can stay simple.

    Reads
    -----
    - state["user_query"]

    Writes
    ------
    - state["normalized_query"]
    """

    normalized_query = state["user_query"].strip().lower()
    return {"normalized_query": normalized_query}


def draft_answer_node(state: State) -> dict:
    """
    Draft the final answer.

    Reads
    -----
    - state["normalized_query"]

    Writes
    ------
    - state["answer"]
    """

    normalized_query = state.get("normalized_query") or state["user_query"]
    return {"answer": f"You said: {normalized_query}"}

