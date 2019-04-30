import requests
from dotenv import load_dotenv
import os
from pprint import pprint
import datetime

load_dotenv()


def get_statistic_per_day(start_time, end_time):
    url = 'https://api.vk.com/method/newsfeed.search'
    params = {
        'access_token': os.getenv('TOKEN'),
        'v': '5.95',
        'q': 'Кока-кола',
        'start_time': start_time,
        'end_time': end_time
    }
    response = requests.get(url, params=params)
    return response.json()['response']['total_count']


def get_statistic_per_period():
    return [(timestamp[0], get_statistic_per_day(timestamp[1], timestamp[2])) for timestamp in get_period_timestamps()]


def get_day_timestaps(year, month, day):
    time_delta = datetime.timedelta(days=1)
    day_start = datetime.datetime(year, month, day)
    day_end = day_start + time_delta
    return datetime.date(day_start.year, day_start.month, day_start.day), day_start.timestamp(), day_end.timestamp()


def get_period_timestamps(n=7):
    today = datetime.date.today().day
    return [get_day_timestaps(2019, 4, day) for day in range(today-n, today)]


if __name__ == '__main__':
    pprint(get_statistic_per_period())