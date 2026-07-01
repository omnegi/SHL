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

Use ONLY the retrieved assessments.

Do NOT invent assessment names.

Do NOT invent URLs.

Explain briefly why the assessments fit.

If the last user message modifies the shortlist
(add/remove/replace),
update the recommendation accordingly.

Never mention assessments that are not retrieved.

Keep the response under 150 words.
"""

    response = llm.invoke(prompt)

    state["reply"] = response.content

    state["recommendations"] = recommendations

    state["end_of_conversation"] = True

    return state

print("RECOMMEND")