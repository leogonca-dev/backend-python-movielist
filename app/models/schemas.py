from pydantic import BaseModel
from typing import List

class ProducerInterval(BaseModel):
    producer: str
    interval: int
    previousWin: int
    followingWin: int

class AwardIntervals(BaseModel):
    min: List[ProducerInterval]
    max: List[ProducerInterval]
