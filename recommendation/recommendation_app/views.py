# Create your views here.
# recommendation_app/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import generate_recommendation_task, add
from recommendation_app.recommender import generate_recommendation
from django.conf import settings
import logging

@api_view(['GET'])
def get_recommendation(request, user_id):
    service_key = request.headers.get('Service-Key')
    if service_key != settings.SERVICE_SECRET_KEY:
        return Response({'error': 'Unauthorized'}, status=401)
    #TODO Celery not working for some reason, switch to manual for now
    task = generate_recommendation_task.delay(user_id)
    result = task.get(timeout=10)  # Wait for the task to complete
    #result = generate_recommendation(user_id)
    if result:
        print(result)
        logging.info(f"work found and sent {user_id}.")
        return Response({'recommendation': result})
    else:
        logging.info(f"No works found matching the criteria for user {user_id}.")
        return Response({'message': 'No recommendations available at this time.'}, status=404)
    

@api_view(['GET'])
def add_numbers(request):
    x = request.query_params.get('x')
    y = request.query_params.get('y')
    if x is not None and y is not None:
        try:
            x = int(x)
            y = int(y)
            # Call the Celery task
            result = add.delay(x, y)
            sum_result = result.get(timeout=10)
            return Response({'sum': sum_result})
        except ValueError:
            return Response({'error': 'Invalid input'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    else:
        return Response({'error': 'Missing parameters'}, status=400)