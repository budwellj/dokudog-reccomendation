# recommendation_app/tasks.py

from celery import shared_task
from .recommender import generate_recommendation

@shared_task
def generate_recommendation_task(user_id):
    return generate_recommendation(user_id)

@shared_task
def add(x, y):
    """A simple test task to add two numbers."""
    return x + y