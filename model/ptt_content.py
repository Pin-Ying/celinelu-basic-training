from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from db.database import  Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    posts = relationship('Post', back_populates='author')
    comments = relationship('Comment', back_populates='user')

class Board(Base):
    __tablename__ = 'boards'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    posts = relationship('Post', back_populates='board')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('users.id'))
    board_id = Column(Integer, ForeignKey('boards.id'))

    author = relationship('User', back_populates='posts')
    board = relationship('Board', back_populates='posts')
    comments = relationship('Comment', back_populates='post')

    # 確保不會重複同一篇文章(標題、作者、時間)
    __table_args__ = (
        UniqueConstraint('title', 'author_id', 'created_at', name='uq_title_author_created_at'),
    )

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    created_at = Column(Text)
    post_id = Column(Integer, ForeignKey('posts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    post = relationship('Post', back_populates='comments')
    user = relationship('User', back_populates='comments')

    # 確保不會重複同一則留言(來源文章、發言者、發言內容、時間)
    __table_args__ = (
        UniqueConstraint('post_id', 'user_id', 'content','created_at' , name='uq_title_author_created_at'),
    )

class CrawlLog(Base):
    __tablename__ = 'crawl_logs'
    id = Column(Integer, primary_key=True)
    board = Column(String)
    post_count = Column(Integer)
    success = Column(Boolean)
    error = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.now)
