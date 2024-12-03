# recommendation_app/urls.py

from django.urls import path
from .views import get_recommendation, add_numbers

urlpatterns = [
    path('recommendation/<int:user_id>/', get_recommendation, name='get_recommendation'),
    path('add/', add_numbers, name='add_numbers'),
]
