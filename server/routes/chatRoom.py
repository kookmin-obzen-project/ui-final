import sys
sys.path.append("update-chat-server/server")

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request, Response
from pydantic import *
from routes.session import * 
from routes.JSON_format import *
from db.model_chatRoom  import *
import uuid
import copy
import httpx
### query 문에서 .first() 는 object, .all() 은 list
### .first 는 is None, .all은 len() == 0

app = FastAPI()
router = APIRouter()

# chatRoom 테이블에 있는 데이터 가져오기
@router.get("/", status_code=status.HTTP_200_OK)
async  def get_all_chatRoom(request: Request, response: Response, db: db_dependency):
    chatRoom = db.query(ChatRoom).all()
    return JSON_format("Success, Get All chatRoom", chatRoom)

# chatRoom 테이블 중 특정 user 의 chatRoom 다 가져오기
@router.get("/user", status_code=status.HTTP_200_OK)
async  def get_user_all_chatRoom(request:Request, response:Response, db: db_dependency):
    chatRoom = db.query(ChatRoom).all()
    return JSON_format("Success, Get All chatRoom", chatRoom)

# chatRoom 테이블 중 특정 user 의 특정 chatRoom 정보만 가져오기
@router.get("/{chatRoom_ID}", status_code=status.HTTP_200_OK)
async  def get_one_chatRoom(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    try:
        chatRoom = db.query(ChatRoom).filter(
            and_(
                ChatRoom.chatRoom_ID == chatRoom_ID)
            ).all()
        if len(chatRoom) == 0: 
            raise HTTPException(status_code=404, detail=f'Not Found chatRoom ID: {chatRoom_ID}')
        return JSON_format(f"Success, Get User's one chatRoom", chatRoom)
    except TypeError: 
        raise HTTPException(status_code=404, detail='Not Found Your Session ID')

# chatRoom 생성하기_ver0 -> 랜덤 ID 주입하여 생성하는 방식
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chatRoom_ver0(request:Request, response:Response, db: db_dependency):
    try: 
        chatRoom_ID = str(uuid.uuid4())
        new_chatRoom = ChatRoom(
            chatRoom_ID = chatRoom_ID,
        )
        db.add(new_chatRoom)
        db.commit()
        return JSON_format("Success, Create chatRoom", 
                           { "chatRoom_ID": chatRoom_ID} )
    except TypeError: # get_session_id 가 제대로 작동 안할 경우
        raise HTTPException(status_code=404, detail='Not Found Your Session ID')
    
# chatRoom 생성하기_ver1 -> chatRoom 데이터를 받아 주입하는 방식
@router.post("/chatRoom_Base", status_code=status.HTTP_201_CREATED)
async def create_chatRoom_ver1(chatRoom: ChatRoomBase,request:Request, response:Response, db: db_dependency):
    # session_ID or chatRoom_ID 가 누락된다면, error 발생x, 아래와 같은 형식으로 return 된다.
    # "detail": [
    #     {
    #         "type": "missing",
    #         "loc": [
    #             "body",
    #             "chatRoom_ID"
    #         ],
    #         "msg": "Field required",
    #         "input": {
    #             "session_ID": "user_session"
    #         },
    #         "url": "https://errors.pydantic.dev/2.3/v/missing"
    #     }
    # ]
    new_chatRoom = ChatRoom(**chatRoom.dict())
    if  db.query(ChatRoom).filter(and_(
                ChatRoom.chatRoom_ID == new_chatRoom.chatRoom_ID)
            ).all(): 
        raise HTTPException(status_code=404, detail=f'chatRoom_ID: {new_chatRoom.chatRoom_ID} already exists')
    db.add(new_chatRoom)
    db.commit()
    return JSON_format("Success, Create chatRoom", 
                       {"chatRoom_ID": new_chatRoom.chatRoom_ID})

    
# chatRoom 생성하기_ver2 -> 쿼리스트링으로 chatRoom_ID 만 받아 생성하는 방식
@router.post("/{chatRoom_ID}", status_code=status.HTTP_201_CREATED)
async def create_chatRoom_ver2(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    try: 
        if  db.query(ChatRoom).filter(and_(
                ChatRoom.chatRoom_ID == chatRoom_ID)
            ).all(): 
            raise HTTPException(status_code=404, detail=f'chatRoom_ID: {chatRoom_ID} already exists')
        new_chatRoom = ChatRoom(
            chatRoom_ID = chatRoom_ID,
        )
        db.add(new_chatRoom)
        db.commit()
        return JSON_format("Success, Create chatRoom", 
                           {"chatRoom_ID": chatRoom_ID} )
    except TypeError: # get_session_id 가 제대로 작동 안할 경우
        raise HTTPException(status_code=404, detail='Not Found Your Session ID')

# chatRoom 생성하기_ver3 -> 쿼리스트링으로 chatRoom_ID, name 을 받아 생성하는 방식
@router.post("/{chatRoom_ID}/{name}", status_code=status.HTTP_201_CREATED)
async def create_chatRoom_ver3(chatRoom_ID: str, name: str, request:Request, response:Response, db: db_dependency):
    try:
        if  db.query(ChatRoom).filter(and_(
                ChatRoom.chatRoom_ID == chatRoom_ID)
            ).all(): 
            raise HTTPException(status_code=404, detail=f'chatRoom_ID: {chatRoom_ID} already exists')
        new_chatRoom = ChatRoom(
            chatRoom_ID = chatRoom_ID,
            name = name
        )
        db.add(new_chatRoom)
        db.commit()
        return JSON_format("Success, Create chatRoom", 
                           {"chatRoom_ID": chatRoom_ID, 
                            "name":name} )
    except TypeError: # get_session_id 가 제대로 작동 안할 경우
        raise HTTPException(status_code=404, detail='Not Found Your Session ID')
    
# chatRoom 전체 채팅방 삭제하기
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_All_chatRoom(request:Request, response:Response, db: db_dependency):
    all_chatRoom = db.query(ChatRoom).all()
    for deleted in all_chatRoom:
        db.delete(deleted)
    db.commit()
    return JSON_format("Success, Delete All chatRoom Data")
        

# chatRoom sessionID 로 필터링 후 채팅방 삭제하기
@router.delete("/{chatRoom_ID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_one_chatRoom(chatRoom_ID: str, request:Request, response:Response, db: db_dependency):
    try:
        deleted = db.query(ChatRoom).filter(
            and_(
                ChatRoom.chatRoom_ID == chatRoom_ID)
            ).first()
        if deleted is None:
            raise HTTPException(status_code=404, detail='chatRoom not found')
        db.delete(deleted)
        db.commit()
        return JSON_format(f"Success, Delete {chatRoom_ID} chatRoom", 
                           {"chatRoom_ID": chatRoom_ID})
    except TypeError: # get_session_id 가 제대로 작동 안할 경우
        raise HTTPException(status_code=404, detail='Not Found Your Session ID')
    
# chatRoom sessionID 로 필터링 후 채팅방 이름 업데이트
@router.put("/{chatRoom_ID}/{new_name}", status_code=status.HTTP_200_OK)
async def update_name_chatRoom(chatRoom_ID: str, new_name: str, request:Request, response:Response, db: db_dependency):
    try:
        updated= db.query(ChatRoom).filter(
            and_(
                ChatRoom.chatRoom_ID == chatRoom_ID)
            ).first()
        old_name = updated.name
        if updated is None:
            raise HTTPException(status_code=404, detail='chatRoom not found')
        updated.name = new_name
        db.commit()
        return JSON_format(f"Success, Update chatRoom name, {old_name} -> {new_name}", 
                           {"chatRoom_ID": chatRoom_ID, 
                            "old name": old_name, 
                            "new_name": new_name})
    except TypeError: # get_session_id 가 제대로 작동 안할 경우
        raise HTTPException(status_code=404, detail='Not Found Your Session ID')