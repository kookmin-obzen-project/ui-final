import sys
sys.path.append("update-chat-server/server/")
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, func, Text, DateTime
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from pydantic import *
from typing import Annotated
from db.db import *
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


class ChatRoom(Base):
    __tablename__ = 'chatRoom'

    id = Column(Integer, primary_key=True, index=True)
    user_session = Column(String, unique=True, server_default='')
    created_at = Column(DateTime, default=func.now())
    name = Column(String)
    
class ChatRoomBase(BaseModel):
    user_session: str
    # Test 를 위한 sessionID 추가
    created_at : datetime = datetime.now()
    name: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

