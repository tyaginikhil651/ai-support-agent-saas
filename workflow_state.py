from typing import TypedDict


class AgentState(TypedDict):

    user_id: str

    intent: str

    service: str

    date: str

    time: str

    issue: str

    response: str

    message: str

    complaint: str