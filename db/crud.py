import time
from typing import List

from sqlalchemy.exc import OperationalError, SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session, joinedload

from db.database import Base, engine, SessionLocal
from model.ptt_content import User, Post, Comment, Board, Log
from schema.ptt_content import PostCrawl, CommentCrawl, PostSearch, PostSchema, PostSchemaResponse, BoardSchema, \
    UserSchema, CommentSchema, PostDetailSchema


def create_default():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    all_boards = {'home-sale': 1, 'basketballTW': 2, 'NBA': 3, 'car': 4, 'Lifeismoney': 5}
    seed_boards(db, all_boards)
    db.close()


def safe_commit(session: Session, retries: int = 3, delay: float = 0.5):
    for attempt in range(retries):
        try:
            session.commit()
            return
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                raise
        except OperationalError as e:
            if "Deadlock found" in str(e):
                session.rollback()
                time.sleep(delay)
                continue
            raise
        except Exception:
            session.rollback()
            raise
    raise Exception("Deadlock could not be resolved after retries.")


# --- User ---
def get_or_create_user(db: Session, username: str) -> type[User] | None | User:
    user = db.query(User).filter_by(name=username).first()
    if user:
        return user
    try:
        user = User(name=username)
        db.add(user)
        db.flush()
        return user
    except IntegrityError:
        db.rollback()
        return user


# ToDo : test method
def get_existing_user_map(db: Session):
    existing_users = db.query(User).all()
    return {u.name: u for u in existing_users}


def prepare_users_from_posts(db: Session, posts: list[PostCrawl]):
    all_usernames = set()
    for p in posts:
        all_usernames.add(p.author)
        for c in p.comments:
            all_usernames.add(c.user)

    existing_users = db.query(User).filter(User.name.in_(all_usernames)).all()
    user_map = {u.name: u for u in existing_users}

    missing_usernames = all_usernames - user_map.keys()
    username: str
    new_users = [User(name=username) for username in missing_usernames]

    if new_users:
        db.add_all(new_users)
        db.flush()

    for user in new_users:
        user_map[user.name] = user

    return user_map


# --- Post ---
def post_crawl_pydantic_to_sqlalchemy(post_input: PostCrawl, author_id: int) -> Post:
    return Post(
        title=post_input.title,
        content=post_input.content,
        created_at=post_input.created_at,
        board_id=post_input.board_id,
        author_id=author_id
    )


def post_schema_pydantic_to_sqlalchemy(post_input: PostSchema, author_id: int, board_id: int) -> Post:
    return Post(
        title=post_input.title,
        content=post_input.content,
        created_at=post_input.created_at,
        board_id=board_id,
        author_id=author_id
    )


def post_schema_sqlalchemy_to_pydantic(post_input: Post) -> PostSchema:
    return PostSchema(
        id=post_input.id,
        title=post_input.title,
        content=post_input.content,
        created_at=post_input.created_at,
        board=BoardSchema(name=post_input.board.name),
        author=UserSchema(name=post_input.author.name)
    )


def post_detail_sqlalchemy_to_pydantic(post_input: Post) -> PostDetailSchema:
    return PostDetailSchema(
        id=post_input.id,
        title=post_input.title,
        content=post_input.content,
        created_at=post_input.created_at,
        board=BoardSchema(name=post_input.board.name),
        author=UserSchema(name=post_input.author.name),
        comments=[
            CommentSchema(user=UserSchema(name=c.user.name), content=c.content, created_at=c.created_at)
            for c in post_input.comments
            if post_input.comments is not None
        ]
    )


def get_latest_post(db: Session, board: int):
    return db.query(Post).filter_by(board_id=board).order_by(Post.created_at.desc()).first()


def get_query_by_search_dic(db: Session, post_search: PostSearch):
    query = db.query(Post).options(
        joinedload(Post.author),
        joinedload(Post.board)
    )

    filters = []
    if post_search.author:
        query = query.join(Post.author)
        filters.append(User.name == post_search.author.name)

    if post_search.board:
        query = query.join(Post.board)
        filters.append(Board.name == post_search.board.name)

    if post_search.start_datetime:
        filters.append(Post.created_at >= post_search.start_datetime)

    if post_search.end_datetime:
        filters.append(Post.created_at <= post_search.end_datetime)

    return query.filter(*filters).order_by(Post.created_at.desc())


def get_posts_by_search_dic(db: Session, search_filter, posts_limit=50, posts_offset=0):
    all_posts = get_query_by_search_dic(db, search_filter).offset(posts_offset).limit(posts_limit).all()
    post_schema_list = [post_schema_sqlalchemy_to_pydantic(p) for p in all_posts]
    return PostSchemaResponse(result="success", data=post_schema_list)


def get_post_detail_by_id(db: Session, post_id: int):
    the_post = db.query(Post).filter_by(id=post_id)
    the_post = the_post.options(joinedload(Post.comments)).first()
    if the_post is None:
        return PostSchemaResponse(result="PostNotFound")
    post_schema = post_detail_sqlalchemy_to_pydantic(the_post)
    return PostSchemaResponse(result="success", data=post_schema)


