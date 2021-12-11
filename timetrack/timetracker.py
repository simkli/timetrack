from collections import defaultdict
from datetime import timedelta, datetime, date

TYPE_WORKING = 'working'  # cont representing expected working time
TYPE_TRACKED = 'tracked'  # const representing tracked time


class Day:

    def __init__(self):
        # usually should be one per day
        self.working_time_events = []

        self.tracked_events = []

    def add_working_time_event(self, event):
        self.working_time_events.append(event)

    def add_tracked_time_event(self, event):
        self.tracked_events.append(event)

    def get_working_time(self):
        return self._get_duration(self.working_time_events)

    def get_tracked_time(self):
        return self._get_duration(self.tracked_events)

    @staticmethod
    def _get_duration(store):
        duration = timedelta()
        for event in store:
            duration += event.duration
        return duration

    def get_overtime(self):
        return self.get_working_time() - self.get_tracked_time()


class Event:

    def __init__(self, start, end, tag):
        """

        Args:
            start: datetime of event start
            end: datetime of event end
            tag: name/description of event
        """
        self.start = start
        self.end = end
        self.duration = end - start
        self.tag = tag


class TimeTracker:

    def __init__(self, start, view_start, view_end):
        self.start = start
        self.view_start = view_start
        self.view_end = view_end
        self.events = defaultdict(Day)

    def add_events(self, events, type=TYPE_WORKING):
        """

        Args:
            events: list of events retrieved from Google calendar api
            type: string TYPE_WORKING OR TYPE_TRACKED

        """
        for event in events:
            if 'dateTime' not in event['start'] or 'dateTime' not in event['end']:
                print('event skipped no start or end', event['summary'], event['start']['date'])
                continue
            if not 'summary' in event or not event['summary'].startswith('#'):
                print('event skipped has no hashtag', event['summary'], event['start'])
                continue

            event_start = datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
            event_end = datetime.strptime(event['end']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
            event_obj = Event(event_start, event_end, event['summary'])

            day_key = event_start.strftime('%Y-%m-%d')
            if type == TYPE_WORKING:
                self.events[day_key].add_working_time_event(event_obj)
            elif type == TYPE_TRACKED:
                self.events[day_key].add_tracked_time_event(event_obj)
            else:
                raise Exception(f'unknown event type {type}, expected one of {TYPE_TRACKED}, {TYPE_WORKING}')

    def __iter__(self):
        working_time_sum = timedelta()
        overtime_sum = timedelta()
        tracked_time_sum = timedelta()

        days = abs(int((self.start - self.view_end).total_seconds() / 60 / 60 / 24)) + 1

        for day_date in (self.start + timedelta(n) for n in range(days)):
            key = day_date.strftime('%Y-%m-%d')
            day = self.events[key]
            working_time_sum += day.get_working_time()
            tracked_time_sum += day.get_tracked_time()
            overtime_sum += day.get_working_time() - day.get_tracked_time()

            if day_date >= self.view_start and day_date <= self.view_end:
                yield day_date, day, working_time_sum, overtime_sum, tracked_time_sum
