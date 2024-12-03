# main_app/utils.py

import requests

def get_sum_from_recommendation_service(x, y):
    url = 'http://localhost:8000/api/add/'
    params = {'x': x, 'y': y}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        return data.get('sum')
    except requests.exceptions.RequestException as e:
        # Handle exceptions (e.g., connection errors, timeouts)
        print(f"An error occurred: {e}")
        return None
