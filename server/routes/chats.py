import sys
sys.path.append("update-chat-server/server")

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from pydantic import *
from typing import Annotated
from db.db import *
from db.model_chat  import Chat
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter


app = FastAPI()
router = APIRouter()
# Chat = Chat()
# Chat.metadata.create_all(bind=engine)

# origins = [
#      # "http://localhost:3000",
#      "*",
#  ]



class ChatBase(BaseModel):
    text: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", status_code=status.HTTP_200_OK)
async  def get_all_chats(db: db_dependency):
    chats = db.query(Chat).all()
    return chats

@router.get("/{session_id}", status_code=status.HTTP_200_OK)
async def read_chat(session_id: int, db: db_dependency):
    chat = db.query(Chat).filter(Chat.id == session_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail='chat not found')
    return chat


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chat(chat: ChatBase, db: db_dependency):
    db_chat = Chat(**chat.dict())
    db.add(db_chat)
    db.commit()


@router.delete("/{session_id}", status_code=status.HTTP_200_OK)
async def delete_chat(session_id: int, db: db_dependency):
    deleted = db.query(Chat).filter(Chat.id == session_id).first()
    if deleted is None:
        raise HTTPException(status_code=404, detail='chat not found')
    db.delete(deleted)
    db.commit()

# test 끝..
@router.post("/reflect", status_code=status.HTTP_200_OK)
async def reflect_chat(chat: ChatBase, db: db_dependency):
    # 받은 채팅 정보를 그대로 반환
    text =  {'answer':chat.text}
    return text


