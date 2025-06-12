from datetime import datetime
from unittest.mock import MagicMock

import pytest
from sqlalchemy import create_engine, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker

from db.database import Base
from model.ptt_content import User, Post, Comment, Board
from schema.ptt_content import PostCrawl, CommentCrawl, PostSchema, BoardSchema, UserSchema, CommentSchema, PostSearch


def replace_longtext_with_text(target, connection, **kw):
    if isinstance(target.type, LONGTEXT):
        target.type = Text()


@pytest.fixture
def sqlite_db():
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Post.__table__.c.content.type = Text()
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def db():
    db = MagicMock()
    db.query().all.return_value = {}
    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.return_value = None
    return db


# --- pydantic schema ---
@pytest.fixture
def dummy_postschema(dummy_commentschema):
    return PostSchema(
        id=None,
        title="test_post_schema",
        content="test_content",
        post_created_time=datetime.now(),
        board=BoardSchema(name="test_board"),
        author=UserSchema(name="test_author"),
        comments=[dummy_commentschema]
    )


@pytest.fixture
def dummy_commentschema():
    return CommentSchema(
        user=UserSchema(name="comment_user"),
        content="test_comment_content",
        comment_created_time=datetime.now().isoformat()
    )


@pytest.fixture
def dummy_postcrawl(dummy_commentcrawl):
    return PostCrawl(
        title="test_post_crawl",
        content="test_content",
        post_created_time=datetime.now(),
        board_id=1,
        author="test_user",
        comments=[dummy_commentcrawl]
    )


@pytest.fixture
def dummy_commentcrawl():
    return CommentCrawl(
        user="comment_user",
        content="test_comment_content",
        comment_created_time=datetime.now().isoformat()
    )


@pytest.fixture
def dummy_postsearch():
    return PostSearch(
        author=UserSchema(name="test_author"),
        board=BoardSchema(name="test_board"),
        start_datetime=datetime(2025, 5, 1),
        end_datetime=datetime(2025, 5, 31)
    )


# --- sqlalchemy model ---
@pytest.fixture
def dummy_model_user():
    return User(
        id=1,
        name="test_user"
    )


@pytest.fixture
def dummy_model_post(dummy_model_user, dummy_model_board):
    return Post(
        id=1,
        title="test_post",
        content="test_content",
        post_created_time=datetime(2025, 5, 27, 12, 0, 0),
        author=dummy_model_user,
        board=dummy_model_board
    )


@pytest.fixture
def dummy_model_board():
    return Board(
        id=1,
        name="test_board"
    )


@pytest.fixture
def dummy_model_comment(dummy_model_post, dummy_model_user):
    return Comment(
        id=1,
        content="test_comment_content",
        comment_created_time="2025-05-27T15:30:00",
        post=dummy_model_post,
        user=dummy_model_user
    )
