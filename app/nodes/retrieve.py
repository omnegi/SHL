from app.services.retriever import search_assessments


def retrieve(state):

    query = "\n".join(
        f"{m.role}: {m.content}"
        for m in state["messages"]
    )

    docs = search_assessments(query, k=20)

    state["docs"] = docs

    return state