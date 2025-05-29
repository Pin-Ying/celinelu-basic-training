from fastapi import Form
from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import datetime


# --- Crawl ---
class CommentCrawl(BaseModel):
    user: str
    content: str
    created_at: str

    class Config:
        orm_mode = True


class PostCrawl(BaseModel):
    title: str
    content: str
    author: str
    board_id: int
    created_at: datetime
    comments: List[CommentCrawl]

    class Config:
        orm_mode = True


# --- API ---
class UserSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class BoardSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CommentSchema(BaseModel):
    user: Optional['UserSchema'] = None
    content: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[datetime] = None
    author: Optional['UserSchema'] = None
    board: Optional['BoardSchema'] = None

    class Config:
        orm_mode = True


class PostDetailSchema(PostSchema):
    comments: Optional['List[CommentSchema]'] = None


class PostSearch(BaseModel):
    author: Optional[UserSchema] = None
    board: Optional[BoardSchema] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None

    class Config:
        orm_mode = True


class PostSchemaResponse(BaseModel):
    result: str = ''
    data: Optional[Union[PostSchema, PostDetailSchema, List[PostSchema]]] = None

    class Config:
        orm_mode = True


class StatisticsResponse(PostSchemaResponse):
    search_filter: Optional[PostSearch]
    result_count: int


#  --- Form Data ---
class PostFormData(BaseModel):
    title: str
    content: str
    author_name: str
    board_name: str

    @classmethod
    def as_form(
            cls,
            title: str = Form(...),
            content: str = Form(...),
            author_name: str = Form(...),
            board_name: str = Form(...)
    ):
        return cls(title=title, content=content, author_name=author_name, board_name=board_name)