def get_existing_post_keys(db: Session, posts: list[PostCrawl]):
    min_date = min(p.created_at for p in posts)
    max_date = max(p.created_at for p in posts)

    authors = list(set(p.author for p in posts))
    author_map = {
        u.name: u.id for u in db.query(User).filter(User.name.in_(authors)).all()
    }

    post_keys = set()
    if author_map:
        existing_posts = db.query(Post.title, Post.author_id, Post.created_at).filter(
            Post.created_at >= min_date,
            Post.created_at <= max_date
        ).all()

        post_keys = set((p.title, p.author_id, p.created_at) for p in existing_posts)

    return post_keys


# ToDo: test method
def get_or_create_post(db: Session, post_input: Post):
    post = db.query(Post).filter_by(
        title=post_input.title,
        author_id=post_input.author_id,
        created_at=post_input.created_at
    ).first()
    if post:
        return post
    try:
        db.add(post_input)
        db.commit()
        db.refresh(post_input)
        return post_input
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise e


def create_post_from_postschema(db: Session, post_schema: PostSchema):
    try:
        author = get_or_create_user(db, post_schema.author.name)
        board = get_or_create_board(db, post_schema.board.name)
        new_post = post_schema_pydantic_to_sqlalchemy(post_schema, author.id, board.id)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        post_schema.id = new_post.id
        post_schema.created_at = new_post.created_at

    except SQLAlchemyError as e:
        return PostSchemaResponse(result=f"error,{e}", data=post_schema)
    except Exception as e:
        return PostSchemaResponse(result=f"error,{e}", data=post_schema)

    return PostSchemaResponse(result="success", data=post_schema)


def update_post_from_id(db: Session, post_id, post_schema: PostSchema):
    target_post = db.get(Post, post_id)
    author = get_or_create_user(db, post_schema.author.name)
    board = get_or_create_board(db, post_schema.board.name)
    if target_post is None:
        return PostSchemaResponse(result="PostNotFound")
    target_post.title = post_schema.title
    target_post.content = post_schema.content
    target_post.created_at = post_schema.created_at
    target_post.author = author
    target_post.board = board

    try:
        db.add(target_post)
        db.commit()
        db.refresh(target_post)
        post_schema.id = target_post.id
    except SQLAlchemyError as e:
        return PostSchemaResponse(result=f"error,{e}", data=post_schema)
    except Exception as e:
        return PostSchemaResponse(result=f"error,{e}", data=post_schema)

    return PostSchemaResponse(result="success", data=post_schema)


def delete_post_from_id(db: Session, post_id):
    target_post = db.get(Post, post_id)
    if target_post is None:
        return PostSchemaResponse(result="PostNotFound")
    try:
        post_schema = post_schema_sqlalchemy_to_pydantic(target_post)
        db.delete(target_post)
        db.commit()
    except SQLAlchemyError as e:
        return PostSchemaResponse(result=f"error,{e}", data=post_schema)
    except Exception as e:
        return PostSchemaResponse(result=f"error,{e}", data=post_schema)

    return PostSchemaResponse(result="success", data=post_schema)


# --- Comment ---
def comment_pydantic_to_sqlalchemy(comment_input: CommentCrawl, user_id: int, post_id: int):
    return Comment(
        post_id=post_id,
        user_id=user_id,
        content=comment_input.content,
        created_at=comment_input.created_at
    )


# ToDo: test method
def get_or_create_comment(db: Session, comment_input: Comment):
    comment = db.query(Comment).filter_by(
        post_id=comment_input.post_id,
        user_id=comment_input.user_id,
        content=comment_input.content,
        created_at=comment_input.created_at
    ).first()
    if comment:
        return comment
    try:
        db.add(comment_input)
        db.commit()
        db.refresh(comment_input)
        return comment_input
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise e


def get_existing_comment_set(db: Session, post_id: int) -> List:
    comments = (
        db.query(Comment)
        .filter_by(post_id=post_id)
        .options(joinedload(Comment.user))
        .all()
    )
    if comments:
        return [(comment.user.name, comment.content, comment.created_at) for comment in comments]

    return []


def create_comments_bulk(db: Session, comments: List[Comment]):
    try:
        db.add_all(comments)
        db.commit()
        db.refresh(comments)
        return comments
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise e


# --- Board ---
def get_all_boards(db: Session):
    boards = db.query(Board).all()
    return {b.name: b.id for b in boards}


def get_or_create_board(db: Session, boardname: str) -> type[Board] | None | User:
    board = db.query(Board).filter_by(name=boardname).first()
    if board:
        return board
    try:
        board = Board(name=boardname)
        db.add(board)
        db.commit()
        db.refresh(board)
        return board
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise e


def seed_boards(db: Session, board_dic: dict):
    for name, id_ in board_dic.items():
        exists = db.query(Board).filter_by(id=id_).first()
        if not exists:
            db.add(Board(id=id_, name=name))
    db.commit()


# --- Log ---
def log_crawl_result(db: Session, task_id: str, message: str, level: str = "INFO"):
    log = Log(task_id=task_id, message=message, level=level)
    db.add(log)
    db.commit()


if __name__ == "__main__":
    create_default()
