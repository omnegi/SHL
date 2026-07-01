def refuse(state):

    state["reply"] = (
        "I can help recommend and compare SHL assessments, "
        "but I can't provide legal, regulatory, or unrelated advice."
    )

    state["recommendations"] = []

    state["end_of_conversation"] = False

    return state