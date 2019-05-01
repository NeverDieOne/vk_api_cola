import requests
from dotenv import load_dotenv
import os
import datetime
import plotly.plotly as py
import plotly.graph_objs as go

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


def get_statistic_per_period(timestamps_list):
    return [(timestamp[0], get_statistic_per_day(timestamp[1], timestamp[2])) for timestamp in timestamps_list]


def get_day_timestaps(year, month, day):
    time_delta = datetime.timedelta(days=1)
    day_start = datetime.datetime(year, month, day)
    day_end = day_start + time_delta
    return day_start.timestamp(), day_end.timestamp()


def get_period(n=7):
    today = datetime.date.today()
    days = []

    for n in range(1, n+1):  # Чтобы получить статистику за последние 7 дней, начиная со вчера
        time_delta = datetime.timedelta(days=n)
        day = today - time_delta
        days.append(day)

    return days


def get_period_timestamps(period):
    return [(day, *get_day_timestaps(day.year, day.month, day.day)) for day in period]


def create_schedule(statistic: list, name, auto_open=True):
    trace1 = [go.Bar(
        x=[day[0].day for day in statistic],
        y=[day[1] for day in statistic],
        name=name
    )]
    link = py.plot(trace1, filename=name, auto_open=auto_open)
    return link


if __name__ == '__main__':
    period_of_days = 7

    period = get_period(period_of_days)
    timestamps = get_period_timestamps(period)
    statistic = get_statistic_per_period(timestamps)
    create_schedule(statistic, 'Coca-Cola')






