import json
import re

from app.services.llm import llm
from app.schemas import Recommendation


def rank(state):

    docs = state["docs"]

    catalog = []

    for i, doc in enumerate(docs):

        catalog.append(
            {
                "id": i,
                "name": doc.metadata["name"],
                "url": doc.metadata["url"],
                "type": doc.metadata["test_type"],
                "description": doc.page_content[:500],
            }
        )

    prompt = f"""
You are selecting SHL assessments.

User request:

{state['query']}

Candidate assessments:

{json.dumps(catalog, indent=2)}

Return ONLY a JSON array of assessment ids.

Example:

[1,4,7]

Return between 1 and 7 ids.
"""

    response = llm.invoke(prompt).content

    match = re.search(r"\[[^\]]*\]", response)

    ids = []

    if match:
        try:
            ids = json.loads(match.group())
        except Exception:
            ids = list(range(min(5, len(docs))))
    else:
        ids = list(range(min(5, len(docs))))

    recommendations = []

    ranked_docs = []

    for idx in ids:

        if idx >= len(docs):
            continue

        doc = docs[idx]

        ranked_docs.append(doc)

        recommendations.append(
            Recommendation(
                name=doc.metadata["name"],
                url=doc.metadata["url"],
                test_type=doc.metadata["test_type"],
            )
        )

    state["docs"] = ranked_docs
    state["recommendations"] = recommendations

    return state

print("RANK")