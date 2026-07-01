from app.services.llm import llm


def clarify(state):

    history = ""

    for m in state["messages"]:
        history += f"{m.role}: {m.content}\n"

    prompt = f"""
You are an SHL Assessment Recommendation Assistant.

The user has not provided enough information.

Conversation:

{history}

Ask ONE concise clarification question.

The question should help recommend SHL assessments.

Examples:
- role
- seniority
- language
- hiring vs development
- technical vs leadership
- personality requirements

Only ask ONE question.
"""

    response = llm.invoke(prompt)

    state["reply"] = response.content
    state["recommendations"] = []
    state["end_of_conversation"] = False

    return state