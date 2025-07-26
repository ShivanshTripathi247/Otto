import requests
import json

def get_weather(city_name):
    """Fetches weather data for a given city from OpenWeatherMap."""
    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
            api_key = config['OPENWEATHER_API_KEY']
    except (FileNotFoundError, KeyError):
        return "API key not found. Please check your config.json file."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  # For Celsius
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        main = data['main']
        weather_desc = data['weather'][0]['description']
        
        temp = main['temp']
        feels_like = main['feels_like']
        
        return (f"Currently in {city_name}, it's {temp}°C and feels like {feels_like}°C "
                f"with {weather_desc}.")

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return f"Sorry, I could not find the weather for {city_name}."
        else:
            return f"An HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An unexpected error occurred: {err}"