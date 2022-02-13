import os
import time
import requests


WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
# lat and lon: weather json
weather_cache = {}
# if we hit an old entry, refresh it
WEATHER_CACHE_TIMEOUT_SECONDS = 100
DIRECTION_NAMES = [
    'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
    'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'
]
DIRECTION_BIN_SIZE = 360.0 / len(DIRECTION_NAMES)
DIRECTION_DICT = {
    (DIRECTION_BIN_SIZE * i): DIRECTION_NAMES[i]
    for i in range(len(DIRECTION_NAMES))
}


def get_weather_blurb(location):
    markdown = '''
    Sunny, expensive, lots of tech people
    '''
    if location:
        location_key = f'{location[0]:.3f}{location[1]:.3f}'
        cached_weather_json = weather_cache.get(location_key)
        # if cache hit AND data is recent
        if (
            cached_weather_json and
            (
                int(time.time()) - cached_weather_json['dt']
            ) < WEATHER_CACHE_TIMEOUT_SECONDS
        ):
            markdown = json_to_blurb(cached_weather_json)
        else:
            weather_cache[location_key] = get_weather_json(location)
            weather_cache[location_key]['dt'] = int(time.time())
            markdown = json_to_blurb(weather_cache[location_key])
    return markdown


def get_weather_json(location):
    lat, lon = location
    weather_url = (
        f'https://api.openweathermap.org/data/2.5/weather?'
        f'units=imperial&lat={lat}&lon={lon}&appid={WEATHER_API_KEY}'
    )
    weather_req = requests.get(weather_url)
    return weather_req.json()


def json_to_blurb(w_json):
    summary = w_json['weather'][0]['main']
    temp = w_json['main']['temp']
    wind_speed = w_json['wind']['speed']
    wind_angle = deg_to_dir(w_json['wind']['deg'])
    markdown = (
        f'Hex weather: '
        f'{summary}, {temp} \N{DEGREE SIGN} F, '
        f'with wind @ {wind_speed} mph {wind_angle}'
    )
    return markdown


# converts degree to cardinal direction string
def deg_to_dir(deg):
    for key, value in DIRECTION_DICT.items():
        if min_deg_diff(deg, key) <= DIRECTION_BIN_SIZE / 2:
            return value


def min_deg_diff(deg_1, deg_2):
    abs_diff = abs(deg_1 - deg_2)
    return min(abs_diff, 360.0 - abs_diff)
