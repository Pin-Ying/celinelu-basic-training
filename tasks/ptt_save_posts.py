from typing import List

from sqlalchemy.orm import Session

from db.crud import get_or_create_user, post_crawl_pydantic_to_sqlalchemy, get_or_create_post, \
    get_existing_comment_sets, get_existing_user_map, comment_input_pydantic_to_sqlalchemy
from model.ptt_content import Comment
from schema.ptt_content import PostCrawl, CommentCrawl


# ToDo: Combine Two Methods

def create_post_from_postcrawl(db: Session, post_input: PostCrawl):
    try:
        user_map = get_existing_user_map(db)
        # 取得作者
        author = get_or_create_user(db, post_input.author)
        new_post = post_crawl_pydantic_to_sqlalchemy(post_input, author.id)
        post = get_or_create_post(db, new_post)

        return post

    except Exception as e:
        db.rollback()
        raise e


def create_comments_bulk(db: Session, comments_inputs: List[CommentCrawl], post_id: int, user_map):
    try:
        comments = []
        existing_comment_rows = get_existing_comment_sets(db, post_id)
        seen_comments = set(existing_comment_rows)

        for comment in comments_inputs:
            comment_key = (comment.user, comment.content, comment.created_at)
            if (comment.user, comment.content, comment.created_at) in seen_comments:
                continue
            seen_comments.add(comment_key)

            comment_user = user_map.get(comment.user)
            if comment_user is None:
                comment_user = get_or_create_user(db, comment.user)
                user_map[comment.user] = comment_user

            comment = comment_input_pydantic_to_sqlalchemy(comment, comment_user.id, post_id)
            comments.append(comment)

        return comments

    except Exception as e:
        db.rollback()
        raise e