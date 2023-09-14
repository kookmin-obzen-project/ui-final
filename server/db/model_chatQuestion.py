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
    chat_session = Column(String)
    user_session = Column(String, unique=True)
    created_at = Column(DateTime, default=func.now())
    
class ChatQuestionBase(BaseModel):
    text: str
    chat_session: str
    user_session : str
    created_at : datetime = datetime.now()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

