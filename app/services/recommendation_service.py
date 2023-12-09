from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from typing import List
from app.models.recommendation import Recommendation
from app.repositories.recommendation_repo import RecommendationRepo


class RecommendationService:
    recommendation_repo: RecommendationRepo

    def __init__(self, rec_repo: RecommendationRepo = Depends(RecommendationRepo)) -> None:
        self.recommendation_repo = rec_repo

    def get_recommendations_for_user(self, user_id: UUID) -> List[Recommendation]:
        return self.recommendation_repo.get_recommendations_for_user(user_id)

    def create_recommendation(self, user_id: UUID, recommended_book_id: UUID) -> Recommendation:
        return self.recommendation_repo.create_recommendation(book_id=recommended_book_id, user_id=user_id)

    def remove_recommendation(self, recommendation_id: UUID) -> None:
        self.recommendation_repo.remove_recommendation(recommendation_id)
