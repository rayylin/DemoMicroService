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


# main.py (add near the top with other imports)
from typing import Any, Optional
import requests
from fastapi import FastAPI, HTTPException

# ...

def getHkCmpInfo(cmp_name: str) -> Optional[dict[str, Any]]:
    url = "https://data.cr.gov.hk/cr/api/api/v1/api_builder/json/local/search"
    params = {
        "query[0][key1]": "Comp_name",
        "query[0][key2]": "begins_with",
        "query[0][key3]": cmp_name,
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        # 502 Bad Gateway makes sense for upstream issues
        raise HTTPException(status_code=502, detail=f"Upstream error: {e}")

    data = r.json()
    if data and isinstance(data, list):
        dic = data[0]
        dic["CompanySource"] = "TW"  # keep your original behavior
        return dic
    return None

# Add a new GET endpoint (query param: ?name=...)
@app.get("/hk/company", response_model=dict[str, Any] | None)
def hk_company(name: str):
    info = getHkCmpInfo(name)
    if info is None:
        # 404 if nothing found
        raise HTTPException(status_code=404, detail="Company not found")
    return info