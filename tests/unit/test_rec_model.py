import pytest
from uuid import uuid4
from pydantic import ValidationError

from app.models.recommendation import Recommendation


def test_recommendation_creation():
    id = uuid4()
    user_id = uuid4()
    recommended_book_id = uuid4()

    recommendation = Recommendation(id=id, user_id=user_id, recommended_book_id=recommended_book_id)

    assert dict(recommendation) == {'id': id, 'user_id': user_id, 'recommended_book_id': recommended_book_id}


def test_recommendation_user_id_required():
    id = uuid4()
    recommended_book_id = uuid4()

    with pytest.raises(ValidationError):
        Recommendation(id=id, recommended_book_id=recommended_book_id)


def test_recommendation_recommended_book_id_required():
    id = uuid4()
    user_id = uuid4()

    with pytest.raises(ValidationError):
        Recommendation(id=id, user_id=user_id)
