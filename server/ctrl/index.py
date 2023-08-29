from fastapi import APIRouter
from fastapi import FastAPI
from .obzai import test

ctrl_router = APIRouter()
data = {
    "res": "a"
}

ai_model = test.obzai(**data)


@ctrl_router.get('/ctrl')
async def home():
    return {'msg': 'ctrl'}


@ctrl_router.post('/ctrl/text2sql')
async def home():
    res = await ai_model.funct_text2sql(nlq="안녕")
    return res


@ctrl_router.post('/ctrl/text2pvtable')
async def home():
    res = await ai_model.funct_text2pvtable(nlq="안녕", recall=True)
    return res
