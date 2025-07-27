import requests
import json
import os
import sys

# This block determines the correct base path for assets
if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def get_weather(city_name):
    config_path = os.path.join(BASE_PATH, 'config.json')
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
            api_key = config['OPENWEATHER_API_KEY']
    except (FileNotFoundError, KeyError):
        return "API key not found. Please check your config.json file."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        main = data['main']
        weather_desc = data['weather'][0]['description']
        temp = main['temp']
        feels_like = main['feels_like']
        return (f"Currently in {city_name}, it's {temp}°C and feels like {feels_like}°C "
                f"with {weather_desc}.")
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            return f"Sorry, I could not find the weather for {city_name}."
        else:
            return "An HTTP error occurred while fetching the weather."
    except Exception as err:
        return f"An unexpected error occurred: {err}"