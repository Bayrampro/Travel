# weather/services.py

import requests


class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.openweathermap.org/data/2.5/forecast/'

    def get_weekly_forecast(self, city):
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
        }
        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return None
