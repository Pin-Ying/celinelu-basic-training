from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
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

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey('posts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    post = relationship('Post', back_populates='comments')
    user = relationship('User', back_populates='comments')
