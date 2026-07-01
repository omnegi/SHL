def clarify(state):

    state["reply"] = (
        "Could you tell me the job role or position you are hiring for? "
        "For example: Java Developer, Sales Executive, Graduate Analyst, "
        "Customer Service Representative, etc."
    )

    state["recommendations"] = []

    state["end_of_conversation"] = False

    return state