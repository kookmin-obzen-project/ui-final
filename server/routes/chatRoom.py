import sys
sys.path.append("update-chat-server/server")

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from pydantic import *

from db.model_chatRoom  import *

from fastapi import APIRouter, Request

### query 문에서 .first() 는 object, .all() 은 list
### .first 는 is None, .all은 len() == 0

app = FastAPI()
router = APIRouter()

# chatRoom 테이블에 있는 데이터 가져오기
@router.get("/", status_code=status.HTTP_200_OK)
async  def get_all_chatRoom(db: db_dependency):
    chatRoom = db.query(ChatRoom).all()
    return chatRoom


# chatRoom sessionID 로 필터링 후 해당 채팅방 전체 답변 받아오기
@router.get("/{session_id}", status_code=status.HTTP_200_OK)
async def read_chatRoom(session_id: str, db: db_dependency):
    chatRoom = db.query(ChatRoom).filter(ChatRoom.user_session == session_id).all()
    if len(chatRoom) == 0:
        raise HTTPException(status_code=404, detail='chatRoom not found')
    
    return chatRoom

# chatRoom 생성하기
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chat(chatRoom: ChatRoomBase, db: db_dependency):
    db_chatRoom = ChatRoom(**chatRoom.dict())
    db.add(db_chatRoom)
    db.commit()

# chatRoom sessionID 로 필터링 후 채팅방 삭제하기
@router.delete("/{session_id}", status_code=status.HTTP_200_OK)
async def delete_chat(session_id: str, db: db_dependency):
    deleted = db.query(ChatRoom).filter(ChatRoom.user_session == session_id).first()
    if deleted is None:
        raise HTTPException(status_code=404, detail='chatRoom not found')
    db.delete(deleted)
    db.commit()
    


# chatRoom sessionID 로 필터링 후 채팅방 이름 업데이트
@router.put("/{session_id}/{name}", status_code=status.HTTP_200_OK)
async def delete_chat(session_id: str, name: str, db: db_dependency):
    deleted = db.query(ChatRoom).filter(ChatRoom.user_session == session_id).first()
    deleted.name = name
    if deleted is None:
        raise HTTPException(status_code=404, detail='chatRoom not found')
    db.commit()
    