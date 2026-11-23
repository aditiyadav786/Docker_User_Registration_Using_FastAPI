from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Docker User Management System")

DATABASE_URL = "postgresql://admin:admin123@db:5432/UserDetails"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


Base.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


@app.get("/")
def home():
    return {"message": "User Management System is running"}


@app.post("/users/register")
def register_user(user: UserCreate):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == user.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email
            }
        }
    finally:
        db.close()


@app.get("/users")
def get_users():
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()


@app.get("/users/{user_id}")
def get_user(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    finally:
        db.close()


@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: UserUpdate):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.first_name = updated_user.first_name
        user.last_name = updated_user.last_name
        user.email = updated_user.email

        db.commit()
        db.refresh(user)
        return {"message": "User updated successfully", "user": user}
    finally:
        db.close()


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    finally:
        db.close()