import pytest
from unittest.mock import MagicMock
from datetime import datetime

from db.crud import (
    get_or_create_user,
    prepare_users_from_posts,
    post_crawl_pydantic_to_sqlalchemy,
    post_schema_pydantic_to_sqlalchemy,
    post_schema_sqlalchemy_to_pydantic,
    create_post,
    get_post_by_search_dic,
    get_or_create_board,
    get_all_boards,
    create_comments,
    log_crawl_result,
)
from model.ptt_content import Post, User, Board, Comment, Log
from schema.ptt_content import PostCrawl, CommentCrawl, PostSearch, PostSchema, BoardSchema, AuthorSchema


def test_get_or_create_user_found():
    mock_db = MagicMock()
    mock_db.query().filter_by().first.return_value = User(id=1, name="alice")
    user = get_or_create_user(mock_db, "alice")
    assert user.name == "alice"


def test_get_or_create_user_create():
    mock_db = MagicMock()
    mock_db.query().filter_by().first.side_effect = [None, User(id=1, name="bob")]
    user = get_or_create_user(mock_db, "bob")
    assert user.name == "bob"


def test_prepare_users_from_posts():
    mock_db = MagicMock()
    posts = [
        PostCrawl(title="t1", content="c1", created_at=datetime.now(), board_id=1, author="alice", comments=[]),
        PostCrawl(title="t2", content="c2", created_at=datetime.now(), board_id=1, author="bob", comments=[
            CommentCrawl(user="carol", content="comment", created_at=datetime.now().isoformat())
        ])
    ]
    mock_db.query().filter().all.return_value = []
    users = prepare_users_from_posts(mock_db, posts)
    assert set(users.keys()) == {"alice", "bob", "carol"}


def test_post_pydantic_conversions():
    dt = datetime.now()
    post_crawl = PostCrawl(title="t", content="c", created_at=dt, board_id=1, author="a", comments=[])
    post_model = post_crawl_pydantic_to_sqlalchemy(post_crawl, author_id=1)
    assert post_model.title == "t"

    post_schema = PostSchema(id=None, title="t", content="c", created_at=dt,
                             board=BoardSchema(name="b"), author=AuthorSchema(name="a"))
    post_model = post_schema_pydantic_to_sqlalchemy(post_schema, 1, 2)
    assert post_model.board_id == 2

    post = Post(id=1, title="t", content="c", created_at=dt,
                author=User(id=1, name="a"), board=Board(id=1, name="b"))
    schema = post_schema_sqlalchemy_to_pydantic(post)
    assert schema.title == "t"
    assert schema.author.name == "a"


def test_create_post_success():
    mock_db = MagicMock()
    mock_db.query().filter_by().first.side_effect = [None, None, Board(id=1, name="NBA")]
    mock_db.flush.side_effect = None
    post_schema = PostSchema(id=None, title="t", content="c", created_at=datetime.now(),
                             board=BoardSchema(name="NBA"), author=AuthorSchema(name="a"))
    response = create_post(mock_db, post_schema)
    assert response.result == "success"


def test_get_post_by_search_dic():
    mock_db = MagicMock()
    post_search = PostSearch(
        author=AuthorSchema(name="a"),
        board=BoardSchema(name="NBA"),
        start_datetime=datetime(2023, 1, 1),
        end_datetime=datetime(2024, 1, 1)
    )
    mock_query = mock_db.query().options().join().filter().join().filter().filter().filter().order_by().offset().limit()
    mock_query.all.return_value = ["post_match"]
    posts = get_post_by_search_dic(mock_db, post_search)
    assert isinstance(posts, list)
    assert len(posts) == 1


def test_get_or_create_board():
    mock_db = MagicMock()
    mock_db.query().filter_by().first.side_effect = [None, Board(id=1, name="NBA")]
    board = get_or_create_board(mock_db, "NBA")
    assert board.name == "NBA"


def test_get_all_boards():
    mock_db = MagicMock()
    mock_db.query().all.return_value = [Board(id=1, name="NBA"), Board(id=2, name="Gossiping")]
    boards = get_all_boards(mock_db)
    assert boards == {"NBA": 1, "Gossiping": 2}


def test_create_comments():
    mock_db = MagicMock()
    user_map = {"alice": User(id=1, name="alice")}
    post_input = PostCrawl(
        title="t", content="c", created_at=datetime.now(), board_id=1, author="alice",
        comments=[CommentCrawl(user="alice", content="hi", created_at=datetime.now().isoformat())]
    )
    new_post = Post(id=1)
    mock_db.query().filter_by().all.return_value = []
    create_comments(mock_db, new_post, post_input, user_map)
    mock_db.add.assert_called()


def test_log_crawl_result():
    mock_db = MagicMock()
    log_crawl_result(mock_db, "test message", "DEBUG")
    mock_db.add.assert_called()
    mock_db.commit.assert_called()
