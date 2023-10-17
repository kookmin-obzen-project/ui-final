import httpx
from db.model_chat import *
from pydantic import *
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request
import sys

sys.path.append("update-chat-server/server")

app = FastAPI()
router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_chats(db: db_dependency):
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
    target_url = f"http://43.201.72.216:8000/{chat.text}"
    response = httpx.get(target_url, timeout=10.0)  # 10 seconds timeout
    text = {
        'answer': response.text,
    }
    db_chat = Chat(**chat.dict())
    db.add(db_chat)
    db.commit()

    return text
