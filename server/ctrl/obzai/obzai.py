from obzai.text2sql.gen_sql import text2sql
from pydantic import Field, BaseModel
from dotenv import load_dotenv
import os

# load .env
load_dotenv(".env_obzai")

env_OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class obzai_model(BaseModel):
    table_info: list[object] = None
    table_alias_info: list[str] = None  # alias만 빼낸 리스트 -> 필요시 함수화
    join_info: list[list]
    model: str
    version: int
    self_correction: str
    OPENAI_API_KEY: str = env_OPENAI_API_KEY
    db_type: str
    prev_messages: list[object] = None

    def get_obzai_data(self) -> object:
        data = {
            "table_info": self.table_info,
            "table_alias_info": self.table_alias_info,
            "join_info": self.join_info,
            "model": self.model,
            "version": self.version,
            "self_correction": self.self_correction,
            "OPENAI_API_KEY": None,
            "db_type": self.db_type,
            "prev_messages": self.prev_messages
        }
        return data

    async def funct_text2sql(self, nlq: str) -> object:
        res_dict = await text2sql(
            query=nlq,
            table_info=f'"tables": {str(self.table_info)}',
            join_info=f'"foreign_keys": {str(self.join_info)}',
            model_type=self.model,
            version=self.version,
            self_correction=self.self_correction,
            db_type=self.db_type,
            is_base64_encoded=False,
            openai_api_key=self.OPENAI_API_KEY,
        )
        return res_dict

    # recall==True -> 재호출, recall==False -> 처음 호출
    async def funct_text2pvtable(self, nlq: str, recall: bool) -> object:
        if bool:
            res_dict = await text2pvtable(
                query=nlq,
                prev_messages=self.prev_messages,
                model_type=self.model,
                openai_api_key=self.OPENAI_API_KEY,
            )
            return res_dict["params"]

        res_dict = await text2pvtable(
            query=nlq,
            table_info=self.table_alias_info,
            model_type=self.model,
            openai_api_key=self.OPENAI_API_KEY,
        )

        return res_dict["params"]
