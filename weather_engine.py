# weather_engine.py
import requests
import os

API_KEY = os.getenv("API_KEY")


def get_coordinates(city: str):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    res = requests.get(geo_url)
    res.raise_for_status()
    data = res.json()
    if not data:
        raise ValueError("City not found.")
    return data[0]["lat"], data[0]["lon"]

def get_weather(lat: float, lon: float):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()

def get_air(lat: float, lon: float):
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()

def summarize(city: str):
    lat, lon = get_coordinates(city)
    weather = get_weather(lat, lon)
    air = get_air(lat, lon)

    aqi_levels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
    aqi = air["list"][0]["main"]["aqi"]

    return {
        "city": weather["name"],
        "temperature": weather["main"]["temp"],
        "description": weather["weather"][0]["description"],
        "humidity": weather["main"]["humidity"],
        "wind_speed": weather["wind"]["speed"],
        "air_quality": aqi_levels.get(aqi, "Unknown"),
        "icon": f"http://openweathermap.org/img/wn/{weather['weather'][0]['icon']}@2x.png"
    }
