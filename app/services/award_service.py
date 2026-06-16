from typing import List, Dict, Any
from collections import defaultdict
from app.repositories.producer_repository import ProducerRepository
from app.models.schemas import ProducerInterval, AwardIntervals

class AwardService:
    def __init__(self, producer_repository: ProducerRepository):
        self.producer_repository = producer_repository

    def calculate_award_intervals(self) -> AwardIntervals:
        winner_movies = self.producer_repository.get_winner_movies()

        producer_wins = defaultdict(list)
        for movie in winner_movies:
            producers = movie.producers.replace(" and ", ",").split(",")
            for producer in producers:
                producer = producer.strip()
                if producer:
                    producer_wins[producer].append(movie.year)
        
        min_intervals: List[ProducerInterval] = []
        max_intervals: List[ProducerInterval] = []
        
        overall_min_interval = float('inf')
        overall_max_interval = 0

        for producer, years in producer_wins.items():
            years.sort()
            if len(years) > 1:
                for i in range(len(years) - 1):
                    interval = years[i+1] - years[i]
                    
                    producer_interval = ProducerInterval(
                        producer=producer,
                        interval=interval,
                        previousWin=years[i],
                        followingWin=years[i+1]
                    )

                    if interval < overall_min_interval:
                        overall_min_interval = interval
                        min_intervals = [producer_interval]
                    elif interval == overall_min_interval:
                        min_intervals.append(producer_interval)
                    
                    if interval > overall_max_interval:
                        overall_max_interval = interval
                        max_intervals = [producer_interval]
                    elif interval == overall_max_interval:
                        max_intervals.append(producer_interval)
        
        return AwardIntervals(min=min_intervals, max=max_intervals)
