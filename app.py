import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.figure_factory as ff
import json
import random

HEX_OPACITY = 0.3
HEX_DENSITY = 40

app = Dash(__name__)

"""
for long, movement is linear (radial, beach ball lines)
for lat, the closer to poles you get, 
one degree of lat means less vertical movement on map
they're radians oh my godddddddddddd
"""

ca_bounds_lat_lon = {
  'lon_range': [-124.409591, -114.131211],
  'lat_range': [32.534156, 42.009518]
}

ca_corners_dash_coords = {
  'NW': [-2.1713569841888964,0.8094695916078232],
  'SE': [-1.9919654110589782,0.6009796124845259]
}

ca_bounds_dash_coords = {
  'x_range': [ca_corners_dash_coords['NW'][0], ca_corners_dash_coords['SE'][0]],
  'y_range': [ca_corners_dash_coords['SE'][1], ca_corners_dash_coords['NW'][1]]
}

ca_bound_locations = [
  [42.009518, -124.409591],
  [32.534156, -114.131211]
]

def dash_coord_to_lat_lon_california(location):
  x, y = location
  x_range = ca_bounds_dash_coords['x_range']
  y_range = ca_bounds_dash_coords['y_range']
  lon_range = ca_bounds_lat_lon['lon_range']
  lat_range = ca_bounds_lat_lon['lat_range']
  
  x_std = (x - x_range[0]) / abs(x_range[1] - x_range[0])
  y_std = (y - y_range[0]) / abs(y_range[1] - y_range[0])

  x_proj = lon_range[0] + x_std * (lon_range[1] - lon_range[0])
  y_proj = lat_range[0] + y_std * (lat_range[1] - lat_range[0])

  return [x_proj, y_proj]


# generate fake fire data per location
locations = json.load(open('data/locations.json'))
mock_df = pd.DataFrame(
  [location + [random.random()] for location in locations],
  columns=['LAT', 'LON', 'FIRE_SCORE']
)

# median fire probability per hex, based on mock data
fire_prob_median_fig = ff.create_hexbin_mapbox(
    data_frame=mock_df, lat="LAT", lon="LON",
    mapbox_style='open-street-map',
    nx_hexagon=HEX_DENSITY, opacity=HEX_OPACITY, 
    labels={"color": "Median fire chance"},
    color="FIRE_SCORE", agg_func=np.median,
    min_count=1, width=600, height=600
)

fire_prob_median_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# number of fires recorded per hex
fire_count_fig = ff.create_hexbin_mapbox(
    data_frame=mock_df, lat="LAT", lon="LON",
    mapbox_style='open-street-map',
    nx_hexagon=HEX_DENSITY, opacity=HEX_OPACITY, 
    labels={"color": "# of fires"},
    min_count=1, width=600, height=600
)
fire_count_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# you can switch fire_prob_median_fig for fire_count_fig
app.layout = html.Div([
  html.H1(
    children='Wildfires? In MY hexagon?'
  ),
  
  html.P(
    'placeholder',
    id='click-receiver',
    style={
      'color': '#FF7F50'
    }
  ),

  dcc.Graph(
    figure=fire_count_fig,
    id='fire-graph'
  )
], style={'color': '#FF7F50'})


# reverses the mercator projection
# dash's 'y coordinate' ranges from -PI to PI
# confusingly, it isn't radians
# latitute = 2(arctan(e^y) - PI/4)
# https://en.wikipedia.org/wiki/Web_Mercator_projection
def y_to_lat(y):
  return (
    2 * (
      np.arctan(
        np.exp(y) 
      ) -
      (np.pi / 4.0)
    )
  )

# click callback example
@app.callback(
  Output('click-receiver', 'children'),
  [Input('fire-graph', 'clickData')]
)
def display_click_data(clickData):
  # print(clickData['points'][0]['location'])
  location = [float(num) for num in clickData['points'][0]['location'].split(',')]
  location = [y_to_lat(location[1]), location[0]]
  location = [np.rad2deg(num) for num in location]
  return f'clicked at position {location}'

if __name__ == '__main__':
    app.run_server(debug=True)