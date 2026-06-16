from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.repositories.producer_repository import ProducerRepository
from app.services.award_service import AwardService
from app.models.schemas import AwardIntervals

router = APIRouter()

@router.get("/awards/intervals", response_model=AwardIntervals)
def get_award_intervals(db: Session = Depends(get_db)):
    producer_repo = ProducerRepository(db)
    award_service = AwardService(producer_repo)
    return award_service.calculate_award_intervals()
