from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    posts = relationship('Post', back_populates='author')
    comments = relationship('Comment', back_populates='user')

class Board(Base):
    __tablename__ = 'boards'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    posts = relationship('Post', back_populates='board')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('users.id'))
    board_id = Column(Integer, ForeignKey('boards.id'))

    author = relationship('User', back_populates='posts')
    board = relationship('Board', back_populates='posts')
    comments = relationship('Comment', back_populates='post')

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

    __table_args__ = (
        UniqueConstraint('post_id', 'user_id', 'content','created_at' , name='uq_title_author_created_at'),
    )

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(10))
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
