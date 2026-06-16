import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.database.database import Base, get_db
import os

# Configuração de banco de dados para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db_integration.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

from app.database.init_db import init_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    init_db(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

def test_get_award_intervals():
    response = client.get("/awards/intervals")
    assert response.status_code == 200
    data = response.json()
    
    assert "min" in data
    assert "max" in data
    assert isinstance(data["min"], list)
    assert isinstance(data["max"], list)
    
    # Valida estrutura dos dados retornados
    if len(data["min"]) > 0:
        item = data["min"][0]
        assert "producer" in item
        assert "interval" in item
        assert "previousWin" in item
        assert "followingWin" in item
        assert item["interval"] == item["followingWin"] - item["previousWin"]

def test_data_integrity():
    # Este teste garante que os dados foram carregados corretamente do CSV original
    response = client.get("/awards/intervals")
    assert response.status_code == 200
    data = response.json()
    
    # Com base no CSV original, podemos validar alguns resultados esperados
    # Exemplo: Se soubermos que o intervalo mínimo é 1, podemos validar isso
    # Como o requisito diz que será testado com outros dados, o foco é na estrutura e lógica
    assert len(data["min"]) >= 1
    assert len(data["max"]) >= 1
