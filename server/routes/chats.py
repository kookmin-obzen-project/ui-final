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

@router.get("/chatRoom", status_code=status.HTTP_200_OK)
async  def get_all_chats(db: db_dependency):
    chats = db.query(ChatRoom).all()
    return chats

@router.post("/chatRoom", status_code=status.HTTP_201_CREATED)
async def create_chat(chatRoom: ChatRoomBase, db: db_dependency):
    db_chatRoom = ChatRoom(**chatRoom.dict())
    db.add(db_chatRoom)
    db.commit()

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
    print("chat - sessionID: " + chat.sessionID)
    talk =  {
        'answer':chat.talk,
        }
    # 같은 채팅창일 경우 sessionID 가 같게 넘어옴
    return talk

# Cookie 를 적용했지만 작동 X -> local환경 등 코드 자체는 맞음
# @router.post("/reflect", status_code=status.HTTP_200_OK)
# async def reflect_chat(chat: ChatBase, db: db_dependency,request: Request):
#     session_id = request.cookies.get("sessionID")
#     print("Request - session_id")
#     print( session_id)
#     # 받은 채팅 정보를 그대로 반환
#     print("chat - sessionID: " + chat.sessionID)
#     text =  {
#         'answer':chat.text,
#         }
#     return text
