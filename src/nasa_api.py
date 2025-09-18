import requests
from config import NASA_API_KEY

def get_apod(date=None):
    url = f"https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": NASA_API_KEY,
        "date": date
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_mars_rover_photos(sol=None, camera=None):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
    params = {
        "api_key": NASA_API_KEY,
        "sol": sol,
        "camera": camera
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    print(response)
    return response.json()
