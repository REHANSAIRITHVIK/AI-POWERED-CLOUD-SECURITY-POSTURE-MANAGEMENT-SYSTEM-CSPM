# db.py
from sqlmodel import SQLModel, create_engine, Session
from typing import Optional

DATABASE_URL = "sqlite:///./cspm.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
