# recommendation_app/tests/test_api.py

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from api.models import UserProfile, Language, Theme, Work, Type
from django.urls import reverse
import random

@pytest.mark.django_db
def test_recommendation_api():
    # Step 1: Create test data

    # Create languages
    native_language = Language.objects.create(name='English')
    target_language = Language.objects.create(name='Japanese')

    # Create themes
    theme1 = Theme.objects.create(name='Science Fiction')
    theme2 = Theme.objects.create(name='Adventure')

    # Create a Work Type
    work_type = Type.objects.create(name='Book')

    # Create Works that match the user's preferences
    work1 = Work.objects.create(
        title='Dune',
        author='Frank Herbert',
        difficulty=0.5,
        type=work_type,
        language=target_language  # Assuming Work model has a ForeignKey to Language
    )
    work1.themes.set([theme1, theme2])

    work2 = Work.objects.create(
        title='Neuromancer',
        author='William Gibson',
        difficulty=0.5,
        type=work_type,
        language=target_language
    )
    work2.themes.set([theme1])

    # Create a test user
    user = User.objects.create_user(username="testuser", password="testpass")

    # Create a UserProfile for the test user
    profile = UserProfile.objects.create(
        user=user,
        difficulty_score=0.5,
        native_language=native_language,
        target_language=target_language,
    )
    # Assign themes to the profile
    profile.themes.set([theme1, theme2])

    # Step 2: Log in with the test user to obtain authentication
    client = APIClient()
    login_response = client.post('/api/token/', {'username': 'testuser', 'password': 'testpass'})
    assert login_response.status_code == 200, "Login failed!"

    token = login_response.data['access']

    # Step 3: Make an authenticated API request
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    url = reverse('get_recommendation', args=[user.id])
    response = client.get(url)

    # Step 4: Assert the response
    assert response.status_code == 200
    recommended_work =  response.data['recommendation'] # Expecting a recommended work with a title
    assert recommended_work['title'] == 'Neuromancer'
    assert recommended_work['author'] == 'William Gibson'
    assert recommended_work['difficulty'] == 0.5
    # Additional assertions can be added based on the expected response structure


@pytest.mark.django_db
def test_recommendation_api_no_works():
    # Step 1: Create test data without Works

    # Create languages
    native_language = Language.objects.create(name='English')
    target_language = Language.objects.create(name='Japanese')

    # Create themes
    theme1 = Theme.objects.create(name='Science Fiction')
    theme2 = Theme.objects.create(name='Adventure')

    # Create a test user
    user = User.objects.create_user(username="testuser2", password="testpass")

    # Create a UserProfile for the test user
    profile = UserProfile.objects.create(
        user=user,
        difficulty_score=0.5,
        native_language=native_language,
        target_language=target_language,
    )
    # Assign themes to the profile
    profile.themes.set([theme1, theme2])

    # Step 2: Log in with the test user to obtain authentication
    client = APIClient()
    login_response = client.post('/api/token/', {'username': 'testuser2', 'password': 'testpass'})
    assert login_response.status_code == 200, "Login failed!"

    token = login_response.data['access']

    # Step 3: Make an authenticated API request
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    url = reverse('get_recommendation', args=[user.id])
    response = client.get(url)

    # Step 4: Assert that no recommendations are available
    assert response.status_code == 200
    assert 'message' in response.data['recommendation']
    assert response.data['recommendation']['message'] == 'No suitable works found'