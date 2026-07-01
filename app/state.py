from typing import TypedDict, List, Any
from app.schemas import Message, Recommendation


class AgentState(TypedDict):
    messages: List[Message]

    query: str

    docs: List[Any]

    reply: str

    recommendations: List[Recommendation]

    clarification_needed: bool

    comparison: bool

    off_topic: bool

    end_of_conversation: bool