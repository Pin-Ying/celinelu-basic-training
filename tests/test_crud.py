from db.crud import get_or_create_user, get_or_create_post, get_or_create_comment
from model.ptt_content import User, Post, Comment


# --- User ---
def test_get_or_create_user(sqlite_db):
    result = get_or_create_user(sqlite_db, username="test")
    assert sqlite_db.query(User).count() == 1
    assert result.name == "test"


# --- Post ---
def test_get_or_create_post(sqlite_db, dummy_model_post):
    result = get_or_create_post(sqlite_db, dummy_model_post)
    assert sqlite_db.query(Post).count() == 1
    assert result.title == dummy_model_post.title


# --- Comment ---
def test_get_or_create_comment(sqlite_db, dummy_model_comment):
    result = get_or_create_comment(sqlite_db, dummy_model_comment)
    assert sqlite_db.query(Comment).count() == 1
    assert result.content == dummy_model_comment.content
