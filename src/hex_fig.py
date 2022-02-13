import plotly.figure_factory as ff
from numpy import mean


HEX_ST = {
    'map': 'carto-positron',
    'font-size': 14,
    'font-fam': 'Roboto Mono, monospace',
    'bg': '#FF7F50',
    'w': None,
    'h': None,
    'opac': 0.4,
    'dens': 14
}


# mean fire probability per hex, based on mock data
def get_hex_fig(df, use_count=True):
    hex_fig = ff.create_hexbin_mapbox(
        data_frame=df, lat="lat", lon="lon",
        mapbox_style=HEX_ST['map'],
        nx_hexagon=HEX_ST['dens'],
        opacity=HEX_ST['opac'],
        animation_frame='year',
        labels=(
            {"color": "Fires", "frame": "Year"}
            if use_count else
            {"color": "Fire Chance", "frame": "Year"}),
        color=None if use_count else "fire_score",
        agg_func=None if use_count else mean,
        min_count=1,
        width=HEX_ST['w'],
        height=HEX_ST['h']
    )
    hex_fig.update_layout(
        clickmode='event+select',
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        plot_bgcolor=HEX_ST['bg'],
        paper_bgcolor=HEX_ST['bg'],
        font_size=HEX_ST['font-size'],
        font_family=HEX_ST['font-fam']
    )
    hex_fig.layout.sliders[0].pad = {"r": 0, "t": 10, "l": 20, "b": 10}
    hex_fig.layout.updatemenus[0].pad = {"r": 0, "t": 30, "l": 10, "b": 0}
    hex_fig.layout.updatemenus[0].x = 0.106
    print(hex_fig.layout)
    return hex_fig
