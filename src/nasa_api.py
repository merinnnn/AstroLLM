import requests
from .config import NASA_API_KEY

def get_apod(date=None):
    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": NASA_API_KEY
    }
    if date: 
        params["date"] = date
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()

def get_mars_photos(sol=1000, rover="curiosity", camera=None):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos"
    params = {
        "api_key": NASA_API_KEY,
        "sol": sol
    }
    if camera: 
        params["camera"] = camera
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()
