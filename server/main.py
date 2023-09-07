import sys
sys.path.append("update-chat-server/server")


from pydantic import *
from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from routes import chats
from db.model_chat import Chat
from db.db import *

app = FastAPI()
Chat.metadata.create_all(bind=engine)

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
#pp.include_router(router=ctrl_router)
