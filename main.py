from fastapi import FastAPI, Depends
from app.database.database import engine, SessionLocal, Base, get_db
from app.database.init_db import init_db
from app.api import endpoints
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    csv_file_path: str = "Movielist.csv"

settings = Settings()

app = FastAPI(
    title="Golden Raspberry Awards API",
    description="API para identificar produtores com maior e menor intervalo de prêmios."
)

@app.on_event("startup")
def on_startup():
    # Garante que o diretório do CSV existe, se for um caminho relativo
    if not os.path.isabs(settings.csv_file_path):
        settings.csv_file_path = os.path.join(os.getcwd(), settings.csv_file_path)
    
    # Inicializa o banco de dados e carrega os dados do CSV
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

app.include_router(endpoints.router)

