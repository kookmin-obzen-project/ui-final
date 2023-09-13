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

# chatQuestion 테이블에 있는 데이터 가져오기
@router.get("/", status_code=status.HTTP_200_OK)
async  def get_all_chatQuestion(db: db_dependency):
    chatQuestion = db.query(ChatQuestion).all()
    return chatQuestion


# chatQuestion sessionID 로 필터링 후 해당 채팅방 전체 답변 받아오기
@router.get("/{session_id}", status_code=status.HTTP_200_OK)
async def read_chatQuestion(session_id: str, db: db_dependency):
    chatQuestion = db.query(ChatQuestion).filter(ChatQuestion.chatRoom_session == session_id).all()
    if len(chatQuestion) == 0:
        raise HTTPException(status_code=404, detail='chatRoom`Question not found')
    return chatQuestion

# chatQuestion 생성하기
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chat(chatQuestion: ChatQuestionBase, db: db_dependency):
    db_chatQuestion = ChatQuestion(**chatQuestion.dict())
    db.add(db_chatQuestion)
    db.commit()

# chatRoom sessionID 로 필터링 후 해당 채팅방 전체 질문 삭제하기
@router.delete("/{session_id}", status_code=status.HTTP_200_OK)
async def delete_chat(session_id: str, db: db_dependency):
    deleted = db.query(ChatQuestion).filter(ChatQuestion.chatRoom_session == session_id).first()
    if deleted is None:
        raise HTTPException(status_code=404, detail='chat not found')
    db.delete(deleted)
    db.commit()
    
# chatRoom sessionID, index 로 필터링 후 해당 질문 삭제하기
@router.delete("/{session_id}/{chat_id}", status_code=status.HTTP_200_OK)
async def delete_chat(session_id: str, chat_id: int, db: db_dependency):
    deleted = db.query(ChatQuestion).filter(and_(ChatQuestion.chatRoom_session == session_id, ChatQuestion.id == chat_id)).first()
    if deleted is None:
        raise HTTPException(status_code=404, detail='Quesion not found')
    db.delete(deleted)
    db.commit()

