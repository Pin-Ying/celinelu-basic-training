import pytest

from db.crud import get_or_create_user, create_post, get_post_filter_by, create_posts_bulk, get_or_create_board, \
    log_crawl_result
from model.ptt_content import User, Log
from schema.ptt_content import PostSchema, BoardSchema, AuthorSchema, PostCrawl, CommentCrawl


# --- User ---
def test_get_or_create_user(db):
    user = get_or_create_user(db, "test_user")
    user1 = get_or_create_user(db, "existing_user")
    user2 = get_or_create_user(db, "existing_user")
    assert user.name == "test_user"
    assert isinstance(user, User)
    assert user1.id == user2.id


# --- Post ---
def test_create_post(db):
    schema = PostSchema(
        title="test_title",
        content="test_content",
        board=BoardSchema(name="test_board"),
        author=AuthorSchema(name="test_user")
    )
    resp = create_post(db, schema)
    assert resp.result == "success"
    assert resp.data.id is not None


def test_get_post_filter_by(db):
    schema = PostSchema(
        title="Hello",
        content="world",
        board=BoardSchema(name="board1"),
        author=AuthorSchema(name="alice")
    )
    create_post(db, schema)
    posts = get_post_filter_by(db, title="Hello")
    assert len(posts) == 1


def test_create_posts_bulk(db):
    post = PostCrawl(
        title="Sample",
        content="with comments",
        created_at="2024-01-01T00:00:00",
        board_id=1,
        author="bob",
        comments=[
            CommentCrawl(user="c1", content="Nice!", created_at="2024-01-01T01:00:00"),
            CommentCrawl(user="c2", content="Great!", created_at="2024-01-01T01:30:00"),
        ]
    )
    posts = create_posts_bulk(db, [post])
    assert len(posts) == 1
    assert len(posts[0].comments) == 2


def test_get_or_create_board(db):
    board = get_or_create_board(db, "test_board")
    board1 = get_or_create_board(db, "test_board")
    board2 = get_or_create_board(db, "test_board")
    assert board.name == "test_board"
    assert board1.id == board2.id


def test_log_write(db):
    log_crawl_result(db, "Something happened", "INFO")
    log = db.query(Log).first()
    assert log.message == "Something happened"
    assert log.level == "INFO"
