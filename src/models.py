import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import declarative_base, relationship
from eralchemy2 import render_er

Base = declarative_base()

followers = Table('followers', Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('following_id', Integer, ForeignKey('users.id'), primary_key=True)
)

messages = Table('messages', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('text', String, nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('sender_id', Integer, ForeignKey('users.id')),
    Column('receiver_id', Integer, ForeignKey('users.id'))
)

post_tags = Table('post_tags', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    bio = Column(String)
    profile_picture_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    stories = relationship("Story", back_populates="user")
    following = relationship(
        "User",
        secondary=followers,
        primaryjoin=id == followers.c.follower_id,
        secondaryjoin=id == followers.c.following_id,
        backref="followers"
    )
    sent_messages = relationship(
        "Message",
        foreign_keys=[messages.c.sender_id],
        backref="sender"
    )
    received_messages = relationship(
        "Message",
        foreign_keys=[messages.c.receiver_id],
        backref="receiver"
    )
    posts = relationship("Post", back_populates="user")

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True)
    content_url = Column(String, nullable=False)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="stories")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    caption = Column(String, nullable=False)
    image_url_video_url = Column(String, nullable=False)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    post = relationship("Post", back_populates="comments")
    user = relationship("User")

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    post = relationship("Post", back_populates="likes")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")


## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
