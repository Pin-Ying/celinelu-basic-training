from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock

import pytest

from db.crud import (
    get_or_create_user, create_post_from_postschema,
    update_post_from_id, delete_post_from_id, get_or_create_board,
    get_all_boards
)
from model.ptt_content import Post, User, Board, Comment
from schema.ptt_content import PostCrawl, CommentCrawl, PostSchema, UserSchema, BoardSchema, CommentSchema


# -------- Fixtures --------
@pytest.fixture
def db():
    return MagicMock()


@pytest.fixture
def dummy_postcrawl():
    return PostCrawl(
        title="test_post_crawl",
        content="test_content",
        created_at=datetime.now(),
        board_id=1,
        author="test_user",
        comments=[
            CommentCrawl(user="comment_user", content="test_comment_content", created_at=datetime.now().isoformat())
        ]
    )


@pytest.fixture
def dummy_postschema():
    return PostSchema(
        id=None,
        title="test_post_schema",
        content="test_content",
        created_at=datetime.now(),
        board=BoardSchema(name="test_board"),
        author=UserSchema(name="test_author"),
        comments=[
            CommentSchema(user=UserSchema(name="comment_user"), content="test_comment_content",
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
def dummy_model_board():
    return Board(
        id=1,
        name="test_board"
    )


@pytest.fixture
def dummy_model_comment(dummy_model_user):
    return Comment(
        id=1,
        content="test_comment_content",
        created_at="2025-05-27T15:30:00",
        user=dummy_model_user
    )


@pytest.fixture
def dummy_model_post(dummy_model_user, dummy_model_board, dummy_model_comment):
    return Post(
        id=1,
        title="test_post",
        content="test_content",
        created_at=datetime(2025, 5, 27, 12, 0, 0),
        author=dummy_model_user,
        board=dummy_model_board,
        comments=[dummy_model_comment]
    )


# -------- Tests for User --------
def test_get_or_create_user_new(db):
    db.query().get.return_value = None
    user = get_or_create_user(db, "test_new")
    assert db.add.call_count == 1
    assert user.name == "test_new"


def test_get_or_create_user_existing(db, dummy_model_user):
    db.query().get.return_value = dummy_model_user
    user = get_or_create_user(db, dummy_model_user.name)
    assert db.add.call_count == 0
    assert user.name == dummy_model_user.name


# -------- Tests for Post --------
# def test_existing_post_key(db, dummy_postcrawl, dummy_model_user, dummy_model_post):
#     # author => dummy_model_user
#     # existing_posts => dummy_model_post
#
#     mock_filter_user = MagicMock()
#     mock_filter_user.all.return_value = [dummy_model_user]
#
#     mock_filter_post = MagicMock()
#     mock_filter_post.all.return_value = [dummy_model_post]
#
#     # 因無法直接對應不同 query 結果 => 使用 side_effect
#     def query_side_effect(*args):
#         # db.query(User)
#         if len(args) == 1:
#             return MagicMock(filter=MagicMock(return_value=mock_filter_user))
#         # db.query(Post.title, Post.author_id, Post.created_at)
#         elif len(args) == 3:
#             return MagicMock(filter=MagicMock(return_value=mock_filter_post))
#         return MagicMock()
#
#     db.query = MagicMock(side_effect=query_side_effect)
#
#     post_keys = get_existing_post_keys(db, [dummy_postcrawl])
#
#     expected = {
#         (dummy_model_post.title, dummy_model_post.author_id, dummy_model_post.created_at)
#     }
#
#     assert post_keys == expected


def test_create_post_success(db, dummy_postschema, dummy_model_user, dummy_model_board):
    with mock.patch("db.crud.get_or_create_user") as mock_get_or_create_user, \
            mock.patch("db.crud.get_or_create_board") as mock_get_or_create_board:
        mock_get_or_create_user.return_value = dummy_model_user
        mock_get_or_create_board.return_value = dummy_model_board

        result = create_post_from_postschema(db, dummy_postschema)

        assert result.result == "success"
        assert result.data.title == dummy_postschema.title
        assert result.data.created_at == dummy_postschema.created_at


def test_update_post_from_id_success(db, dummy_postschema, dummy_model_post):
    db.query().filter().first.return_value = dummy_model_post
    response = update_post_from_id(db, dummy_model_post.id, dummy_postschema)
    assert response.result == "success"
    assert response.data.id == dummy_model_post.id


def test_delete_post_from_id_success(db, dummy_model_post):
    db.query().filter().first.return_value = dummy_model_post
    response = delete_post_from_id(db, dummy_model_post.id)
    assert response.result == "success"
    assert response.data.id == dummy_model_post.id


# -------- Tests for Board --------
def test_get_or_create_board_new(db):
    db.query().get.return_value = None
    board = get_or_create_board(db, "test_new")
    assert db.add.call_count == 1
    assert board.name == "test_new"


def test_get_or_create_board_existing(db, dummy_model_board):
    db.query().get.return_value = dummy_model_board
    board = get_or_create_board(db, dummy_model_board.name)
    assert db.add.call_count == 0
    assert board.name == dummy_model_board.name


def test_get_all_boards(db, dummy_model_board):
    db.query().all.return_value = [dummy_model_board]
    boards = get_all_boards(db)
    assert boards[dummy_model_board.name] == dummy_model_board.id

