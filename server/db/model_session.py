import json
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.db import *
from typing import Annotated
from pydantic import *
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy import *
import sys
sys.path.append("update-chat-server/server/")


class Session(Base):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    expired_at = Column(DateTime, default=None)
    session_ID = Column(String(255), unique=True)


class SessionBase(BaseModel):
    created_at: datetime = datetime.now()
    expired_at: datetime = None
    session_ID: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
