import base64
import io

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

VAR_TRACKED_TIME = 'tracked_time'
VAR_TRACKED_TIME_SUM = 'tracked_time_sum'
VAR_WORKING_TIME = 'working_time'
VAR_OVERTIME = 'overtime'
VAR_OVERTIME_SUM = 'overtime_sum'


def plot_to_base64(plt):
    pic_IObytes = io.BytesIO()
    plt.savefig(pic_IObytes, format='jpeg')
    pic_IObytes.seek(0)
    return 'data:image/png;base64,' + base64.b64encode(pic_IObytes.read()).decode()


def get_df_from_tracker(timetracker):
    table = []
    for day_date, day, working_time_sum, overtime_sum, tracked_time_sum in timetracker:
        table.append({
            'day': day_date.strftime('%Y-%m-%d'),
            'daydate': day_date,
            VAR_TRACKED_TIME: day.get_tracked_time(),
            VAR_TRACKED_TIME_SUM: tracked_time_sum,
            VAR_WORKING_TIME: day.get_working_time(),
            VAR_OVERTIME: day.get_overtime()* (-1),
            VAR_OVERTIME_SUM: overtime_sum* (-1)
        })

    return pd.DataFrame.from_dict(table)


def daily_overtime(timetracker, variable):
    df = get_df_from_tracker(timetracker)
    df[variable] = df[variable].apply(lambda x: x.total_seconds() / 3600) * (-1)
    ax = sns.lineplot(x="day", y=variable, data=df)
    ax.tick_params(axis='x', rotation=90)
    plt.tight_layout()
    return plot_to_base64(plt)


def weekly_overtime(timetracker, variable):
    df = get_df_from_tracker(timetracker)
    df[variable] = df[variable].apply(lambda x: x.total_seconds() / 3600)

    ax = sns.lineplot(x="day", y=variable, data=df)
    for ind, label in enumerate(ax.get_xticklabels()):
        if ind % 7 != 0:
            label.set_visible(False)
    ax.tick_params(axis='x', rotation=90)
    plt.tight_layout()
    return plot_to_base64(plt)


def monthly_overtime(timetracker, variable):
    df = get_df_from_tracker(timetracker)
    df[variable] = df[variable].apply(lambda x: x.total_seconds() / 3600)
    sns.set(rc={'figure.figsize': (13.7, 8.27)})
    ax = sns.lineplot(x="day", y=variable, data=df)
    for ind, label in enumerate(ax.get_xticklabels()):
        if ind % 30 != 0:
            label.set_visible(False)
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    return plot_to_base64(plt)
