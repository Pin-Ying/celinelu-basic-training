from datetime import datetime

import pytz
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship

from db.database import Base

tz = pytz.timezone("Asia/Taipei")
datetime_now = lambda: datetime.now(tz)

# ToDo: Comment 改欄位了!!!


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    posts = relationship('Post', back_populates='author')
    comments = relationship('Comment', back_populates='user')


class Board(Base):
    __tablename__ = 'boards'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    posts = relationship('Post', back_populates='board')


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(LONGTEXT)
    post_created_time = Column(DateTime)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    board_id = Column(Integer, ForeignKey('boards.id'), nullable=False)

    author = relationship('User', back_populates='posts')
    board = relationship('Board', back_populates='posts')
    comments = relationship('Comment', back_populates='post')

    __table_args__ = (
        UniqueConstraint('title', 'author_id', 'post_created_time', name='uq_title_author_created_time'),
    )


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    comment_created_time = Column(Text)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    post = relationship('Post', back_populates='comments')
    user = relationship('User', back_populates='comments')

    __table_args__ = (
        UniqueConstraint('post_id', 'user_id', 'content', 'comment_created_time', name='uq_post_author_created_time'),
    )


class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id = Column(Text, nullable=False)
    level = Column(String(10))
    message = Column(Text)
    created_at = Column(DateTime, default=datetime_now)
