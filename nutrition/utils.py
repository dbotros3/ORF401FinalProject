import requests
import logging

def search_usda_food(query, api_key):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        'api_key': api_key,
        'query': query,
        'dataType': ["Survey (FNDDS)", "Foundation", "Branded"],
        'pageSize': 5
    }
    try :
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('foods', [])
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        return []
