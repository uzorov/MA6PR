from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Recommendation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    recommended_book_id: UUID

    def json(self):
        return {
            "user_id": str(self.user_id),
            "recommended_book_id": str(self.recommended_book_id),
        }


class CreateRecommendationRequest(BaseModel):
    user_id: UUID
    recommended_book_id: UUID
