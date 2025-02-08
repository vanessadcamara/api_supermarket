from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import uvicorn
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota raiz
@app.get("/")
def read_root():
    return JSONResponse(content={"message": "Supermarket Backend API is running!"})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
