import uuid
from uuid import UUID
from typing import List

from app.models.book import Book
from app.models.recommendation import Recommendation
from app.models.user import User


class RecommendationRepo:
    recommendations: List[Recommendation] = []

    def get_recommendations_for_user(self, user_id: UUID) -> List[Recommendation]:
        return [rec for rec in self.recommendations if rec.user_id == user_id]

    def create_recommendation(self, book_id: UUID, user_id: UUID) -> Recommendation:
        recommendation = Recommendation(id=uuid.uuid4(), user_id=user_id, recommended_book_id=book_id)
        self.recommendations.append(recommendation)
        return recommendation

    def remove_recommendation(self, recommendation_id: UUID) -> None:
        before_del = self.recommendations
        self.recommendations = [rec for rec in self.recommendations if rec.id != recommendation_id]

        if len(before_del) == len(self.recommendations):
            raise ValueError
