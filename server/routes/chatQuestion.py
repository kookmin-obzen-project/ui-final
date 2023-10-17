import sys
sys.path.append("update-chat-server/server")

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request, Response
from pydantic import *
from db.model_chat  import *
from db.model_chatRoom  import *
from db.model_chatAnswer  import *
from db.model_chatQuestion  import *
from routes.session import *
from routes.JSON_format import *
import json

app = FastAPI()
router = APIRouter()

# chatQuestion 테이블에 있는 데이터 가져오기
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_chatQuestion(db: db_dependency):
    chatQuestion = db.query(ChatQuestion).all()
    return JSON_format("Success, Get All chatQuestion", chatQuestion)

# chatQuestion sessionID 로 필터링 후 해당 채팅방 전체 질문 받아오기
@router.get("/{chatRoom_ID}", status_code=status.HTTP_200_OK)
async def get_Room_chatQuestion(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    try:
        chatQuestion = db.query(ChatQuestion).filter(
            and_(
                ChatQuestion.chatRoom_ID == chatRoom_ID)
            ).all()
        if len(chatQuestion) == 0:
            chatRoom = db.query(ChatRoom).all()
            if chatRoom is None: 
                raise HTTPException(status_code=404, detail='Not Found chatRoom')
            else:
                raise HTTPException(status_code=404, detail='Question does not exist')
        return JSON_format(f"Success, Get {chatRoom_ID} chatQuestion", chatQuestion)
    except TypeError: # get_session_id 가 제대로 작동 안할 경우
        raise HTTPException(status_code=404, detail='Not Found Your Session ID')

# chatQuestion sessionID 로 필터링 후 해당 채팅방 특정 질문 받아오기
@router.get("/{chatRoom_ID}/{chat_id}", status_code=status.HTTP_200_OK)
async def get_Room_one_chatQuestion(chatRoom_ID: str, chat_id: int, request:Request, response:Response, db: db_dependency):
    try:
        chatQuestion = db.query(ChatQuestion).filter(
            and_(
                ChatQuestion.chatRoom_ID == chatRoom_ID,
                ChatQuestion.id == chat_id)
            ).first()
        if chatQuestion is None:
            chatRoom = db.query(ChatRoom).all()
            if chatRoom is None: 
                raise HTTPException(status_code=404, detail='chatRoom not found')
            else:
                raise HTTPException(status_code=404, detail='Question does not exist')
        return JSON_format(f"Success, Get {chatRoom_ID}-{chat_id} chatQuestion", chatQuestion)
    except TypeError: # get_session_id 가 제대로 작동 안할 경우
        raise HTTPException(status_code=404, detail='Not Found Your Session ID')
    
# chatQuestion 생성 & text 추가 - 사용 중
@router.post("/new/{chatRoom_ID}", status_code=status.HTTP_201_CREATED)
async def create_chatQuestion_ver2_new(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    try:
        request_body = await request.body()
        json_data = json.loads(request_body)
        text = json_data["text"]

        new_chatQuestion = ChatQuestion(
            chatRoom_ID = chatRoom_ID,
            text = text
        )
        
        db.add(new_chatQuestion)
        db.commit()
        return JSON_format("Success, Create chatQuestion", 
                        {"chatRoom_ID": chatRoom_ID,
                            "chat_id": new_chatQuestion.id, "text": text})
    except TypeError: # get_session_id 가 제대로 작동 안할 경우
        raise HTTPException(status_code=404, detail='Not Found Your Session ID')

# chatQuestion 생성하기
@router.post("/chatQuestion_Base", status_code=status.HTTP_201_CREATED)
async def create_chatQuestion(chatQuestion: ChatQuestionBase, db: db_dependency):
    try:
        new_chatQuestion = ChatQuestion(**chatQuestion.dict())
        db.add(new_chatQuestion)
        db.commit()
        return JSON_format("Success, Create chatQuestion", 
                        {"chatRoom_ID": new_chatQuestion.chatRoom_ID,
                            "chat_id": new_chatQuestion.id})
    except TypeError: # get_session_id 가 제대로 작동 안할 경우
        raise HTTPException(status_code=404, detail='Not Found Your Session ID')
    
# # chatQuestion 생성하기_ver2 -> 쿼리스트링으로 chatRoom_ID 만 받아 생성하는 방식
@router.post("/{chatRoom_ID}", status_code=status.HTTP_201_CREATED)
async def create_chatQuestion_ver2(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    try:
        new_chatQuestion = ChatQuestion(
            chatRoom_ID = chatRoom_ID,
        )
        db.add(new_chatQuestion)
        db.commit()
        return JSON_format("Success, Create chatQuestion", 
                        {"chatRoom_ID": chatRoom_ID,
                            "chat_id": new_chatQuestion.id})
    except TypeError: # get_session_id 가 제대로 작동 안할 경우
        raise HTTPException(status_code=404, detail='Not Found Your Session ID')

# chatRoom sessionID 로 필터링 후 해당 채팅방 전체 질문 삭제하기
@router.delete("/{chatRoom_ID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_Room_chatQuestion(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    try:
        All_chatQuestion = db.query(ChatQuestion).filter(
            and_(
                ChatQuestion.chatRoom_ID == chatRoom_ID)
            ).all()
        if len(All_chatQuestion) == 0:
            chatRoom = db.query(ChatRoom).all()
            if chatRoom is None:
                raise HTTPException(status_code=404, detail='chatRoom not found')
            else:
                raise HTTPException(status_code=404, detail='Question does not exist')
        for deleted in All_chatQuestion:
            db.delete(deleted)
        db.commit()
        return JSON_format(f"Success, Delete {chatRoom_ID} chatQuestion", 
                           {"chatRoom_ID": chatRoom_ID})
    except TypeError: # get_session_id 가 제대로 작동 안할 경우
        raise HTTPException(status_code=404, detail='Not Found Your Session ID')
    
# chatRoom sessionID, index 로 필터링 후 해당 질문 삭제하기
@router.delete("/{chatRoom_ID}/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_Room_one_chatQuestion(chatRoom_ID: str, chat_id: int, request:Request, response:Response, db: db_dependency):
    try:
        deleted = db.query(ChatQuestion).filter(
            and_(
                ChatQuestion.chatRoom_ID == chatRoom_ID,
                ChatQuestion.id == chat_id)
            ).first()
        if deleted is None:
            chatRoom = db.query(ChatRoom).all()
            if chatRoom is None:
                raise HTTPException(status_code=404, detail='chatRoom not found')
            else:
                raise HTTPException(status_code=404, detail= str(chat_id)+ ' Question does not exist')
        db.delete(deleted)
        db.commit()
        return JSON_format(f"Success, Delete {chatRoom_ID}-{chat_id} chatQuestion", {
                            "chatRoom_ID": chatRoom_ID,
                            "chat_id": chat_id})
    except TypeError: # get_session_id 가 제대로 작동 안할 경우
        raise HTTPException(status_code=404, detail='Not Found Your Session ID')

# text 업데이트
@router.put("/{chatRoom_ID}/{chat_id}", status_code=status.HTTP_200_OK)
async def update_text(chatRoom_ID: str, chat_id: int, request:Request, response:Response, db: db_dependency):
    try:
        request_json = await request.json()
        text = request_json["text"]

        updated= db.query(ChatQuestion).filter(
            and_(
                ChatQuestion.chatRoom_ID == chatRoom_ID,
                ChatQuestion.id == chat_id)
            ).first()
        if updated is None:
            raise HTTPException(status_code=404, detail='chatQuestion not found')
        updated.text = text
        db.commit()
        return JSON_format(f"Success, Update chatQuestion text", 
                           {
                            "chatRoom_ID": chatRoom_ID, 
                            "chat_id": chat_id, 
                            "text": text})
    except TypeError: # get_session_id 가 제대로 작동 안할 경우
        raise HTTPException(status_code=404, detail='Not Found Your Session ID')