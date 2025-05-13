from flask import current_app
import requests
import os

def weather_by_city(city_name):
    weather_url = current_app.config['WEATHER_URL']
    params = {
        'key': current_app.config['WEATHER_API_KEY'],
        'q': city_name,
        'format': 'json',
        'fx': 'yes',  # Включаем текущую погоду и прогноз
        'lang': 'ru'
    }
    try:
        result = requests.get(weather_url, params=params)
        result.raise_for_status()
        weather = result.json()
          # Отладочный вывод
        if 'data' in weather:
            if 'error' in weather['data']:
                print(f"API error: {weather['data']['error']}")
                return False
            if 'current_condition' in weather['data']:
                try:
                    return weather['data']['current_condition'][0]
                except (IndexError, TypeError) as e:
                    print(f"Error accessing current_condition: {e}")
                    return False
            else:
                print("No 'current_condition' in response")
                return False
        else:
            print("No 'data' in response")
            return False
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return False
    except ValueError as e:

        return False

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.py')
    app.config.from_pyfile(config_path)
    with app.app_context():
        print(weather_by_city('Sevastopol,Russia'))