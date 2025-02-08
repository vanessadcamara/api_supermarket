from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
import uvicorn
from app.controllers import sales_router


app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(sales_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
