import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.figure_factory as ff
import json
import random

HEX_OPACITY = 0.3
HEX_DENSITY = 40

app = Dash(__name__)

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
# latitute = 2(arctan(e^y) - PI/4)
# y is the y from clickData 
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