from app import state


COMPARE_WORDS = {
    "compare", "difference", "vs", "versus"
}

OFFTOPIC_WORDS = {
    "salary", "visa", "weather", "politics", "tax", "football"
}

ROLE_WORDS = {
    "developer",
    "engineer",
    "analyst",
    "manager",
    "sales",
    "operator",
    "java",
    "python",
    "backend",
    "frontend",
    "aws",
    "sql",
    "spring",
    "react",
    "node",
}

SENIORITY = {
    "intern",
    "entry",
    "junior",
    "mid",
    "senior",
    "lead",
    "principal",
}


def router(state):
    query = state["messages"][-1].content.lower()

    state["query"] = query
    state["comparison"] = False
    state["off_topic"] = False
    state["clarification_needed"] = False

    if any(word in query for word in COMPARE_WORDS):
        state["comparison"] = True
        return state

    if any(word in query for word in OFFTOPIC_WORDS):
        state["off_topic"] = True
        return state

    has_role = any(word in query for word in ROLE_WORDS)
    has_level = any(word in query for word in SENIORITY)

    # Only clarify when we truly don't know what the user wants
    if not has_role:
        state["clarification_needed"] = True

    return state

print("ROUTER")
print(state)