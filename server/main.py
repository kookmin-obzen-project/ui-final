from fastapi import FastAPI
from pydantic import *
from ctrl import index

app = FastAPI()
ctrl_router = index.ctrl_router


@app.get('/')
async def home():
    return {'msg': 'main.py'}

app.include_router(router=ctrl_router)
