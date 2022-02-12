import plotly.figure_factory as ff
from numpy import mean


HEX_OPACITY = 0.3
HEX_DENSITY = 15
FIG_WIDE = None
FIG_TALL = None
MAP_STYLE = 'carto-positron'
DIRECTION_NAMES = [
    'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
    'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'
]
DIRECTION_BIN_SIZE = 360.0 / len(DIRECTION_NAMES)
DIRECTION_DICT = {
    (DIRECTION_BIN_SIZE * i): DIRECTION_NAMES[i]
    for i in range(len(DIRECTION_NAMES))
}


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
    fire_prob_mean_fig.update_layout(
        clickmode='event+select',
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
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
    fire_count_fig.update_layout(
        clickmode='event+select',
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return fire_count_fig


# converts degree to cardinal direction string
def deg_to_dir(deg):
    for key, value in DIRECTION_DICT.items():
        if min_deg_diff(deg, key) <= DIRECTION_BIN_SIZE / 2:
            return value


def min_deg_diff(deg_1, deg_2):
    abs_diff = abs(deg_1 - deg_2)
    return min(abs_diff, 360.0 - abs_diff)


def get_weather_blurb(w_json):
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
