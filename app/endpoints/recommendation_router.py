from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body
from app.services.recommendation_service import RecommendationService
from app.models.recommendation import Recommendation, CreateRecommendationRequest

recommendation_router = APIRouter(prefix='/recommendations', tags=['Recommendations'])


@recommendation_router.get('/user/{user_id}')
def get_recommendations_for_user(user_id: UUID,
                                 recommendation_service: RecommendationService = Depends(RecommendationService)) -> \
        list[Recommendation]:
    return recommendation_service.get_recommendations_for_user(user_id)


@recommendation_router.post('/add')
def add_recommendation(request: CreateRecommendationRequest, recommendation_service: RecommendationService = Depends(
    RecommendationService)) -> Recommendation:
    new_recommendation = recommendation_service.create_recommendation(request.user_id, request.recommended_book_id)
    return new_recommendation.dict()


@recommendation_router.delete('/remove/{recommendation_id}')
def remove_recommendation(recommendation_id: UUID,
                          recommendation_service: RecommendationService = Depends(RecommendationService)) -> None:
    recommendation_service.remove_recommendation(recommendation_id)
    return {'message': 'Recommendation removed successfully'}
