import pandas as pd
TABLE_START = 4
ROW_START = 55

"""
Nabin:
Generate URLs
make request (requests library)

Kevin:
document what each column means
parse file
store to dataframe
filter out other states (like nevada)

Yash:
turn into grid data
"""

with open('data\\PNM_Mar_2022.txt') as file:
    lines = file.read().splitlines()[TABLE_START:]
    data = [line[ROW_START:].split() for line in lines]

    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    df = df[1:]

    df.to_csv("data/test_noaa_precip.csv")
