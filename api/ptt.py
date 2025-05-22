from fastapi import APIRouter, FastAPI
from fastapi import Depends
from typing import List

from db.crud import get_post_filter_by
from db.database import SessionLocal
from schema.ptt_content import PostSchema, PostInput, PostSearch

app = FastAPI()
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/api/posts", response_model=List[PostSchema])
async def get_all_posts(db=Depends(get_db), limit=50, offset=None):
    return get_post_filter_by(db, page_limit=limit, page_offset=offset)


@router.get("/api/posts/{id}", response_model=List[PostSchema])
async def get_post(db=Depends(get_db), id=None):
    the_post = get_post_filter_by(db, **{'id':id})
    return the_post


@router.get("/api/statistics", response_model=List[PostSchema])
async def get_statistics(db=Depends(get_db), **search_filter):
    PostSearch(**search_filter)

    return


@router.post("/api/posts", response_model=PostInput)
async def add_post(**post_input):


    pass


@router.put("/api/posts/{id}", response_model=List[PostSchema])
async def update_post(id):
    pass


@router.delete("/api/posts/{id}", response_model=List[PostSchema])
async def delete_post(id):
    pass
