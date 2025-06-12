import os
import requests
import json

API_KEY = os.getenv("API_KEY")
SETS_URL = os.getenv("SETS_URL")

def get_sets():
    headers = {
        "X-Api-Key": API_KEY
    }
    params = {
        "pageSize": 250
    }

    response = requests.get(SETS_URL, headers=headers, params=params) 
    
    print(json.dumps(response.json(), indent=2)) 

    data = response.json()
    return data["data"]