from typing import List, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str
    content: str


class Context(BaseModel):
    name: str
    description: Optional[str] = None
    user: str = 'Default'
    messages: List[Message] = []
