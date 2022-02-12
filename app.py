import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import json
import random
import src.util as util
import src.figs as figs
import requests


WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')

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
    html.H1(
        children='Wildfires? In MY hexagon?'
    ),

    html.P(
        id='click-receiver',
        style={
            'color': '#FF7F50'
        }
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
    # print(clickData['points'][0]['location'])
    update_string = 'Click on a hex!'
    location = util.click_to_lat_lon(clickData)
    if location:
        lat, lon = location
        update_string = (
            f'Clicked at '
            f'{lat:.3f}\N{DEGREE SIGN}, '
            f'{lon:.3f}\N{DEGREE SIGN}'
        )
    return update_string, location


@app.callback(
    Output('weather-blurb', 'children'),
    Input('click-receiver', 'location')
)
def display_weather_blurb(location):
    markdown = None
    if location:
        lat, lon = location
        print(lat, lon)
        weather_url = (
            f'https://api.openweathermap.org/data/2.5/weather?'
            f'units=imperial&lat={lat}&lon={lon}&appid={WEATHER_API_KEY}'
        )
        weather_req = requests.get(weather_url)
        if weather_req.status_code == 200:
            markdown = figs.get_weather_blurb(weather_req.json())
    return markdown


if __name__ == '__main__':
    app.run_server(debug=True)
