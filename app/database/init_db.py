import csv
import os
from sqlalchemy.orm import Session
from app.models.movie import Movie
from app.database.database import Base, engine
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    csv_file_path: str = "Movielist.csv"

settings = Settings()

def init_db(db: Session):
    Base.metadata.create_all(bind=engine)

    if db.query(Movie).count() == 0:
        csv_path = settings.csv_file_path
        if not os.path.exists(csv_path):
            print(f"Erro: Arquivo CSV não encontrado em {csv_path}")
            return

        with open(csv_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                # Validação básica de dados para garantir robustez
                try:
                    year_val = int(row['year'])
                except (ValueError, KeyError):
                    continue

                winner = True if row.get('winner', '').lower() == 'yes' else False
                
                # Normalização de produtores (removendo espaços extras e tratando múltiplos separadores)
                producers_raw = row.get('producers', '')
                
                movie = Movie(
                    year=year_val,
                    title=row.get('title', 'Untitled'),
                    studios=row.get('studios', ''),
                    producers=producers_raw,
                    winner=winner
                )
                db.add(movie)
            db.commit()
        print("Dados do CSV carregados com sucesso no banco de dados.")
