from django.contrib.auth.models import User
from django.db import connections
import random

# recommendation_app/recommender.py

from api.models import UserProfile, Work

def generate_recommendation(user_id):
    try:
        profile = UserProfile.objects.get(user_id=user_id)
        user_difficulty = profile.difficulty_score
        user_themes = profile.themes.all()
        target_language = profile.target_language

        theme_ids = [theme.id for theme in user_themes]

        works = Work.objects.filter(
            difficulty__gte=user_difficulty - 0.1,
            difficulty__lte=user_difficulty + 0.1,
            themes__in=theme_ids,
            language=target_language
        ).distinct()

        if works.exists():
            recommended_work = random.choice(list(works))
            result = {
                'id': recommended_work.id,
                'title': recommended_work.title,
                'author': recommended_work.author,
                'difficulty': recommended_work.difficulty,
            }
        else:
            result = {'message': 'No suitable works found'}

        return result

    except UserProfile.DoesNotExist:
        return {'error': 'UserProfile does not exist'}


