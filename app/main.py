from fastapi import FastAPI
from app.api import endpoints
from app.models.models import Base
from app.db.session import engine

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is running"}

app.include_router(endpoints.router)
Base.metadata.create_all(bind=engine)
