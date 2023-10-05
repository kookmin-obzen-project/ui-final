import sys
sys.path.append("update-chat-server/server")

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request, Response
from pydantic import *
from db.model_chat  import *
from db.model_chatRoom  import *
from db.model_chatAnswer  import *
from db.model_chatQuestion  import *
from fastapi import APIRouter, Request

# request:Request, response:Response,
# session_ID = await get_session(request, response, db)

app = FastAPI()
router = APIRouter()

# chatAnswer 테이블에 있는 데이터 가져오기
@router.get("/", status_code=status.HTTP_200_OK)
async  def get_all_chatAnswer(db: db_dependency):
    chatAnswer = db.query(ChatAnswer).all()
    return chatAnswer

# chatAnswer sessionID 로 필터링 후 해당 채팅방 전체 답변 받아오기
@router.get("/{chatRoom_ID}", status_code=status.HTTP_200_OK)
async def get_Room_chatAnswer(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    chatAnswer = db.query(ChatAnswer).filter(
        and_(
            ChatAnswer.session_ID == session_ID,
            ChatAnswer.chatRoom_ID == chatRoom_ID)
        ).all()
    if len(chatAnswer) == 0:
        chatRoom = db.query(ChatRoom).filter(ChatRoom.session_ID == session_id).first()
        if chatRoom is None: 
            raise HTTPException(status_code=404, detail='chatRoom not found')
        else:
            raise HTTPException(status_code=404, detail='Answer does not exist')
    return chatAnswer

# chatAnswer sessionID 로 필터링 후 해당 채팅방 특정 답변 받아오기
@router.get("/{chatRoom_ID}/{chat_id}", status_code=status.HTTP_200_OK)
async def get_Room_one_chatAnswer(chatRoom_ID: str, chat_id: int, request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    chatAnswer = db.query(ChatAnswer).filter(
        and_(
            ChatAnswer.session_ID == session_ID,
            ChatAnswer.chatRoom_ID == chatRoom_ID,
            ChatAnswer.id == chat_id)
        ).first()
    if chatAnswer is None:
        chatRoom = db.query(ChatRoom).filter(ChatRoom.session_ID == session_id).first()
        if chatRoom is None: 
            raise HTTPException(status_code=404, detail='chatRoom not found')
        else:
            raise HTTPException(status_code=404, detail='Answer does not exist')
    return chatAnswer

# chatAnswer 생성하기
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chatAnswer(chatAnswer: ChatAnswerBase, db: db_dependency):
    db_chatAnswer = ChatAnswer(**chatAnswer.dict())
    db.add(db_chatAnswer)
    db.commit()

# # chatAnswer생성하기 -> 쿼리스트링으로 chatRoom_ID 만 받아 생성하는 방식
@router.post("/{chatRoom_ID}", status_code=status.HTTP_201_CREATED)
async def create_chatAnswer_ver2(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    new_chatAnswer = ChatAnswer(
        session_ID = session_ID,
        chatRoom_ID = chatRoom_ID,
    )
    db.add(new_chatAnswer)
    db.commit()


# chatRoom sessionID 로 필터링 후 해당 채팅방 전체 질문 삭제하기
@router.delete("/{chatRoom_ID}", status_code=status.HTTP_200_OK)
async def delete_Room_chatAnswer(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    deleted = db.query(ChatAnswer).filter(
        and_(
            ChatAnswer.session_ID == session_ID,
            ChatAnswer.chatRoom_ID == chatRoom_ID)
        ).all()
    if len(deleted) == 0:
        chatRoom = db.query(ChatRoom).filter(ChatRoom.session_ID == session_id).first()
        if chatRoom is None:
            raise HTTPException(status_code=404, detail='chatRoom not found')
        else:
            raise HTTPException(status_code=404, detail='Answer does not exist')
    db.delete(deleted)
    db.commit()

# chatRoom sessionID, index 로 필터링 후 해당 질문 삭제하기
@router.delete("/{chatRoom_ID}/{chat_id}", status_code=status.HTTP_200_OK)
async def delete_Room_one_chatAnswer(chatRoom_ID: str, chat_id: int, request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    deleted = db.query(ChatAnswer).filter(
        and_(
            ChatAnswer.session_ID == session_ID,
            ChatAnswer.chatRoom_ID == chatRoom_ID,
            ChatAnswer.id == chat_id)
        ).first()
    if deleted is None:
        chatRoom = db.query(ChatRoom).filter(ChatRoom.session_ID == session_id).first()
        if chatRoom is None:
            raise HTTPException(status_code=404, detail='chatRoom not found')
        else:
            raise HTTPException(status_code=404, detail= str(chat_id)+ ' Answer does not exist')
    db.delete(deleted)
    db.commit()
