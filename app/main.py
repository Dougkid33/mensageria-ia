from fastapi import FastAPI
from app.api import endpoints
from app.models.models import Base
from app.db.session import engine
from app.api.endpoints import router
import threading
from app.api.schedule import start_scheduler

app = FastAPI()

# Iniciar o agendador de tarefas em um thread separado para não bloquear o FastAPI
def start():
    thread = threading.Thread(target=start_scheduler)
    thread.daemon = True  # Torna o thread de fundo
    thread.start()

# Iniciar o agendador
start()

@app.get("/")
def read_root():
    return {"message": "API is running"}

app.include_router(endpoints.router)
Base.metadata.create_all(bind=engine)
