import sys
sys.path.append("update-chat-server/server")

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request, Response
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from pydantic import *
from db.model_session  import *
from routes.JSON_format import *
import uuid
import copy

app = FastAPI()
router = APIRouter()
session_expiration_time = 100000 # 초 단위, 3600 = 1시간, cookie에 있는 session 유지 시간.

# Session DB 에 담긴 모든 데이터 가져오기
@router.get("/", status_code=status.HTTP_200_OK)
async def get_cookie( db:db_dependency):
    all_cookies = db.query(Session).all()
    return JSON_format("Success, Get All Session Data", all_cookies)

# Session ID 를 생성하고, DB 에 저장
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_session(request:Request, response:Response, db: db_dependency):
    try:
        print(request.cookies)
        cookie = request.cookies["session_id"] # KeyError -> 애초에 session 이 없는 경우 -> create
        db_session = db.query(Session).filter(Session.session_ID == cookie).all() # ValueError -> DB 에만 없는 경우. DB 에 저장하면 됨.
        if len(db_session) == 0:
            raise ValueError("Session Id Found But Not Stored in DB, So Reset Your Session")
        
    except KeyError: 
        session_ID = str(uuid.uuid4())
        
        new_session = Session()
        new_session.session_ID = session_ID
        new_session.expired_at = datetime.now() + timedelta(seconds=session_expiration_time)
        new_session_copy = copy.deepcopy(new_session)
        db.add(new_session)
        db.commit()
        
        response.set_cookie(key="session_id", value=session_ID, max_age=session_expiration_time)
        return JSON_format("Success, Create Session", new_session_copy)
    
    except ValueError:
        session_ID = str(uuid.uuid4())
        
        new_session = Session()
        new_session.session_ID = session_ID
        new_session.expired_at = datetime.now() + timedelta(seconds=session_expiration_time)
        new_session_copy = copy.deepcopy(new_session)
        db.add(new_session)
        db.commit()
        
        response.set_cookie(key="session_id", value=session_ID, max_age=session_expiration_time)
        return JSON_format("Session Id Found But Not Stored in DB, So Reset Your Session", new_session_copy)
    
    else: 
        raise HTTPException(status_code=404, detail='Session can not create, already exist')
        
    
# Session DB 에 담긴 모든 데이터 삭제하기, user cookie 의 session_id 는 삭제하지 않습니다.
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(request:Request, db: db_dependency):
    all_session = db.query(Session).all()
    for deleted in all_session:
        db.delete(deleted)
    db.commit()
    print(request.cookies)
    return JSON_format("Success, Delete All Session Data")

# 접속한 user 의 session_id 가져오기, 만약 DB 에 없다면 user cookie 의 session_id 를 다시 세팅합니다.
@router.get("/session_id", status_code=status.HTTP_201_CREATED)
async def get_session(request: Request, response: Response, db: db_dependency):
    try:
        cookie = request.cookies["session_id"] # KeyError
        db_session = db.query(Session).filter(Session.session_ID == cookie).all() # ValueError
        if len(db_session) == 0:
            raise ValueError("already exist")
        return JSON_format("Success, Get Session ID", {"session_id":cookie})
    
    except ValueError:
        session_ID = str(uuid.uuid4())
        
        new_session = Session()
        new_session.session_ID = session_ID
        new_session.expired_at = datetime.now() + timedelta(seconds=session_expiration_time)
        new_session_copy = copy.deepcopy(new_session)
        db.add(new_session)
        db.commit()
        
        response.set_cookie(key="session_id", value=session_ID, max_age=session_expiration_time)
        return JSON_format("Session Id Found But Not Stored in DB, So Reset Your Session", new_session_copy)
    
    except KeyError:
        raise HTTPException(status_code=404, detail='Session Id Not Found')

    
@router.delete("/session_id", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session_cookie(request: Request, response: Response):
    try:
        response.delete_cookie("session_id")
    except :
        raise HTTPException(status_code=404, detail='Session Id Not Found')