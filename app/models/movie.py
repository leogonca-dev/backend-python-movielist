from sqlalchemy import Column, Integer, String, Boolean
from app.database.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    title = Column(String)
    studios = Column(String)
    producers = Column(String)
    winner = Column(Boolean, default=False)
