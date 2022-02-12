import numpy as np


Y_LIM = 2 * np.arctan(np.exp(np.pi)) - (np.pi / 2)


# reverse web mercator projection
# https://en.wikipedia.org/wiki/Web_Mercator_projection
# latitute = 2(arctan(e^[clickData y]) - PI/4)
def y_to_lat(y):
    if not -Y_LIM <= y <= Y_LIM:
        raise Exception('y out of bounds')
    return (
        2 * (
            np.arctan(
                np.exp(y)
            ) -
            (np.pi / 4.0)
        )
    )


def click_to_lat_lon(clickData):
    location = None
    if clickData:
        x, y = map(
            float, 
            clickData['points'][0]['location'].split(',')
        )
        lat = np.rad2deg(y_to_lat(y))
        lon = np.rad2deg(x)
        location = [lat, lon]
    return location
