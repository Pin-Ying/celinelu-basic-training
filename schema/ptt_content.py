from pydantic import BaseModel
from typing import List
from datetime import datetime

class CommentInput(BaseModel):
    user: str
    content: str
    created_at: str

class PostInput(BaseModel):
    title: str
    content: str
    author: str
    created_at: datetime
    comments: List[CommentInput]
