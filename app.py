import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import json
import random
import src.util as util
import src.figs as figs
import requests
import time


WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')

# lat and lon: weather json
weather_cache = {}
# if we hit an old entry, refresh it
WEATHER_CACHE_TIMEOUT_SECONDS = 100

app = Dash(__name__)
server = app.server

# generate fake fire data per location
locations = json.load(open('data/locations.json'))
mock_df = pd.DataFrame(
    [location + [random.random()] for location in locations],
    columns=['LAT', 'LON', 'FIRE_SCORE']
)

# you can switch fire_prob_median_fig for fire_count_fig
app.layout = html.Div([
    html.H2(
        id='click-receiver'
    ),

    dcc.Markdown(
        id='weather-blurb'
    ),

    dcc.Graph(
        figure=figs.get_count_fire_fig(mock_df),
        id='fire-graph'
    )
], style={'color': '#FF7F50'})


# click callback example
@app.callback(
    Output('click-receiver', 'children'),
    Output('click-receiver', 'location'),
    [Input('fire-graph', 'clickData')]
)
def display_location(clickData):
    # print(clickData)
    update_string = 'Wildfires? In MY hexagon? Click to find out!'
    location = util.click_to_lat_lon(clickData)
    if location:
        lat, lon = location
        update_string = (
            f'Hex @:   '
            f'{lat:.3f}\N{DEGREE SIGN}, '
            f'{lon:.3f}\N{DEGREE SIGN}'
            f' (lat, lon)'
        )
    return update_string, location


@app.callback(
    Output('weather-blurb', 'children'),
    Input('click-receiver', 'location')
)
def display_weather_blurb(location):
    markdown = '''
    Sunny, expensive, lots of tech people
    '''
    if location:
        location_key = f'{location[0]:.3f}{location[1]:.3f}'
        # print('location_key: ', location_key)
        cached_weather_json = weather_cache.get(location_key)
        # print(int(time.time()), cached_weather_json)
        if (
            cached_weather_json and
            (
                int(time.time()) - cached_weather_json['dt']
            ) < WEATHER_CACHE_TIMEOUT_SECONDS
        ):
            print('cache hit!')
            markdown = figs.get_weather_blurb(cached_weather_json)
        else:
            lat, lon = location
            print('cache miss')
            weather_url = (
                f'https://api.openweathermap.org/data/2.5/weather?'
                f'units=imperial&lat={lat}&lon={lon}&appid={WEATHER_API_KEY}'
            )
            weather_req = requests.get(weather_url)
            if weather_req.status_code == 200:
                weather_cache[location_key] = weather_req.json()
                weather_cache[location_key]['dt'] = int(time.time())
                markdown = figs.get_weather_blurb(weather_req.json())
    return markdown


if __name__ == '__main__':
    app.run_server(debug=True)
