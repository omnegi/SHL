from fastapi import APIRouter

from app.graph import graph

from app.schemas import (
    ChatRequest,
    ChatResponse,
)

router = APIRouter()


@router.get("/health")
def health():

    return {
        "status": "ok"
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    result = graph.invoke(
        {
            "messages": request.messages,
            "query": "",
            "docs": [],
            "reply": "",
            "recommendations": [],
            "clarification_needed": False,
            "comparison": False,
            "off_topic": False,
            "end_of_conversation": False,
        }
    )

    return ChatResponse(
        reply=result["reply"],
        recommendations=result["recommendations"],
        end_of_conversation=result["end_of_conversation"],
    )