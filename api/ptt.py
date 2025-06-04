from datetime import datetime
from typing import Optional

import pytz
from fastapi import APIRouter, FastAPI, Depends, Form, Body
from sqlalchemy.exc import SQLAlchemyError

from db.crud import update_post_from_id, delete_post_from_id, \
    get_query_by_search_dic, get_post_detail_by_id, get_posts_by_search_dic, get_or_create_board, get_or_create_user, \
    get_or_create_post
from db.database import SessionLocal
from model.ptt_content import Post
from schema.ptt_content import PostSchema, PostSearch, UserSchema, BoardSchema, DataResponse, StatisticsResponse, \
    PostDetailSchema, CommentSchema, StatisticsData

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


def post_schema_sqlalchemy_to_pydantic(post_input: Post) -> PostSchema:
    return PostSchema(
        id=post_input.id,
        title=post_input.title,
        content=post_input.content,
        created_at=post_input.created_at,
        board=BoardSchema(name=post_input.board.name) if post_input.board else None,
        author=UserSchema(name=post_input.author.name) if post_input.author else None
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


def handle_create_post(db, post_schema: PostSchema):
    try:
        author = get_or_create_user(db, post_schema.author.name)
        board = get_or_create_board(db, post_schema.board.name)
        new_post = Post(
            title=post_schema.title,
            content=post_schema.content,
            created_at=post_schema.created_at,
            board_id=board.id,
            author_id=author.id
        )
        post_created = get_or_create_post(db, new_post)

        post_schema.id = post_created.id
        post_schema.created_at = post_created.created_at
        return DataResponse(result="Success", data=post_schema)
    except Exception as e:
        return DataResponse(result=f"error,{e}", data=post_schema)


# --- GET ---
@router.get("/api/posts", response_model=DataResponse,
            response_model_exclude={"data": {"__all__": {"comments"}}})
async def get_posts(search_filter: PostSearch = Depends(post_search_query),
                    db=Depends(get_db),
                    limit=50,
                    page=1):
    try:
        offset = (int(page) - 1) * int(limit)
        all_posts = get_posts_by_search_dic(db, search_filter, limit, offset)
        post_schema_list = [post_schema_sqlalchemy_to_pydantic(p) for p in all_posts]
        return DataResponse(result="Success", data=post_schema_list)
    except Exception as e:
        return DataResponse(result=f"error,{e}")


@router.get("/api/posts/{post_id}", response_model=DataResponse)
async def get_post(db=Depends(get_db), post_id=None):
    try:
        post_input = get_post_detail_by_id(db, post_id)
        if post_input is None:
            return DataResponse(result="PostNotFound")
        post_schema = PostDetailSchema(
            id=post_input.id,
            title=post_input.title,
            content=post_input.content,
            created_at=post_input.created_at,
            board=BoardSchema(name=post_input.board.name),
            author=UserSchema(name=post_input.author.name),
            comments=[
                CommentSchema(user=UserSchema(name=c.user.name), content=c.content, created_at=c.created_at)
                for c in post_input.comments
                if post_input.comments is not None
            ]
        )
        return DataResponse(result="Success", data=post_schema)
    except Exception as e:
        return DataResponse(result=f"error,{e}")


@router.get("/api/statistics", response_model=StatisticsResponse)
async def get_statistics(search_filter: PostSearch = Depends(post_search_query),
                         db=Depends(get_db)):
    try:
        query = get_query_by_search_dic(db, search_filter)

        # 統計符合條件的文章總數
        total_count = query.count()
        return StatisticsResponse(result="Success",
                                  data=StatisticsData(search_filter=search_filter, total_count=total_count))
    except Exception as e:
        return StatisticsResponse(result=f"error,{e}")


# --- POST ---
@router.post("/api/posts", response_model=DataResponse)
async def add_post(post_add: PostSchema = Body(...), db=Depends(get_db)):
    try:
        return handle_create_post(db, post_add)
    except Exception as e:
        return DataResponse(result=f"error,{e}")


# --- PUT ---
@router.put("/api/posts/{post_id}", response_model=DataResponse)
async def update_post(post_id: int, db=Depends(get_db), post_update: PostSchema = Body(...)):
    try:
        target_post = update_post_from_id(db, post_id, post_update)
        if target_post is None:
            return DataResponse(result="PostNotFound")
        post_update.id = target_post.id
        return DataResponse(result="Success", data=post_update)
    except Exception as e:
        return DataResponse(result=f"error,{e}", data=post_update)


# --- DELETE ---
@router.delete("/api/posts/{post_id}", response_model=DataResponse)
async def delete_post(post_id, db=Depends(get_db)):
    try:
        target_post = delete_post_from_id(db, post_id)
        if target_post is None:
            return DataResponse(result="PostNotFound")
        post_schema = post_schema_sqlalchemy_to_pydantic(target_post)
        return DataResponse(result="Success", data=post_schema)
    except Exception as e:
        return DataResponse(result=f"error,{e}")
