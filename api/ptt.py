from fastapi import APIRouter, FastAPI, Depends, Query, Form, Body
from typing import List, Optional, Any, Coroutine
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from db.crud import get_post_filter_by, get_post_by_search_dic, create_post
from db.database import SessionLocal
from model.ptt_content import Post
from schema.ptt_content import PostSchema, PostSearch, AuthorSchema, BoardSchema, PostSchemaResponse

app = FastAPI()
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise e
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
async def get_all_posts(db=Depends(get_db), limit=50, offset=0):
    return get_post_filter_by(db, posts_limit=limit, posts_offset=offset)


@router.get("/api/posts/{id}", response_model=List[PostSchema])
async def get_post(db=Depends(get_db), id=None):
    the_post = get_post_filter_by(db, **{'id': id})
    return the_post


@router.get("/api/statistics", response_model=List[PostSchema])
async def get_statistics(search_filter: PostSearch = Depends(post_search_query),
                         db=Depends(get_db),
                         limit=50,
                         offset=0):
    return get_post_by_search_dic(db, search_filter, posts_limit=limit, posts_offset=offset)


@router.post("/api/posts", response_model=PostSchemaResponse)
async def add_post(post_add: PostSchema = Body(...), db=Depends(get_db)):
    data = create_post(db, post_add)
    if data is None:
        return PostSchemaResponse(result='Error')
    return PostSchemaResponse(result='success',data=data)


@router.post("/api/posts/form")
async def create_post_from_form(
        title: str = Form(...),
        content: str = Form(...),
        author_name: str = Form(...),
        board_name: str = Form(...),
        created_at: Optional[datetime] = datetime.now(),
        db=Depends(get_db)
):
    post_data = PostSchema(
        title=title,
        content=content,
        author=AuthorSchema(name=author_name) if author_name else None,
        board=BoardSchema(name=board_name) if board_name else None,
        created_at=created_at,
    )
    return await add_post(post_data, db)


@router.put("/api/posts/{id}", response_model=PostSchemaResponse)
async def update_post(id):
    pass


@router.delete("/api/posts/{id}", response_model=PostSchemaResponse)
async def delete_post(id):
    pass
