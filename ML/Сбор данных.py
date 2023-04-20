import requests
import json

API_KEY = "your_russpass_api_key"
BASE_URL = "https://api.russpass.ru/"

def fetch_data(api_method, params):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = f"{BASE_URL}/{api_method}"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
