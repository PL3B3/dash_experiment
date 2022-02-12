import pandas as pd
from dash import Dash, dcc, html, Input, Output
import json
import random
import src.util as util
import src.figs as figs

HEX_OPACITY = 0.3
HEX_DENSITY = 25
FIG_WIDE = None
FIG_TALL = None
MAP_STYLE = 'carto-positron'

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

    dcc.Graph(
        figure=figs.get_count_fire_fig(mock_df),
        id='fire-graph'
    )
], style={'color': '#FF7F50'})


# click callback example
@app.callback(
    Output('click-receiver', 'children'),
    [Input('fire-graph', 'clickData')]
)
def display_click_data(clickData):
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
    return update_string


if __name__ == '__main__':
    app.run_server(debug=True)
