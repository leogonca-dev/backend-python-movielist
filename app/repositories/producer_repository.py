from sqlalchemy.orm import Session
from app.models.movie import Movie
from typing import List, Dict, Any

class ProducerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_winner_movies(self) -> List[Movie]:
        return self.db.query(Movie).filter(Movie.winner == True).order_by(Movie.year).all()
