from fastapi import APIRouter, FastAPI, Depends, Query, Form, Body
from typing import List, Optional, Any, Coroutine
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import pytz

from db.crud import get_post_filter_by, get_post_by_search_dic, create_post, update_post_from_id, delete_post_from_id
from db.database import SessionLocal
from schema.ptt_content import PostSchema, PostSearch, AuthorSchema, BoardSchema, PostSchemaResponse

app = FastAPI()
router = APIRouter()
tz = pytz.timezone("Asia/Taipei")

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


def form_to_postschema(
        title: str = Form(...),
        content: str = Form(...),
        author_name: str = Form(...),
        board_name: str = Form(...),
        created_at: Optional[datetime] = Form(None)
):
    return PostSchema(
        title=title,
        content=content,
        author=AuthorSchema(name=author_name) if author_name else None,
        board=BoardSchema(name=board_name) if board_name else None,
        created_at=created_at if created_at else datetime.now(tz),
    )


def handle_create_post(db, post_data: PostSchema):
    return create_post(db, post_data)


# --- GET ---
@router.get("/api/posts", response_model=List[PostSchema])
async def get_all_posts(db=Depends(get_db), limit=50, offset=0):
    return get_post_filter_by(db, posts_limit=limit, posts_offset=offset)


@router.get("/api/posts/{post_id}", response_model=List[PostSchema])
async def get_post(db=Depends(get_db), post_id=None):
    the_post = get_post_filter_by(db, **{'id': post_id})
    return the_post


@router.get("/api/statistics", response_model=List[PostSchema])
async def get_statistics(search_filter: PostSearch = Depends(post_search_query),
                         db=Depends(get_db),
                         limit=50,
                         offset=0):
    return get_post_by_search_dic(db, search_filter, posts_limit=limit, posts_offset=offset)


# --- POST ---
@router.post("/api/posts", response_model=PostSchemaResponse)
async def add_post(post_add: PostSchema = Body(...), db=Depends(get_db)):
    return handle_create_post(db, post_add)


@router.post("/api/posts/form")
async def create_post_from_form(
        post_data: PostSchema = Depends(form_to_postschema), db=Depends(get_db)):
    return handle_create_post(db, post_data)


# --- PUT ---
@router.put("/api/posts/{post_id}", response_model=PostSchemaResponse)
async def update_post(post_id, db=Depends(get_db), post_update: PostSchema = Body(...)):
    return update_post_from_id(db, post_id, post_update)


@router.put("/api/posts/form/{post_id}", response_model=PostSchemaResponse)
async def update_post_from_form(post_id, db=Depends(get_db), post_update: PostSchema = Depends(form_to_postschema)):
    return update_post_from_id(db, post_id, post_update)


# --- DELETE ---
@router.delete("/api/posts/{post_id}", response_model=PostSchemaResponse)
async def delete_post(post_id, db=Depends(get_db)):
    return delete_post_from_id(db, post_id)
