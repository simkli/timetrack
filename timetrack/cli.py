import argparse
from datetime import datetime

from timetrack.figures import daily_overtime, monthly_overtime, weekly_overtime, VAR_TRACKED_TIME, VAR_TRACKED_TIME_SUM, VAR_WORKING_TIME, VAR_OVERTIME, VAR_OVERTIME_SUM
from timetrack.google import authenticate_build_service, GoogleCalendar
from timetrack.config import get_config_from_env
from timetrack.timetracker import TimeTracker, TYPE_WORKING, TYPE_TRACKED
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = 'command'
    parser_report = subparsers.add_parser('report', help='generate a report')
    parser_report.set_defaults(func=cli_report)
    parser_report.add_argument(
        "start",
        help="""retrieve events from Google calendar starting with this date. Fo\
                rmat YYYY-MM-DD (e.g. 2021-12-24)"""
    )
    parser_report.add_argument(
        'view_start',
        metavar='view-start',
        help="""only include events after (>=, including) this event in the repo\
                rt. Format YYYY-MM-DD (e.g. 2021-12-24)"""
    )
    parser_report.add_argument(
        'view_end',
        metavar='view-end',
        help="""only include events before (<=, including) this event in the rep\
                ort. Format YYYY-MM-DD (e.g. 2021-12-25)"""
    )
    parser_report.add_argument(
        'outfile',
        help="""file report is written to"""
    )
    parser_report.add_argument(
        "--plot-daily",
        choices=[VAR_TRACKED_TIME, VAR_TRACKED_TIME_SUM, VAR_WORKING_TIME, VAR_OVERTIME, VAR_OVERTIME_SUM]
    )
    parser_report.add_argument(
        "--plot-weekly",
        choices=[VAR_TRACKED_TIME, VAR_TRACKED_TIME_SUM, VAR_WORKING_TIME, VAR_OVERTIME, VAR_OVERTIME_SUM]
    )
    parser_report.add_argument(
        "--plot-monthly",
        choices=[VAR_TRACKED_TIME, VAR_TRACKED_TIME_SUM, VAR_WORKING_TIME, VAR_OVERTIME, VAR_OVERTIME_SUM]
    )
    parser_report.add_argument(
        "--title",
        help="report title"
    )

    parser_calendar = subparsers.add_parser('calendar', help='list all '
                                                             'calendar ids')
    parser_calendar.set_defaults(func=cli_calendar)
    return parser.parse_args()


def main():
    args = get_args()

    args.func(args)


def cli_report(args):
    config = get_config_from_env()
    service = authenticate_build_service(config.token_file, config.google_client_config)

    start = datetime.strptime(args.start, '%Y-%m-%d')
    view_start = datetime.strptime(args.view_start, '%Y-%m-%d')
    view_end = datetime.strptime(args.view_end, '%Y-%m-%d')

    calendar = GoogleCalendar(service)
    working_hours_events = get_events(config.working_hours_calendars, calendar, start, view_end)
    tracked_time_events = get_events(config.track_calendars, calendar, start, view_end)

    tracker = TimeTracker(start, view_start, view_end)
    tracker.add_events(working_hours_events, TYPE_WORKING)
    tracker.add_events(tracked_time_events, TYPE_TRACKED)

    df = get_table_detail(tracker)
    html = ''
    if args.title:
        html += f'<h1>{args.title}</h1>'

    if args.plot_daily:
        fig = daily_overtime(tracker, args.plot_daily)
        html += f'<img src="{fig}"/>'

    if args.plot_weekly:
        fig = weekly_overtime(tracker, args.plot_weekly)
        html += f'<img src="{fig}"/>'

    if args.plot_monthly:
        fig = monthly_overtime(tracker, args.plot_monthly)
        html += f'<img src="{fig}"/>'

    html += df.to_html(index=False)

    if not args.outfile.endswith('.html'):
        args.outfile += '.html'

    with open(args.outfile, 'w') as fh:
        fh.write(html)


def cli_calendar(args):
    """
    prints all calendar ids and names fetched from Google
    Args:
        args: cli arguments returned from argparse

    """
    config = get_config_from_env()
    service = authenticate_build_service(config.token_file, config.google_client_config)
    calendar = GoogleCalendar(service)
    print("ID - CALENDAR")
    for c in calendar.get_calendars():
        print(f'{c["id"]}  -  {c["summary"]}')


def get_events(calendar_ids, google_calendar, start, end):
    """
    fetches all events from Google calender with calendar_ids starting from
    start until end.
    Args:
        calendar_ids: list of strings containing Google calendar ids
        google_calendar: A Google calendar object (see google.py)
        start: datetime object
        end: datetime object

    Returns:

    """
    events = []
    for cid in calendar_ids:
        events += google_calendar.get_events(cid, start, end)
    return events


def timedelta_str(timed):
    mm, ss = divmod(timed.seconds, 60)
    hh, mm = divmod(mm, 60)
    if timed.days:
        hh += timed.days * 24
    return "%02d:%02d" % (hh, mm)


def get_table_detail(tracker):
    table = []
    for day_date, day, working_time_sum, overtime_sum, tracked_time_sum in tracker:
        table.append({
            'day': day_date.strftime('%Y-%m-%d %A'),
            'start': '',
            'end': '',
            'duration': '',
            'tag': '',
            'tracked_total': '',
            'should_total': '',
            'overtime': '',
            'overtime_sum': ''
        })
        for event in day.tracked_events:
            table.append({
                'day': '',
                'start': event.start.strftime('%H:%M'),
                'end': event.end.strftime('%H:%M'),
                'duration': timedelta_str(event.duration),
                'tag': event.tag,
                'tracked_total': '',
                'should_total': '',
                'overtime': '',
                'overtime_sum': ''
            })
        table.append({
            'day': '',
            'start': '',
            'end': '',
            'duration': '',
            'tag': '',
            'tracked_total': timedelta_str(day.get_tracked_time()),
            'should_total': timedelta_str(day.get_working_time()),
            'overtime': timedelta_str(day.get_overtime() * (-1.00)),
            'overtime_sum': timedelta_str(overtime_sum * (-1.00))
        })

    return pd.DataFrame.from_dict(table)
