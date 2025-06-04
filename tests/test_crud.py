from db.crud import (
    get_or_create_user,
    update_post_from_id, delete_post_from_id, get_or_create_board,
    get_all_boards, get_existing_user_map
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
