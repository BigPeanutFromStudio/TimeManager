import math
from datetime import datetime

import pandas as pd
import pytz


class Capital():
    def __init__(self, name, country, latitude, longitude, timezone):
        self.name = name
        self.country = country
        self.longitude = longitude
        self.latitude = latitude
        self.timezone = timezone
    def __str__(self):
        return self.name

def load_countries(file):
    df = pd.read_csv(file)
    capitals = []
    for _, row in df.iterrows():
        capital = Capital(row['stolica'], row['kraj'], row['szerokosc'], row['dlugosc'], row['strefa_czasowa'])
        capitals.append(capital)
    return capitals

def str_to_capital(capital_str, capitals):
    for capital in capitals:
        if capital.name == capital_str:
            return capital
    return None

# TODO: maybe return datetime
def get_capital_time(capital):
    IST = pytz.timezone(capital.timezone)
    return datetime.now(IST).strftime("%H:%M:%S")

def get_time_diff(time_a, time_b):
    return datetime.strptime(time_a, "%H:%M:%S") - datetime.strptime(time_b, "%H:%M:%S")

# Use the haversine formula to calculate the distance between two points on earth's surface
# More about haversine formula: https://en.wikipedia.org/wiki/Haversine_formula

# Think this through, maybe after everything
def get_distance_between(capital_a, capital_b):
     r = 6371000
     d_lat = abs(capital_a.latitude - capital_b.latitude)
     d_lon = abs(capital_a.longitude - capital_b.longitude)
     num = 1 - math.cos(d_lat) + (math.cos(capital_a.latitude) * math.cos(capital_b.latitude) * (1 - math.cos(d_lon)))
     hav = num / 2
     d = 2 * r * math.asin(hav)
     return d

