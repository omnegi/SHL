COMPARE_WORDS = {"compare", "difference", "vs", "versus"}

OFFTOPIC_WORDS = {
    "salary",
    "visa",
    "tax",
    "weather",
    "politics",
}

ROLE_KEYWORDS = {
    "developer",
    "engineer",
    "analyst",
    "manager",
    "sales",
    "operator",
    "backend",
    "frontend",
}

TECH_KEYWORDS = {
    "java",
    "python",
    "spring",
    "spring boot",
    "sql",
    "aws",
    "docker",
    "react",
    "node",
    "javascript",
    "c++",
}


def router(state):
    query = state["messages"][-1].content.lower()

    state["query"] = query

    state["comparison"] = any(x in query for x in COMPARE_WORDS)
    state["off_topic"] = any(x in query for x in OFFTOPIC_WORDS)

    if state["comparison"] or state["off_topic"]:
        state["clarification_needed"] = False
        return state

    has_role = any(k in query for k in ROLE_KEYWORDS)
    has_skill = any(k in query for k in TECH_KEYWORDS)

    # Recommend if the user has given either a role or technical skills.
    state["clarification_needed"] = not (has_role or has_skill)

    return state

