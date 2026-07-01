from app.services.llm import llm
from app.prompts import SYSTEM_PROMPT
from app.schemas import Recommendation


def recommend(state):

    docs = state["docs"]

    history = ""

    for m in state["messages"]:
        history += f"{m.role}: {m.content}\n"

    context = ""

    recommendations = []

    for doc in docs:

        context += f"""
Assessment Name:
{doc.metadata["name"]}

Description:
{doc.page_content}

URL:
{doc.metadata["url"]}

Category:
{doc.metadata["test_type"]}

--------------------------------
"""

        recommendations.append(
            Recommendation(
                name=doc.metadata["name"],
                url=doc.metadata["url"],
                test_type=doc.metadata["test_type"],
            )
        )

    prompt = f"""
{SYSTEM_PROMPT}

Conversation:

{history}

Retrieved SHL Assessments:

{context}

Instructions:

You are an SHL assessment recommendation assistant.

Use ONLY the retrieved assessments.

Never invent assessment names.

Never invent URLs.

Recommend the 3–5 most relevant assessments.

Briefly explain why each assessment matches the user's requirements.

IMPORTANT:

- If the user has already provided enough information
  (role, skills, technologies, seniority, etc.),
  DO NOT ask any clarification questions.

- If the retrieved assessments sufficiently match the request,
  simply recommend them.

- Only ask a clarification question if the user's request is too vague
  to recommend any assessment.

- If the user modifies the shortlist (add/remove/replace),
  update the recommendations accordingly.

Return only the final answer.

Keep the response under 150 words.
"""

    response = llm.invoke(prompt)

    state["reply"] = response.content

    state["recommendations"] = recommendations

    reply = response.content.lower()

    needs_followup = any(
        phrase in reply
        for phrase in [
            "could you",
            "can you",
            "please specify",
            "clarify",
            "which one",
            "what kind",
        ]
    )

    state["end_of_conversation"] = not needs_followup

    return state

print("RECOMMEND")