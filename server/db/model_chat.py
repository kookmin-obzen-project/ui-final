from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.db import *
from typing import Annotated
from pydantic import *
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy import Boolean, Column, Integer, String, Text
import sys
sys.path.append("update-chat-server/server/")


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(50))
    # username = Column(String(50), unique=True)
    # question = Column(String(50))
    # answer = Column(String(50))


class ChatBase(BaseModel):
    text: str
    # Test 를 위한 sessionID 추가


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
