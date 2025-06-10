from datetime import datetime
from typing import Optional

import pytz
from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.exc import SQLAlchemyError

from db.crud import update_post_from_id, delete_post_from_id, \
    get_query_by_post_search, get_post_detail_by_id, get_posts_by_search, get_or_create_board, get_or_create_user, \
    get_or_create_post
from db.database import SessionLocal
from model.ptt_content import Post
from schema.ptt_content import PostSchema, PostSearch, UserSchema, BoardSchema, PostDetailSchema, CommentSchema, \
    StatisticsData, DataResponse

router = APIRouter(prefix="/api", tags=["API"])
tz = pytz.timezone("Asia/Taipei")


def empty_str_to_none(s: str):
    if s and s.strip() != "":
        return s
    return None


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


def created_post_search(
        author_name: Optional[str] = "",
        board_name: Optional[str] = "",
        start_datetime: Optional[str] = "",
        end_datetime: Optional[str] = "",
) -> PostSearch:
    try:
        return PostSearch(
            author=UserSchema(name=author_name) if empty_str_to_none(author_name) else None,
            board=BoardSchema(name=board_name) if empty_str_to_none(board_name) else None,
            start_datetime=datetime.fromisoformat(start_datetime) if empty_str_to_none(start_datetime) else None,
            end_datetime=datetime.fromisoformat(end_datetime) if empty_str_to_none(end_datetime) else None
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise e


def post_schema_sqlalchemy_to_pydantic(post_input: Post) -> PostSchema:
    try:
        return PostSchema(
            id=post_input.id,
            title=post_input.title,
            content=post_input.content,
            post_created_time=post_input.post_created_time,
            board=BoardSchema(name=post_input.board.name) if post_input.board else None,
            author=UserSchema(name=post_input.author.name) if post_input.author else None
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise e


# --- GET ---
@router.get("/posts", summary="取得篩選文章列表",
            responses={200: {"model": DataResponse, "description": "成功"}},)
async def get_posts(search_filter: PostSearch = Depends(created_post_search),
                    db=Depends(get_db),
                    limit=50,
                    page=1):
    try:
        offset = (int(page) - 1) * int(limit)
        all_posts = get_posts_by_search(db, search_filter, limit, offset)
        post_schema_list = [post_schema_sqlalchemy_to_pydantic(p) for p in all_posts]
        return DataResponse(data=post_schema_list)

    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/posts/{post_id}", summary="取得指定ID的詳細文章資料",
            responses={200: {"model": DataResponse, "description": "成功"}})
async def get_post(db=Depends(get_db), post_id=None):
    try:
        post_input = get_post_detail_by_id(db, post_id)
        if post_input is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PostNotFound")
        post_schema = PostDetailSchema(
            id=post_input.id,
            title=post_input.title,
            content=post_input.content,
            post_created_time=post_input.post_created_time,
            board=BoardSchema(name=post_input.board.name),
            author=UserSchema(name=post_input.author.name),
            comments=[
                CommentSchema(user=UserSchema(name=c.user.name), content=c.content, comment_created_time=c.comment_created_time)
                for c in post_input.comments
                if post_input.comments is not None
            ]
        )
        return DataResponse(data=post_schema)
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/statistics", summary="取得篩選文章的統計資料",
            responses={200: {"model": DataResponse, "description": "成功"}})
async def get_statistics(search_filter: PostSearch = Depends(created_post_search),
                         db=Depends(get_db)):
    try:
        query = get_query_by_post_search(db, search_filter)

        # 統計符合條件的文章總數
        total_count = query.count()
        statistics_data = StatisticsData(search_filter=search_filter, total_count=total_count)
        return DataResponse(data=statistics_data)

    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# --- POST ---
@router.post("/posts", summary="新增文章")
async def add_post(post_schema: PostSchema = Body(...), db=Depends(get_db)):
    try:
        author = get_or_create_user(db, post_schema.author.name)
        board = get_or_create_board(db, post_schema.board.name)
        new_post = Post(
            title=post_schema.title,
            content=post_schema.content,
            post_created_time=post_schema.post_created_time,
            board_id=board.id,
            author_id=author.id
        )
        post_created = get_or_create_post(db, new_post)
        post_schema.id = post_created.id
        post_schema.post_created_time = post_created.post_created_time
        return DataResponse(data=post_schema)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# --- PUT ---
@router.put("/posts/{post_id}", summary="修改指定ID的文章")
async def update_post(post_id: int, db=Depends(get_db), post_update: PostSchema = Body(...)):
    try:
        target_post = update_post_from_id(db, post_id, post_update)
        if target_post is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PostNotFound")
        return DataResponse(data=post_update)
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# --- DELETE ---
@router.delete("/posts/{post_id}", summary="刪除指定ID的文章", status_code=204,
               responses={204: {"description": "成功刪除"}})
async def delete_post(post_id, db=Depends(get_db)):
    try:
        target_post = delete_post_from_id(db, post_id)
        if target_post is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PostNotFound")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
