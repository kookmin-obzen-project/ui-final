import sys
sys.path.append("update-chat-server/server/")
from sqlalchemy import *
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from pydantic import *
from typing import Annotated
from db.db import *
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

class Session(Base):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    expired_at = Column(DateTime, default= None)
    user_session = Column(String, unique=True, index=True)

class SessionBase(BaseModel):
    created_at : datetime = datetime.now()
    user_session : str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

