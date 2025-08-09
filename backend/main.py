# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, constr
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from db import engine, SessionLocal
from models import Base, Message
from typing import Annotated
from pydantic import BaseModel, constr

# Create tables on startup (simple demo)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Microservice Demo")

# allow Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ItemIn(BaseModel):
    text: Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=4000)]

class ItemOut(BaseModel):
    id: int
    message: str

@app.post("/items", response_model=ItemOut)
def create_item(item: ItemIn):
    # You can use ORM or a parameterized text query; both are safe.
    # Here’s ORM:
    db = SessionLocal()
    try:
        msg = Message(content=item.text)
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return ItemOut(id=msg.id, message="Saved")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        db.close()

# Optional: simple healthcheck
@app.get("/healthz")
def healthz():
    # Will fail if DB unreachable
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}