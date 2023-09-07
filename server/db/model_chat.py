import sys
sys.path.append("update-chat-server/server/")

from sqlalchemy import Boolean, Column, Integer, String
from db.db import Base

class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(50))
    # username = Column(String(50), unique=True)
    # question = Column(String(50))
    # answer = Column(String(50))
    


# class Post(Base):
#     __tablename__ = 'posts'
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(50))
#     content = Column(String(100))
#     user_id = Column(Integer)

