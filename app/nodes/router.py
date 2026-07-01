from app.services.llm import llm


def router(state):

    query = state["messages"][-1].content

    state["query"] = query

    prompt = f"""
You are classifying a user request.

Return ONLY one word.

clarify
recommend
compare
refuse

Rules:

clarify
- insufficient information

recommend
- recommend assessments

compare
- compare assessments

refuse
- legal, medical, political, HR policy,
salary advice or unrelated questions

User:

{query}
"""

    decision = llm.invoke(prompt).content.strip().lower()

    state["clarification_needed"] = decision == "clarify"
    state["comparison"] = decision == "compare"
    state["off_topic"] = decision == "refuse"

    return state