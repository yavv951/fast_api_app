import sqlite3

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select
from pydantic import BaseModel
from models import users
from database import engine, metadata

# Создаем приложение FastAPI
app = FastAPI()

# Настройка базы данных
metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

# Dependency для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Добро пожаловать на тестовый микросервис"}

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    query = users.insert().values(name=user.name, email=user.email, age=user.age)
    result = db.execute(query)
    db.commit()
    user_id = result.inserted_primary_key[0]
    return {**user.model_dump(), "id": user_id}


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    query = users.select().where(users.c.id == user_id)
    result = db.execute(query).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(result._mapping)


@app.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = select(users).offset(skip).limit(limit)
    result = db.execute(query).fetchall()
    # Преобразование результатов в список словарей
    return [dict(row._mapping) for row in result]


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    query = users.update().where(users.c.id == user_id).values(name=user.name, email=user.email, age=user.age)
    db.execute(query)
    db.commit()
    return {**user.model_dump(), "id": user_id}


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    query = users.delete().where(users.c.id == user_id)
    db.execute(query)
    db.commit()
    return {"message": "User deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)