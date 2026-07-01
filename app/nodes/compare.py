from app.services.retriever import search_assessments
from app.services.llm import llm


def compare(state):

    docs = search_assessments(
        state["query"],
        k=2
    )

    context = ""

    for d in docs:

        context += d.page_content
        context += "\n\n"

    prompt = f"""
Compare ONLY using the information below.

{context}

Question:

{state["query"]}
"""

    response = llm.invoke(prompt)

    state["reply"] = response.content

    state["recommendations"] = []

    state["end_of_conversation"] = False

    return state