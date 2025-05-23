from fastapi import APIRouter, FastAPI, Depends, Query
from typing import List, Optional
from datetime import datetime

from db.crud import get_post_filter_by, get_post_by_search_dic
from db.database import SessionLocal
from schema.ptt_content import PostSchema, PostInput, PostSearch, AuthorSchema, BoardSchema

app = FastAPI()
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def post_search_query(
        author_name: Optional[str] = Query(None),
        board_name: Optional[str] = Query(None),
        start_datetime: Optional[datetime] = Query(None),
        end_datetime: Optional[datetime] = Query(None),
) -> PostSearch:
    return PostSearch(
        author=AuthorSchema(name=author_name) if author_name else None,
        board=BoardSchema(name=board_name) if board_name else None,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
    )


@router.get("/api/posts", response_model=List[PostSchema])
async def get_all_posts(db=Depends(get_db), limit=50, offset=None):
    return get_post_filter_by(db, page_limit=limit, page_offset=offset)


@router.get("/api/posts/{id}", response_model=List[PostSchema])
async def get_post(db=Depends(get_db), id=None):
    the_post = get_post_filter_by(db, **{'id': id})
    return the_post


@router.get("/api/statistics", response_model=List[PostSchema])
async def get_statistics(search_filter: PostSearch = Depends(post_search_query), db=Depends(get_db)):
    return get_post_by_search_dic(search_filter)


@router.post("/api/posts", response_model=PostInput)
async def add_post(**post_input):
    pass


@router.put("/api/posts/{id}", response_model=List[PostSchema])
async def update_post(id):
    pass


@router.delete("/api/posts/{id}", response_model=List[PostSchema])
async def delete_post(id):
    pass
