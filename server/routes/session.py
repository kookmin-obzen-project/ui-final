import sys
sys.path.append("update-chat-server/server")

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request
from pydantic import *
from db.model_session  import *

app = FastAPI()
router = APIRouter()

### 여기서부터~~~ 고쳐봅시다 session 파트
# @router.post("/", status_code=status.HTTP_201_CREATED)
# async def create_session( db: db_dependency):
#     db_chatRoom = Session()
#     db.add(db_chatRoom)
#     db.commit()
    
    
#     def create_session(user_id: int, db: Session = Depends(SessionLocal)):
#     session_id = str(uuid4())
#     db_session = SessionModel(session_id=session_id, user_id=user_id)
#     db.add(db_session)
#     db.commit()
#     db.refresh(db_session)
#     return db_session