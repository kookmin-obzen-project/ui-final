from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.db import *
from typing import Annotated
from pydantic import *
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy import Boolean, Column, Integer, String, func, Text, DateTime
import sys
sys.path.append("update-chat-server/server/")


class ChatQuestion(Base):
    __tablename__ = 'chatQuestion'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, default=None)
    chatRoom_ID = Column(String(255), unique=True)
    session_ID = Column(String(255))
    created_at = Column(DateTime, default=func.now())


class ChatQuestionBase(BaseModel):
    text: str
    chatRoom_ID: str
    session_ID: str
    created_at: datetime = datetime.now()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
