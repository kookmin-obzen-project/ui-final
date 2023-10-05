import sys
sys.path.append("update-chat-server/server")

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request, Response
from pydantic import *
from routes.session import * 

from db.model_chatRoom  import *
import httpx
### query 문에서 .first() 는 object, .all() 은 list
### .first 는 is None, .all은 len() == 0

app = FastAPI()
router = APIRouter()

# chatRoom 테이블에 있는 데이터 가져오기
@router.get("/", status_code=status.HTTP_200_OK)
async  def get_all_chatRoom(request: Request, response: Response, db: db_dependency):
    chatRoom = db.query(ChatRoom).all()
    return chatRoom

# chatRoom 테이블 중 특정 user 의 chatRoom 다 가져오기
@router.get("/user", status_code=status.HTTP_200_OK)
async  def get_user_all_chatRoom(request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    chatRoom = db.query(ChatRoom).filter(ChatRoom.session_ID == session_ID).all()
    if len(chatRoom) == 0: 
        raise HTTPException(status_code=404, detail='chatRoom not found')
    return chatRoom

# chatRoom 테이블 중 특정 user 의 특정 chatRoom 정보만 가져오기
@router.get("/{chatRoom_ID}", status_code=status.HTTP_200_OK)
async  def get_one_chatRoom(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    chatRoom = db.query(ChatRoom).filter(
        and_(
            ChatRoom.session_ID == session_ID,
            ChatRoom.chatRoom_ID == chatRoom_ID)
        ).all()
    if len(chatRoom) == 0: 
        raise HTTPException(status_code=404, detail='chatRoom not found')
    return chatRoom
    
# chatRoom 생성하기 -> chatRoom 데이터를 받아 주입하는 방식
@router.post("/chatRoom_Base", status_code=status.HTTP_201_CREATED)
async def create_chatRoom(chatRoom: ChatRoomBase,request:Request, response:Response, db: db_dependency):
    new_chatRoom = ChatRoom(**chatRoom.dict())
    db.add(new_chatRoom)
    db.commit()

# chatRoom 생성하기 -> 쿼리스트링으로 chatRoom_ID, name 만 받아 생성하는 방식
@router.post("/{chatRoom_ID}/{name}", status_code=status.HTTP_201_CREATED)
async def create_chatRoom_ver2(chatRoom_ID: str, name: str ,request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    new_chatRoom = ChatRoom(
        session_ID = session_ID,
        chatRoom_ID = chatRoom_ID,
        name = name
    )
    db.add(new_chatRoom)
    db.commit()

# chatRoom sessionID 로 필터링 후 채팅방 삭제하기
@router.delete("/{chatRoom_ID}", status_code=status.HTTP_200_OK)
async def delete_one_chatRoom(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    deleted = db.query(ChatRoom).filter(
        and_(
            ChatRoom.session_ID == session_ID,
            ChatRoom.chatRoom_ID == chatRoom_ID)
        ).first()
    if deleted is None:
        raise HTTPException(status_code=404, detail='chatRoom not found')
    db.delete(deleted)
    db.commit()
    

# chatRoom sessionID 로 필터링 후 채팅방 이름 업데이트
@router.put("/{chatRoom_ID}/{name}", status_code=status.HTTP_200_OK)
async def update_name_chatRoom(chatRoom_ID: str, name: str, request:Request, response:Response, db: db_dependency):
    session_ID = await get_session(request, response, db)
    deleted = db.query(ChatRoom).filter(
        and_(
            ChatRoom.session_ID == session_ID,
            ChatRoom.chatRoom_ID == chatRoom_ID)
        ).first()
    if deleted is None:
        raise HTTPException(status_code=404, detail='chatRoom not found')
    deleted.name = name
    db.commit()
    