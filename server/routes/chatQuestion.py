import sys
sys.path.append("update-chat-server/server")

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request, Response
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
@router.get("/{chatRoom_ID}", status_code=status.HTTP_200_OK)
async def get_Room_chatQuestion(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    chatQuestion = db.query(ChatQuestion).filter(
        and_(
            ChatQuestion.session_ID == session_ID,
            ChatQuestion.chatRoom_ID == chatRoom_ID)
        ).all()
    if len(chatQuestion) == 0:
        chatRoom = db.query(ChatRoom).filter(ChatRoom.session_ID == session_id).first()
        if chatRoom is None: 
            raise HTTPException(status_code=404, detail='chatRoom not found')
        else:
            raise HTTPException(status_code=404, detail='Question does not exist')
    return chatQuestion

# chatQuestion sessionID 로 필터링 후 해당 채팅방 특정 답변 받아오기
@router.get("/{chatRoom_ID}/{chat_id}", status_code=status.HTTP_200_OK)
async def get_Room_one_chatQuestion(chatRoom_ID: str, chat_id: int, request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    chatQuestion = db.query(ChatQuestion).filter(
        and_(
            ChatQuestion.session_ID == session_ID,
            ChatQuestion.chatRoom_ID == chatRoom_ID,
            ChatQuestion.id == chat_id)
        ).first()
    if chatQuestion is None:
        chatRoom = db.query(ChatRoom).filter(ChatRoom.session_ID == session_id).first()
        if chatRoom is None: 
            raise HTTPException(status_code=404, detail='chatRoom not found')
        else:
            raise HTTPException(status_code=404, detail='Question does not exist')
    return chatQuestion

# chatQuestion 생성하기
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chatQuestion(chatQuestion: ChatQuestionBase, db: db_dependency):
    db_chatQuestion = ChatQuestion(**chatQuestion.dict())
    db.add(db_chatQuestion)
    db.commit()
    
# # chatQuestion생성하기 -> 쿼리스트링으로 chatRoom_ID 만 받아 생성하는 방식
@router.post("/{chatRoom_ID}", status_code=status.HTTP_201_CREATED)
async def create_chatQuestion_ver2(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    new_chatQuestion = ChatQuestion(
        session_ID = session_ID,
        chatRoom_ID = chatRoom_ID,
    )
    db.add(new_chatQuestion)
    db.commit()

# chatRoom sessionID 로 필터링 후 해당 채팅방 전체 질문 삭제하기
@router.delete("/{chatRoom_ID}", status_code=status.HTTP_200_OK)
async def delete_Room_chatQuestion(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    deleted = db.query(ChatQuestion).filter(
        and_(
            ChatQuestion.session_ID == session_ID,
            ChatQuestion.chatRoom_ID == chatRoom_ID)
        ).all()
    if len(deleted) == 0:
        chatRoom = db.query(ChatRoom).filter(ChatRoom.session_ID == session_id).first()
        if chatRoom is None:
            raise HTTPException(status_code=404, detail='chatRoom not found')
        else:
            raise HTTPException(status_code=404, detail='Question does not exist')
    db.delete(deleted)
    db.commit()

# chatRoom sessionID, index 로 필터링 후 해당 질문 삭제하기
@router.delete("/{chatRoom_ID}/{chat_id}", status_code=status.HTTP_200_OK)
async def delete_Room_one_chatQuestion(chatRoom_ID: str, chat_id: int, request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    deleted = db.query(ChatQuestion).filter(
        and_(
            ChatQuestion.session_ID == session_ID,
            ChatQuestion.chatRoom_ID == chatRoom_ID,
            ChatQuestion.id == chat_id)
        ).first()
    if deleted is None:
        chatRoom = db.query(ChatRoom).filter(ChatRoom.session_ID == session_id).first()
        if chatRoom is None:
            raise HTTPException(status_code=404, detail='chatRoom not found')
        else:
            raise HTTPException(status_code=404, detail= str(chat_id)+ ' Question does not exist')
    db.delete(deleted)
    db.commit()

