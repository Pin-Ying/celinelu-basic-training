from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel


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
    comments: Optional[List[CommentCrawl]]

    class Config:
        orm_mode = True


# --- API ---
class UserSchema(BaseModel):
    name: Optional[str] = None

    class Config:
        orm_mode = True


class BoardSchema(BaseModel):
    name: Optional[str] = None

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


class StatisticsData(BaseModel):
    search_filter: Optional[PostSearch] = None
    total_count: int


class DataResponse(BaseModel):
    data: Optional[Union[PostSchema, PostDetailSchema, List[PostSchema], StatisticsData]] = None

    class Config:
        orm_mode = True
