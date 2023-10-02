import sys
sys.path.append("update-chat-server/server")

import subprocess
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from routes import chats, chatAnswer, chatQuestion, chatRoom, session
from db.model_chatRoom import *
from db.model_chatQuestion import *
from db.model_chatAnswer import *
from db.model_chat import *
from db.model_session import *
from db.db import *
from db import scheduler

app = FastAPI()
Chat.metadata.create_all(bind=engine)
ChatAnswer.metadata.create_all(bind=engine)
ChatQuestion.metadata.create_all(bind=engine)
ChatRoom.metadata.create_all(bind=engine)
Session.metadata.create_all(bind=engine)

origins = [
     # "http://localhost:3000",
     "*",
 ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#from ctrl import index

#ctrl_router = index.ctrl_router


@app.get('/')
async def home():
    
    return {'msg': 'main.py'}

app.include_router(chats.router, prefix="/chats")
app.include_router(chatRoom.router, prefix="/chatRoom")
app.include_router(chatAnswer.router, prefix="/chatAnswer")
app.include_router(chatQuestion.router, prefix="/chatQuestion")
app.include_router(session.router, prefix="/session")

