import plotly.figure_factory as ff
from numpy import mean

HEX_OPACITY = 0.3
HEX_DENSITY = 25
FIG_WIDE = None
FIG_TALL = None
MAP_STYLE = 'carto-positron'


# mean fire probability per hex, based on mock data
def get_mean_fire_fig(df):
    fire_prob_mean_fig = ff.create_hexbin_mapbox(
        data_frame=df, lat="LAT", lon="LON",
        mapbox_style=MAP_STYLE,
        nx_hexagon=HEX_DENSITY, opacity=HEX_OPACITY,
        labels={"color": "mean fire chance"},
        color="FIRE_SCORE", agg_func=mean,
        min_count=1, width=FIG_WIDE, height=FIG_TALL
    )
    fire_prob_mean_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fire_prob_mean_fig


# number of fires recorded per hex
def get_count_fire_fig(df):
    fire_count_fig = ff.create_hexbin_mapbox(
        data_frame=df, lat="LAT", lon="LON",
        mapbox_style=MAP_STYLE,
        nx_hexagon=HEX_DENSITY, opacity=HEX_OPACITY,
        labels={"color": "# of fires"},
        min_count=1, width=FIG_WIDE, height=FIG_TALL
    )
    fire_count_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fire_count_fig
