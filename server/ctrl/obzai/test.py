from pydantic import Field, BaseModel
from dotenv import load_dotenv
import os

# load .env
load_dotenv()

env_OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class obzai(BaseModel):
    res: str

    def get_obzai_data(self) -> object:
        data = {
            "res": self.res
        }
        return data

    async def funct_text2sql(self, nlq: str = None) -> object:
        res_dict = {
            "res": "text2sql"
        }
        return res_dict

    # recall==True -> 재호출, recall==False -> 처음 호출
    async def funct_text2pvtable(self, nlq: str = None, recall: bool = True) -> object:
        res_dict = {
            "params": {
                "key": "value"
            }
        }

        return res_dict["params"]
