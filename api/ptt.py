from datetime import datetime
from typing import Optional

import pytz
from fastapi import APIRouter, FastAPI, Depends, Form, Body
from sqlalchemy.exc import SQLAlchemyError

from db.crud import create_post, update_post_from_id, delete_post_from_id, \
    get_query_by_search_dic, get_post_detail_by_id, get_posts_by_search_dic
from db.database import SessionLocal
from schema.ptt_content import PostSchema, PostSearch, UserSchema, BoardSchema, PostSchemaResponse, StatisticsResponse

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


def empty_str_to_none(s: str):
    if s and s.strip() != "":
        return s
    return None


def post_search_query(
        author_name: Optional[str] = "",
        board_name: Optional[str] = "",
        start_datetime: Optional[str] = "",
        end_datetime: Optional[str] = "",
) -> PostSearch:
    return PostSearch(
        author=UserSchema(name=author_name) if empty_str_to_none(author_name) else None,
        board=BoardSchema(name=board_name) if empty_str_to_none(board_name) else None,
        start_datetime=datetime.fromisoformat(start_datetime) if empty_str_to_none(start_datetime) else None,
        end_datetime=datetime.fromisoformat(end_datetime) if empty_str_to_none(end_datetime) else None
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
        author=UserSchema(name=author_name) if author_name else None,
        board=BoardSchema(name=board_name) if board_name else None,
        created_at=created_at if created_at else datetime.now(tz)
    )


def handle_create_post(db, post_data: PostSchema):
    return create_post(db, post_data)


# --- GET ---
@router.get("/api/posts", response_model=PostSchemaResponse,
            response_model_exclude={"data": {"__all__": {"comments"}}})
async def get_posts(search_filter: PostSearch = Depends(post_search_query),
                    db=Depends(get_db),
                    limit=50,
                    page=1):
    offset = (int(page) - 1) * int(limit)
    return get_posts_by_search_dic(db, search_filter, limit, offset)


@router.get("/api/posts/{post_id}", response_model=PostSchemaResponse)
async def get_post(db=Depends(get_db), post_id=None):
    return get_post_detail_by_id(db, post_id)


@router.get("/api/statistics", response_model=StatisticsResponse)
async def get_statistics(search_filter: PostSearch = Depends(post_search_query),
                         db=Depends(get_db)):
    query = get_query_by_search_dic(db, search_filter)

    # 統計符合條件的文章總數
    total_count = query.count()
    return StatisticsResponse(result="success", search_filter=search_filter, result_count=total_count)


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
async def update_post(post_id: int, db=Depends(get_db), post_update: PostSchema = Body(...)):
    return update_post_from_id(db, post_id, post_update)


@router.put("/api/posts/form/{post_id}", response_model=PostSchemaResponse)
async def update_post_from_form(post_id, db=Depends(get_db), post_update: PostSchema = Depends(form_to_postschema)):
    return update_post_from_id(db, post_id, post_update)


# --- DELETE ---
@router.delete("/api/posts/{post_id}", response_model=PostSchemaResponse)
async def delete_post(post_id, db=Depends(get_db)):
    return delete_post_from_id(db, post_id)


app.include_router(router)
