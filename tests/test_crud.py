from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Query

from db.crud import (
    get_or_create_user, prepare_users_from_posts, create_post, create_posts_bulk,
    get_newest_post, get_posts_by_search_dic,
    update_post_from_id, delete_post_from_id, get_or_create_board,
    log_crawl_result, get_all_boards, get_post_detail_by_id, get_query_by_search_dic
)
from model.ptt_content import Post, User, Board, Comment
from schema.ptt_content import PostCrawl, CommentCrawl, PostSchema, UserSchema, BoardSchema, PostSearch, CommentSchema, \
    PostSchemaResponse


# -------- Fixtures --------
@pytest.fixture
def db():
    return MagicMock()


@pytest.fixture
def dummy_postcrawl():
    return PostCrawl(
        title="Sample Title",
        content="Sample Content",
        created_at=datetime.now(),
        board_id=1,
        author="test_user",
        comments=[
            CommentCrawl(user="comment_user", content="Nice post!", created_at=datetime.now().isoformat())
        ]
    )


@pytest.fixture
def dummy_postschema():
    return PostSchema(
        id=None,
        title="Test Post",
        content="Content here",
        created_at=datetime.now(),
        board=BoardSchema(name="test_board"),
        author=UserSchema(name="test_author"),
        comments=[
            CommentSchema(user=UserSchema(name="comment_user"), content="Nice post!",
                          created_at=datetime.now().isoformat())
        ]
    )


@pytest.fixture
def dummy_model_user():
    return User(
        id=1,
        name="test_user"
    )


@pytest.fixture
def dummy_model_post():
    the_board = Board(
        id=1,
        name="NBA"
    )

    the_user = User(
        id=1,
        name="test"
    )

    the_comment = Comment(
        id=1,
        content="test-comment-content",
        created_at="2025-05-27T15:30:00",
        post_id=1,
        user_id=1,
        user=the_user  # ✅ 關鍵補上
    )

    return Post(
        id=1,
        title="test-post",
        content="test-content",
        created_at=datetime(2025, 5, 27, 12, 0, 0),
        author=the_user,
        board=the_board,
        comments=[the_comment]
    )


# -------- Tests for User --------
def test_get_or_create_user_existing(db):
    db.query().filter_by().first.return_value = User(id=1, name="test")
    user = get_or_create_user(db, "test")
    assert user.name == "test"


def test_prepare_users_from_posts(db, dummy_postcrawl):
    db.query().filter().all.return_value = []
    user_map = prepare_users_from_posts(db, [dummy_postcrawl])
    assert db.add_all.call_count == 1
    assert "test_user" in user_map
    assert "comment_user" in user_map


# -------- Tests for Post --------
def test_create_post_success(db, dummy_postschema):
    with mock.patch("db.crud.get_or_create_user") as mock_get_or_create_user:
        mock_get_or_create_user.return_value = User(id=1, name="test_author")
    with mock.patch("db.crud.get_or_create_board") as mock_get_or_create_board:
        mock_get_or_create_board.return_value = Board(id=1, name="test_board")
    pose_response = create_post(db, dummy_postschema)
    assert pose_response.result == "success"


def test_create_posts_bulk_success(db, dummy_postcrawl):
    with mock.patch("db.crud.get_existing_post_keys") as mock_get_existing_post_keys:
        mock_get_existing_post_keys.return_value = {}
    created = create_posts_bulk(db, [dummy_postcrawl])
    assert len(created) == 1
    assert isinstance(created[0], Post)
    assert db.add.call_count >= 2  # post, comment
    assert db.commit.called


def test_get_newest_post(db):
    post = Post(id=1, title="Newest", created_at=datetime.now())
    db.query().filter_by().order_by().first.return_value = post
    result = get_newest_post(db, 1)
    assert result.title == "Newest"


def test_get_post_detail_by_id(db, dummy_model_post):
    mock_query = db.query.return_value
    mock_filter_by = mock_query.filter_by.return_value
    mock_join = mock_filter_by.join.return_value
    mock_filter = mock_join.filter.return_value
    mock_filter.first.return_value = dummy_model_post

    result = get_post_detail_by_id(db, 1)

    assert result.result == "success"
    assert result.data.id == 1
    assert result.data.comments[0].content == "test-comment-content"


def test_update_post_from_id_success(db, dummy_postschema):
    db.query().filter().first.return_value = Post(id=1)
    response = update_post_from_id(db, 1, dummy_postschema)
    assert response.result == "success"
    assert response.data.id == 1


def test_delete_post_from_id_success(db):
    post = Post(id=1, title="Del", content="x", created_at=datetime.now(), board=Board(name="test_board"),
                author=User(name="test_user"))
    db.query().filter().first.return_value = post
    response = delete_post_from_id(db, 1)
    assert response.result == "success"
    assert response.data.id == 1


# -------- Tests for Board --------
def test_get_or_create_board_new(db):
    db.query().filter_by().first.return_value = None
    board = get_or_create_board(db, "test_board")
    assert board.name == "test_board"


def test_get_all_boards(db):
    db.query().all.return_value = [Board(id=1, name="test")]
    boards = get_all_boards(db)
    assert boards["test"] == 1


# -------- Tests for Log --------
def test_log_crawl_result(db):
    log_crawl_result(db, "Crawling success", "INFO")
    db.add.assert_called_once()
    db.commit.assert_called_once()

# # -------- Tests for init/clean --------
# def test_create_default_runs():
#     # 不測試 DB 實作，只測試是否會成功執行
#     try:
#         create_default()
#         assert True
#     except Exception:
#         assert False
#
#
# def test_clean_tables_runs():
#     try:
#         clean_tables()
#         assert True
#     except Exception:
#         assert False
