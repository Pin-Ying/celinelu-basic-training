from pydantic import BaseModel
from typing import List, Optional
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
class AuthorSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class BoardSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[datetime] = None
    author: Optional['AuthorSchema'] = None
    board: Optional['BoardSchema'] = None

    class Config:
        orm_mode = True


class PostSearch(BaseModel):
    author: Optional[AuthorSchema] = None
    board: Optional[BoardSchema] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None

    class Config:
        orm_mode = True
