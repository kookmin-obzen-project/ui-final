import sys
sys.path.append("update-chat-server/server")

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from pydantic import *
from db.model_session  import *
import uuid

app = FastAPI()
router = APIRouter()

@router.get("/", status_code=status.HTTP_201_CREATED)
async def create_session( db: db_dependency):
    session_expiration_time = 30 # 초 단위, 3600 = 1시간, record expiration time = cookie expiration time
    
    user_session = str(uuid.uuid4())
    response = JSONResponse(content={"message": "Session ID set successfully"})
    response.set_cookie(key="session_id", value=user_session, max_age=session_expiration_time)
    
    db_session = Session()
    db_session.user_session = user_session
    db_session.expired_at = datetime.now() + timedelta(seconds=session_expiration_time)
    db.add(db_session)
    db.commit()
    return db_session.expired_at
    

@router.get("/cookie", status_code=status.HTTP_201_CREATED)
async def get_cookie( request: Request):
    all_cookies = request.cookies
    
    return all_cookies

@router.get("/all_cookie", status_code=status.HTTP_201_CREATED)
async def get_cookie( db:db_dependency):
    all_cookies = db.query(Session).all()
    print(db)
    return all_cookies

@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_session(db: db_dependency):
    all_cookie = db.query(Session).all()
    for deleted in all_cookie:
        db.delete(deleted)
    db.commit()
    
