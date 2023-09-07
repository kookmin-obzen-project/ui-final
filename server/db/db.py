import sys
sys.path.append("update-chat-server/server")

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os


load_dotenv("db/.env_db")
DB_URL = os.environ.get("DB_URL")


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
