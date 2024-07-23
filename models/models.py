from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String
from db.database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
    Column("email", String, unique=True, index=True),
    Column("age", Integer),
)


# Pydantic модели для запросов и ответов
class UserCreate(BaseModel):
    name: str
    email: str
    age: int


class User(BaseModel):
    id: int
    name: str
    email: str
    age: int

    class Config:
        orm_mode = True
