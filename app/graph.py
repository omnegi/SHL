from langgraph.graph import StateGraph, END

from app.services import llm
from app.state import AgentState

from app.nodes.router import router
from app.nodes.clarify import clarify
from app.nodes.compare import compare
from app.nodes.refuse import refuse
from app.nodes.retrieve import retrieve
from app.nodes.recommend import recommend
from app.nodes.rank import rank


workflow = StateGraph(AgentState)

# Nodes
workflow.add_node("router", router)
workflow.add_node("clarify", clarify)
workflow.add_node("compare", compare)
workflow.add_node("refuse", refuse)
workflow.add_node("retrieve", retrieve)
workflow.add_node("recommend", recommend)
workflow.add_node("rank", rank)

workflow.set_entry_point("router")


def route(state):

    prompt = f"""
Classify this user message.

Return ONLY ONE WORD.

clarify
recommend
compare
refuse

Message:

{state["query"]}
"""

    decision = llm.invoke(prompt).content.strip().lower()

    if "clarify" in decision:
        return "clarify"

    if "compare" in decision:
        return "compare"

    if "refuse" in decision:
        return "refuse"

    return "retrieve"


workflow.add_conditional_edges(
    "router",
    route,
    {
        "clarify": "clarify",
        "compare": "compare",
        "refuse": "refuse",
        "retrieve": "retrieve",
    },
)

workflow.add_edge("retrieve", "rank")
workflow.add_edge("rank", "recommend")


workflow.add_edge("clarify", END)
workflow.add_edge("compare", END)
workflow.add_edge("refuse", END)
workflow.add_edge("recommend", END)

graph = workflow.compile()