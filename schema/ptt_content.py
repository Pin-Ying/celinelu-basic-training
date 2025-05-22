from pydantic import BaseModel
from typing import List
from datetime import datetime


class CommentInput(BaseModel):
    user: str
    content: str
    created_at: str

    class Config:
        orm_mode = True


class PostInput(BaseModel):
    title: str
    content: str
    author: str
    board_id: int
    created_at: datetime
    comments: List[CommentInput]

    class Config:
        orm_mode = True


class AuthorSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class BoardSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author: AuthorSchema
    board: BoardSchema

    class Config:
        orm_mode = True
