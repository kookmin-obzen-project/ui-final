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
    chatRoom_ID = Column(String(255), unique=True)
    name = Column(String(255), default=None)
    created_at = Column(DateTime, default=func.now())
    
    
class ChatRoomBase(BaseModel):
    chatRoom_ID : str
    name: str = ""
    created_at : datetime = datetime.now()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

