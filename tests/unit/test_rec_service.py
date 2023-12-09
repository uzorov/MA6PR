# /tests/unit/test_recommendation_service.py

import pytest
from uuid import uuid4, UUID
from app.models.recommendation import Recommendation
from app.services.recommendation_service import RecommendationService
from app.repositories.recommendation_repo import RecommendationRepo


@pytest.fixture(scope='session')
def recommendation_service() -> RecommendationService:
    return RecommendationService(RecommendationRepo())


@pytest.fixture(scope='session')
def first_recommendation_data() -> tuple[UUID, UUID, UUID]:
    return uuid4(), uuid4(), uuid4()


@pytest.fixture(scope='session')
def second_recommendation_data() -> tuple[UUID, UUID, UUID]:
    return uuid4(), uuid4(), uuid4()


def test_empty_recommendations(recommendation_service: RecommendationService) -> None:
    assert recommendation_service.get_recommendations_for_user(uuid4()) == []


def test_create_recommendation(
    recommendation_service: RecommendationService,
    first_recommendation_data: tuple[UUID, UUID, UUID]
) -> None:
    user_id, recommended_book_id, _ = first_recommendation_data
    recommendation = recommendation_service.create_recommendation(user_id, recommended_book_id)
    recommendations = recommendation_service.get_recommendations_for_user(user_id)
    assert len(recommendations) == 1
    assert recommendations[0] == recommendation


def test_remove_recommendation(
    recommendation_service: RecommendationService,
    first_recommendation_data: tuple[UUID, UUID, UUID]
) -> None:
    user_id, _, _ = first_recommendation_data
    rec = recommendation_service.get_recommendations_for_user(user_id)[0]

    recommendation_service.remove_recommendation(rec.id)
    recommendations = recommendation_service.get_recommendations_for_user(user_id)
    assert len(recommendations) == 0


def test_remove_nonexistent_recommendation(
    recommendation_service: RecommendationService
) -> None:
    with pytest.raises(ValueError):
        recommendation_service.remove_recommendation(uuid4())
