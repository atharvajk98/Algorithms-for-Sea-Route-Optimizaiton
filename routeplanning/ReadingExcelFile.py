import pandas as pd


def readLatLong(path):
    df = pd.read_csv(path)
    lat = df['Lat']
    long = df['Long']
    return lat, long
