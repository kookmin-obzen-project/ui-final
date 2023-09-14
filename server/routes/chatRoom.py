import sys
sys.path.append("update-chat-server/server")

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request
from pydantic import *

from db.model_chatRoom  import *

### query 문에서 .first() 는 object, .all() 은 list
### .first 는 is None, .all은 len() == 0

app = FastAPI()
router = APIRouter()

# chatRoom 테이블에 있는 데이터 가져오기
@router.get("/", status_code=status.HTTP_200_OK)
async  def get_all_chatRoom(db: db_dependency):
    chatRoom = db.query(ChatRoom).all()
    return chatRoom

# chatRoom 테이블 중 특정 user 의 chatRoom 다 가져오기
@router.get("/{user_session}", status_code=status.HTTP_200_OK)
async  def get_user_chatRoom(user_session: str, db: db_dependency):
    chatRoom = db.query(ChatRoom).filter(ChatRoom.user_session == user_session).all()
    if len(chatRoom) == 0: 
        raise HTTPException(status_code=404, detail='chatRoom not found')
    return chatRoom

# chatRoom 테이블 중 특정 user 의 특정 chatRoom 가져오기
@router.get("/{user_session}/{chat_session}", status_code=status.HTTP_200_OK)
async  def get_chatRoom(user_session: str, chat_session: str, db: db_dependency):
    chatRoom = db.query(ChatRoom).filter(
        and_(
            ChatRoom.user_session == user_session,
            ChatRoom.chat_session == chat_session)
        ).all()
    if len(chatRoom) == 0: 
        raise HTTPException(status_code=404, detail='chatRoom not found')
    return chatRoom

# chatRoom 생성하기
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chatRoom(chatRoom: ChatRoomBase, db: db_dependency):
    db_chatRoom = ChatRoom(**chatRoom.dict())
    db.add(db_chatRoom)
    db.commit()

# chatRoom sessionID 로 필터링 후 채팅방 삭제하기
@router.delete("/{user_session}/{chat_session}", status_code=status.HTTP_200_OK)
async def delete_chatRoom(user_session: str, chat_session: str, db: db_dependency):
    deleted = db.query(ChatRoom).filter(
        and_(
            ChatRoom.user_session == user_session,
            ChatRoom.chat_session == chat_session)
        ).first()
    if deleted is None:
        raise HTTPException(status_code=404, detail='chatRoom not found')
    db.delete(deleted)
    db.commit()
    

# chatRoom sessionID 로 필터링 후 채팅방 이름 업데이트
@router.put("/{user_session}/{chat_session}/{name}", status_code=status.HTTP_200_OK)
async def update_chatRoom_name(user_session: str, chat_session: str, name: str, db: db_dependency):
    deleted = db.query(ChatRoom).filter(
        and_(
            ChatRoom.user_session == user_session,
            ChatRoom.chat_session == chat_session)
        ).first()
    if deleted is None:
        raise HTTPException(status_code=404, detail='chatRoom not found')
    deleted.name = name
    db.commit()
    