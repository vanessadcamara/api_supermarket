from fastapi import FastAPI
import uvicorn
from app.controllers import sales_router
from app.jobs.refresh_materialized_view import start_scheduler
app = FastAPI()
start_scheduler()

app.include_router(sales_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
