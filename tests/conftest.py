from datetime import datetime

import pytest
from unittest.mock import MagicMock

from model.ptt_content import User, Post, Comment, Board
from schema.ptt_content import PostCrawl, CommentCrawl, PostSchema, BoardSchema, UserSchema, CommentSchema


@pytest.fixture
def db():
    db = MagicMock()
    db.query().all.return_value = {}
    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.return_value = None
    return db


@pytest.fixture
def dummy_postschema(dummy_commentschema):
    return PostSchema(
        id=None,
        title="test_post_schema",
        content="test_content",
        created_at=datetime.now(),
        board=BoardSchema(name="test_board"),
        author=UserSchema(name="test_author"),
        comments=[dummy_commentschema]
    )


@pytest.fixture
def dummy_commentschema():
    return CommentSchema(
        user=UserSchema(name="comment_user"),
        content="test_comment_content",
        created_at=datetime.now().isoformat()
    )


@pytest.fixture
def dummy_postcrawl(dummy_commentcrawl):
    return PostCrawl(
        title="test_post_crawl",
        content="test_content",
        created_at=datetime.now(),
        board_id=1,
        author="test_user",
        comments=[dummy_commentcrawl]
    )


@pytest.fixture
def dummy_commentcrawl():
    return CommentCrawl(
        user="comment_user",
        content="test_comment_content",
        created_at=datetime.now().isoformat()
    )


@pytest.fixture
def dummy_model_user():
    return User(
        id=1,
        name="test_user"
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
