import pytest
from uuid import uuid4
from app.models.recommendation import Recommendation
from app.repositories.recommendation_repo import RecommendationRepo


@pytest.fixture(scope='session')
def recommendation_repo() -> RecommendationRepo:
    return RecommendationRepo()


@pytest.fixture(scope='session')
def first_recommendation() -> Recommendation:
    user_id = uuid4()
    recommended_book_id = uuid4()

    return Recommendation(id=uuid4(), user_id=user_id, recommended_book_id=recommended_book_id)


@pytest.fixture(scope='session')
def second_recommendation() -> Recommendation:
    user_id = uuid4()
    recommended_book_id = uuid4()

    return Recommendation(id=uuid4(), user_id=user_id, recommended_book_id=recommended_book_id)


recommendation_test_repo = RecommendationRepo()


def test_empty_recommendation_list() -> None:
    assert recommendation_test_repo.get_recommendations_for_user(uuid4()) == []


def test_create_recommendation(recommendation_repo: RecommendationRepo,
                               first_recommendation: Recommendation) -> None:
    recommendation_repo.create_recommendation(first_recommendation.recommended_book_id, first_recommendation.user_id)
    recommendations = recommendation_repo.get_recommendations_for_user(first_recommendation.user_id)
    assert len(recommendations) == 1
    assert recommendations[0].recommended_book_id == first_recommendation.recommended_book_id


def test_remove_recommendation(recommendation_repo: RecommendationRepo,
                               first_recommendation: Recommendation) -> None:
    recommendation = recommendation_repo.get_recommendations_for_user(first_recommendation.user_id)[0]
    recommendation_repo.remove_recommendation(recommendation.id)
    recommendations = recommendation_repo.get_recommendations_for_user(first_recommendation.user_id)
    assert len(recommendations) == 0


def test_remove_nonexistent_recommendation(recommendation_repo: RecommendationRepo) -> None:
    with pytest.raises(ValueError):
        recommendation_repo.remove_recommendation(uuid4())
