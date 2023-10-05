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

## <문제> : 답변을 줄 때 Data type 을 정의하기 어려움
## <조건> : any 등 type 을 mysql 은 동적으로 받을 수 없음 
## <해결방안> : 1. NoSQL 알아보기
##            2. 예상 답변 타입을 지정 후 default 값을 설정하기

class ChatAnswer(Base):
    __tablename__ = 'chatAnswer'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, default=None)
    chatRoom_ID = Column(String, unique=True)
    session_ID = Column(String, unique=True)
    created_at = Column(DateTime, default=func.now())
    
class ChatAnswerBase(BaseModel):
    text: str
    chatRoom_ID: str
    session_ID : str
    created_at : datetime = datetime.now()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

