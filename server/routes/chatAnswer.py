import sys
sys.path.append("update-chat-server/server")

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from pydantic import *
from db.model_chat  import *
from db.model_chatRoom  import *
from db.model_chatAnswer  import *
from db.model_chatQuestion  import *
from fastapi import APIRouter, Request


app = FastAPI()
router = APIRouter()

# chatAnswer 테이블에 있는 데이터 가져오기
@router.get("/", status_code=status.HTTP_200_OK)
async  def get_all_chatAnswer(db: db_dependency):
    chatAnswer = db.query(ChatAnswer).all()
    return chatAnswer

# chatAnswer sessionID 로 필터링 후 해당 채팅방 전체 답변 받아오기
@router.get("/{user_session}/{chat_session}", status_code=status.HTTP_200_OK)
async def get_user_chatAnswer(user_session: str, chat_session: str, db: db_dependency):
    chatAnswer = db.query(ChatAnswer).filter(
        and_(
            ChatAnswer.user_session == user_session,
            ChatAnswer.chat_session == chat_session)
        ).all()
    if len(chatAnswer) == 0:
        chatRoom = db.query(ChatRoom).filter(ChatRoom.user_session == session_id).first()
        if chatRoom is None: 
            raise HTTPException(status_code=404, detail='chatRoom not found')
        else:
            raise HTTPException(status_code=404, detail='Answer does not exist')
    return chatAnswer

# chatAnswer sessionID 로 필터링 후 해당 채팅방 특정 답변 받아오기
@router.get("/{user_session}/{chat_session}/{chat_id}", status_code=status.HTTP_200_OK)
async def get_user_chatAnswer(user_session: str, chat_session: str, chat_id: int, db: db_dependency):
    chatAnswer = db.query(ChatAnswer).filter(
        and_(
            ChatAnswer.user_session == user_session,
            ChatAnswer.chat_session == chat_session,
            ChatAnswer.id == chat_id)
        ).first()
    if chatAnswer is None:
        chatRoom = db.query(ChatRoom).filter(ChatRoom.user_session == session_id).first()
        if chatRoom is None: 
            raise HTTPException(status_code=404, detail='chatRoom not found')
        else:
            raise HTTPException(status_code=404, detail='Answer does not exist')
    return chatAnswer

# chatAnswer 생성하기
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chat(chatAnswer: ChatAnswerBase, db: db_dependency):
    db_chatAnswer = ChatAnswer(**chatAnswer.dict())
    db.add(db_chatAnswer)
    db.commit()

# chatRoom sessionID 로 필터링 후 해당 채팅방 전체 질문 삭제하기
@router.delete("/{user_session}/{chat_session}", status_code=status.HTTP_200_OK)
async def delete_chat(user_session: str, chat_session: str, db: db_dependency):
    deleted = db.query(ChatAnswer).filter(
        and_(
            ChatAnswer.user_session == user_session,
            ChatAnswer.chat_session == chat_session)
        ).all()
    if len(deleted) == 0:
        chatRoom = db.query(ChatRoom).filter(ChatRoom.user_session == session_id).first()
        if chatRoom is None:
            raise HTTPException(status_code=404, detail='chatRoom not found')
        else:
            raise HTTPException(status_code=404, detail='Answer does not exist')
    db.delete(deleted)
    db.commit()

# chatRoom sessionID, index 로 필터링 후 해당 질문 삭제하기
@router.delete("/{user_session}/{chat_session}/{chat_id}", status_code=status.HTTP_200_OK)
async def delete_chat(user_session: str, chat_session: str, chat_id: int, db: db_dependency):
    deleted = db.query(ChatAnswer).filter(
        and_(
            ChatAnswer.user_session == user_session,
            ChatAnswer.chat_session == chat_session,
            ChatAnswer.id == chat_id)
        ).first()
    if deleted is None:
        chatRoom = db.query(ChatRoom).filter(ChatRoom.user_session == session_id).first()
        if chatRoom is None:
            raise HTTPException(status_code=404, detail='chatRoom not found')
        else:
            raise HTTPException(status_code=404, detail= str(chat_id)+ ' Answer does not exist')
    db.delete(deleted)
    db.commit()
