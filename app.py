import pandas as pd
from dash import Dash, dcc, html, Input, Output
import json
import random
from src.hex_fig import get_hex_fig
from src.location_blurb import get_location_blurb
from src.weather_blurb import get_weather_blurb


# temporarily trimming dataset for testing
# generate fake fire data per location
locations = json.load(open('data/locations.json'))
mock_df = pd.DataFrame(
    [
        location + [random.random(), random.randint(2018, 2021)]
        for location in locations[::15]
    ],
    columns=['lat', 'lon', 'fire_score', 'year']
)


app = Dash(__name__)
server = app.server
app.layout = html.Div([
    html.H2(
        id='click-receiver'
    ),

    html.H3(
        id='weather-blurb'
    ),

    dcc.Graph(
        figure=get_hex_fig(mock_df),
        id='fire-graph',
        className='bordered'
    )
], style={'text-align': 'center'})


# click callback example
@app.callback(
    Output('click-receiver', 'children'),
    Output('click-receiver', 'location'),
    [Input('fire-graph', 'clickData')]
)
def display_location(clickData):
    print(clickData)
    return get_location_blurb(clickData)


@app.callback(
    Output('weather-blurb', 'children'),
    Input('click-receiver', 'location')
)
def display_weather_blurb(location):
    return get_weather_blurb(location)


if __name__ == '__main__':
    app.run_server(debug=True)
