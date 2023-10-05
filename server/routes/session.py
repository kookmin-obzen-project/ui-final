import sys
sys.path.append("update-chat-server/server")

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request, Response
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from pydantic import *
from db.model_session  import *
import uuid

app = FastAPI()
router = APIRouter()
session_expiration_time = 100000 # 초 단위, 3600 = 1시간, cookie에 있는 session 유지 시간.

# Session DB 에 담긴 모든 데이터 가져오기
@router.get("/", status_code=status.HTTP_201_CREATED)
async def get_cookie( db:db_dependency):
    all_cookies = db.query(Session).all()
    return all_cookies

# Session ID 를 생성하고, DB 에 저장
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_session(request:Request, db: db_dependency):
    try:
        cookie = request.cookies["session_id"]
        db_session = db.query(Session).filter(Session.session_ID == cookie).all()
        if len(db_session) != 0:
            raise ValueError("already exist")
        
    except KeyError: 
        session_ID = str(uuid.uuid4())
        response = JSONResponse(content={"message": "Session ID create successfully"})
        response.set_cookie(key="session_id", value=session_ID, max_age=session_expiration_time)
        
        db_session = Session()
        db_session.session_ID = session_ID
        db_session.expired_at = datetime.now() + timedelta(seconds=session_expiration_time)
        db.add(db_session)
        db.commit()
        return response
    
    except ValueError:
        raise HTTPException(status_code=404, detail='Session can not create, already exist')
    
    else: 
        response = JSONResponse(content={"message": "Session ID save successfully"})
        db_session = Session()
        db_session.session_ID = cookie
        db_session.expired_at = datetime.now() + timedelta(seconds=session_expiration_time)
        db.add(db_session)
        db.commit()
        return response
    
# Session DB 에 담긴 모든 데이터 삭제하기
@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_session(db: db_dependency):
    all_cookie = db.query(Session).all()
    for deleted in all_cookie:
        db.delete(deleted)
    db.commit()
    return JSONResponse(content={"message": "Delete all Session record"})

# 접속한 user 의 session_id 가져오기, 만약 DB 에 없다면 Exception 발생
@router.get("/session_id", status_code=status.HTTP_201_CREATED)
async def get_session(request: Request, response: Response, db: db_dependency):
    try:
        cookie = request.cookies["session_id"]
        db_session = db.query(Session).filter(Session.session_ID == cookie).all()
        if len(db_session) == 0:
            raise ValueError("already exist")
        return cookie
    except ValueError:
        response.delete_cookie("session_id")
        raise HTTPException(status_code=404, detail='Session Id Found But Not Save DB, So Delete Your Session')
    except KeyError:
        raise HTTPException(status_code=404, detail='Session Id Not Found')
    
def get_session_ID(request: Request):
    try: 
        cookie = request.cookies["session_id"]
        return cookie
    except : 
        raise HTTPException(status_code=404, detaul="Session Id Not Found")