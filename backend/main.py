from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import os
os.makedirs("data", exist_ok=True)

DATABASE_URL = "sqlite:///./data/dogs.db"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ DATABASE MODEL ------------------

class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    breed = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    behavior = Column(String)
    diet = Column(Text)
    conditions = Column(Text)
    medications = Column(Text)
    notes = Column(Text)
    owner_name = Column(String)
    owner_phone = Column(String)
    owner_email = Column(String)

Base.metadata.create_all(bind=engine)

# ------------------ SCHEMA ------------------

class DogCreate(BaseModel):
    name: str
    breed: str
    age: int | None = None
    weight: float | None = None
    behavior: str | None = None
    diet: str | None = None
    conditions: str | None = None
    medications: str | None = None
    notes: str | None = None
    owner_name: str
    owner_phone: str
    owner_email: str | None = None

# ------------------ API ------------------

@app.post("/dogs")
def create_dog(dog: DogCreate):
    db = SessionLocal()
    new_dog = Dog(**dog.dict())
    db.add(new_dog)
    db.commit()
    db.refresh(new_dog)
    db.close()
    return {"status": "ok", "id": new_dog.id}
