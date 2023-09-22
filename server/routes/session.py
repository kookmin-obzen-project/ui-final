import sys
sys.path.append("update-chat-server/server")

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request
from pydantic import *
from db.model_session  import *
import uuid

app = FastAPI()
router = APIRouter()

@router.get("/", status_code=status.HTTP_201_CREATED)
async def create_session( db: db_dependency):
    session_expiration_time = 3600 # 초 단위, 3600 = 1시간, record expiration time = cookie expiration time
    
    user_session = str(uuid.uuid4())
    response = JSONResponse(content={"message": "Session ID set successfully"})
    response.set_cookie(key="session_id", value=user_session, max_age=session_expiration_time)
    
    db_session = Session()
    db_session.user_session = user_session
    db_session.expired_at = datetime.now() + timedelta(seconds=session_expiration_time)
    db.add(db_session)
    db.commit()
    
    return response
