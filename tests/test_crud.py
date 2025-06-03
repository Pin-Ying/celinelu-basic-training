from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock

import pytest

from db.crud import (
    get_or_create_user,
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

