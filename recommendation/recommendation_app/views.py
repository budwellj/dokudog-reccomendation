# Create your views here.
# recommendation_app/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import generate_recommendation_task, add

@api_view(['GET'])
def get_recommendation(request, user_id):
    task = generate_recommendation_task.delay(user_id)
    result = task.get(timeout=10)  # Wait for the task to complete
    if result:
        return Response({'recommendation': result})
    else:
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