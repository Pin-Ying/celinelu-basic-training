from unittest.mock import MagicMock, patch

from sqlalchemy.orm import InstrumentedAttribute

from db.crud import (
    get_or_create_user,
    update_post_from_id, delete_post_from_id, get_or_create_board,
    get_all_boards, get_existing_user_map, get_or_create_post, get_query_by_post_search, get_posts_by_search,
    get_or_create_comment, get_existing_comments_keys_list
)


# -------- Tests for User --------
def test_get_or_create_user_new(db):
    db.query().filter_by().first.return_value = None
    user = get_or_create_user(db, "test_new")
    assert db.add.call_count == 1
    assert user.name == "test_new"


def test_get_or_create_user_existing(db, dummy_model_user):
    db.query().filter_by().first.return_value = dummy_model_user
    user = get_or_create_user(db, dummy_model_user.name)
    assert db.add.call_count == 0
    assert user.name == dummy_model_user.name


def test_get_existing_user_map(db, dummy_model_user):
    db.query().all.return_value = [dummy_model_user]
    user_map = get_existing_user_map(db)
    assert user_map == {dummy_model_user.name: dummy_model_user}


# -------- Tests for Post --------
def test_get_or_create_post_new(db, dummy_model_post):
    db.query().filter_by().first.return_value = []
    post = get_or_create_post(db, dummy_model_post)
    assert db.add.call_count == 1
    assert post == dummy_model_post


def test_get_or_create_post_existing(db, dummy_model_post):
    db.query().filter_by().first.return_value = dummy_model_post
    post = get_or_create_post(db, dummy_model_post)
    assert db.add.call_count == 0
    assert post == dummy_model_post


def test_update_post_from_id_success(db, dummy_postschema, dummy_model_post):
    db.get.return_value = dummy_model_post
    post = update_post_from_id(db, dummy_model_post.id, dummy_postschema)
    assert post == dummy_model_post


def test_delete_post_from_id_success(db, dummy_model_post):
    db.get.return_value = dummy_model_post
    post = delete_post_from_id(db, dummy_model_post.id)
    assert post.id == dummy_model_post.id


def test_get_query_by_post_search(db, dummy_postsearch):
    query = MagicMock()
    db.query.return_value = query
    query.options.return_value = query
    query.join.return_value = query
    query.filter.return_value = query
    query.order_by.return_value = query

    get_query_by_post_search(db, dummy_postsearch)
    join_calls = [call.args[0] for call in query.join.mock_calls]

    assert any(isinstance(arg, InstrumentedAttribute) and arg.key == "author" for arg in join_calls)
    assert any(isinstance(arg, InstrumentedAttribute) and arg.key == "board" for arg in join_calls)
    query.options.assert_called()
    query.filter.assert_called()
    query.order_by.assert_called_once()


def test_get_posts_by_search(db, dummy_postsearch, dummy_model_post):
    with patch("db.crud.get_query_by_post_search") as mock_get_query_by_post_search:
        query = MagicMock()
        mock_get_query_by_post_search.return_value = query
        query.offset().limit().all.return_value = [dummy_model_post]
        posts = get_posts_by_search(db, dummy_postsearch)
        assert posts == [dummy_model_post]


# -------- Tests for Comment --------
def test_get_or_create_comment_new(db, dummy_model_comment):
    db.query().filter_by().first.return_value = None
    comment = get_or_create_comment(db, dummy_model_comment)
    assert db.add.call_count == 1
    assert comment == dummy_model_comment


def test_get_or_create_comment_existing(db, dummy_model_comment):
    db.query().filter_by().first.return_value = dummy_model_comment
    comment = get_or_create_comment(db, dummy_model_comment)
    assert db.add.call_count == 0
    assert comment == dummy_model_comment


def test_get_existing_comments_keys_list(db, dummy_model_comment, dummy_model_post):
    db.query().filter_by().options().all.return_value = [dummy_model_comment]
    comments = get_existing_comments_keys_list(db, dummy_model_post.id)
    assert comments == [(dummy_model_comment.user.name, dummy_model_comment.content, dummy_model_comment.created_at)]


# -------- Tests for Board --------
def test_get_or_create_board_new(db):
    db.query().filter_by().first.return_value = None
    board = get_or_create_board(db, "test_new")
    assert db.add.call_count == 1
    assert board.name == "test_new"


def test_get_or_create_board_existing(db, dummy_model_board):
    db.query().filter_by().first.return_value = dummy_model_board
    board = get_or_create_board(db, dummy_model_board.name)
    assert db.add.call_count == 0
    assert board.name == dummy_model_board.name


def test_get_all_boards(db, dummy_model_board):
    db.query().all.return_value = [dummy_model_board]
    boards = get_all_boards(db)
    assert boards[dummy_model_board.name] == dummy_model_board.id
