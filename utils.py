import csv
import math
from datetime import datetime
from zoneinfo import ZoneInfo


class Capital:
    def __init__(self, name, country, latitude, longitude, timezone):
        self.name = name
        self.country = country
        self.longitude = longitude
        self.latitude = latitude
        self.timezone = timezone

    def get_current_time(self):
        tz = ZoneInfo(self.timezone)
        return datetime.now(tz).replace(microsecond=0)

    def __str__(self):
        return self.name

def load_countries(file):
    capitals = []
    with open(file, 'r') as f:
        csv_file = csv.reader(f, delimiter=',')
        i = 0
        for row in csv_file:
            if i == 0:
                i+=1
                continue
            capital = Capital(
                row[1],
                row[0],
                row[2],
                row[3],
                row[4],
            )
            capitals.append(capital)
            i+=1
    return capitals


def str_to_capital(capital_str, capitals):
    for capital in capitals:
        if capital.name == capital_str:
            return capital
    return None


def get_time_diff(time_a, time_b):
    time_a = time_a.replace(tzinfo=None)
    time_b = time_b.replace(tzinfo=None)
    return abs(time_b - time_a)

def time_to_string(time):
    return time.strftime("%H:%M:%S")

def format_ms(ms):
    hours = math.floor(ms / 3600000)
    minutes = math.floor(ms / 60000) % 60
    seconds = math.floor(ms / 1000) % 60
    miliseconds = ms % 1000
    # Wyświetl tylko 2 pierwsze cyfry
    miliseconds = str(miliseconds)[:2].zfill(2)
    return f'{minutes:02d}:{seconds:02d}:{miliseconds}' if hours == 0 else f'{hours}:{minutes:02d}:{seconds:02d}' 

