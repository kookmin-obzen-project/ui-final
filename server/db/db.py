import pymysql
from dotenv import load_dotenv
import os


load_dotenv(".env_db")

env_host = os.getenv('db_host')
env_password = os.getenv('password')
connect = pymysql.connect(host=env_host, user="root",
                          password=env_password, db="obzen_test", charset="utf8")

cur = connect.cursor()
sql = "SELECT * FROM CHANNEL"
cur.execute(sql)
result = cur.fetchall()
print(result)

connect.close()
