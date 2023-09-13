import sys
sys.path.append("update-chat-server/server/")

from sqlalchemy import Boolean, Column, Integer, String, func, Text, DateTime
from sqlalchemy.dialects.mysql import DATETIME
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from pydantic import *
from typing import Annotated
from db.db import *
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

class ChatQuestion(Base):
    __tablename__ = 'chatQuestion'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    chatRoom_session = Column(String)
    created_at = Column(DateTime, default=func.now())
    # username = Column(String(50), unique=True)
    # question = Column(String(50))
    # answer = Column(String(50))
    
class ChatQuestionBase(BaseModel):
    text: str
    # Test 를 위한 sessionID 추가
    chatRoom_session: str
    created_at : datetime = datetime.now()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



# class Post(Base):
#     __tablename__ = 'posts'
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(50))
#     content = Column(String(100))
#     user_id = Column(Integer)

