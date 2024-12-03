# recommendation_app/tests/conftest.py

import pytest
from django.contrib.auth.models import User
from api.models import UserProfile, Language

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username="testuser", password="testpass")
    english = Language.objects.create(name='English')
    japanese = Language.objects.create(name='Japanese')
    profile = UserProfile.objects.create(
        user=user,
        difficulty_score=0.5,
        native_language=english,
        target_language=japanese
    )
    return user

