import arrow
from dateutil import tz

from free_times import get_free_times
from busy_times import get_start_end_datetime, is_available, get_busy_dict, \
    get_busy_list
from main import interpret_time, interpret_date, cal_sort_key
from meeting_times import get_meeting_times


def get_meeting_times_1_test():
    """
    Tests a single day with one free time starting and ending on an hour.
    """
    free_times = [('2015-11-17T09:00:00-08:00', '2015-11-17T15:00:00-08:00')]

    meeting_times = [{'start': {'dateTime': '2015-11-17T09:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T10:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T10:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T11:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T11:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T12:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T12:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T13:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T13:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T14:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T14:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T15:00:00-08:00'}}]

    assert meeting_times == get_meeting_times(free_times)


def get_meeting_times_2_test():
    """
    Tests a single day with one free time starting on a hour and ending on a
    minute.
    """
    free_times = [('2015-11-17T09:00:00-08:00', '2015-11-17T15:30:00-08:00')]

    meeting_times = [{'start': {'dateTime': '2015-11-17T09:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T10:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T10:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T11:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T11:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T12:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T12:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T13:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T13:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T14:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T14:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T15:00:00-08:00'}}]

    assert meeting_times == get_meeting_times(free_times)


def get_meeting_times_3_test():
    """
    Tests a single day with one free time starting on a minute and ending on a
    hour.
    """
    free_times = [('2015-11-17T09:30:00-08:00', '2015-11-17T15:00:00-08:00')]

    meeting_times = [{'start': {'dateTime': '2015-11-17T10:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T11:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T11:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T12:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T12:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T13:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T13:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T14:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T14:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T15:00:00-08:00'}}]

    assert meeting_times == get_meeting_times(free_times)


def get_meeting_times_4_test():
    """
    Tests a single day with two free times starting and ending on hours.
    """
    free_times = [('2015-11-17T09:00:00-08:00', '2015-11-17T10:00:00-08:00'),
                  ('2015-11-17T11:00:00-08:00', '2015-11-17T15:00:00-08:00')]

    meeting_times = [{'start': {'dateTime': '2015-11-17T09:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T10:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T11:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T12:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T12:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T13:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T13:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T14:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T14:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T15:00:00-08:00'}}]

    assert meeting_times == get_meeting_times(free_times)


def get_meeting_times_5_test():
    """
    Tests two days with one free time each starting and ending on hours.
    """
    free_times = [('2015-11-17T09:00:00-08:00', '2015-11-17T11:00:00-08:00'),
                  ('2015-11-18T09:00:00-08:00', '2015-11-18T11:00:00-08:00')]

    meeting_times = [{'start': {'dateTime': '2015-11-17T09:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T10:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T10:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T11:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T09:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T10:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T10:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T11:00:00-08:00'}}]

    assert meeting_times == get_meeting_times(free_times)


def get_meeting_times_6_test():
    """
    Tests a multi-day free time starting and ending on an hour.
    """
    free_times = [('2015-11-17T09:00:00-08:00', '2015-11-18T17:00:00-08:00')]

    meeting_times = [{'start': {'dateTime': '2015-11-17T09:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T10:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T10:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T11:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T11:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T12:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T12:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T13:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T13:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T14:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T14:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T15:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T15:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T16:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T16:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T17:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T09:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T10:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T10:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T11:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T11:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T12:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T12:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T13:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T13:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T14:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T14:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T15:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T15:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T16:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T16:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T17:00:00-08:00'}}]

    assert meeting_times == get_meeting_times(free_times)


def get_meeting_times_7_test():
    """
    Tests a multi-day free time ending on an hour before second day's end.
    """
    free_times = [('2015-11-17T16:00:00-08:00', '2015-11-18T10:00:00-08:00')]

    meeting_times = [{'start': {'dateTime': '2015-11-17T16:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T17:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T09:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T10:00:00-08:00'}}]

    assert meeting_times == get_meeting_times(free_times)


def get_meeting_times_8_test():
    """
    Tests multiple free times on different days.
    """
    free_times = [('2015-11-16T09:00:00-08:00', '2015-11-16T10:00:00-08:00'),
                  ('2015-11-16T13:00:00-08:00', '2015-11-16T15:00:00-08:00'),
                  ('2015-11-16T16:00:00-08:00', '2015-11-16T17:00:00-08:00'),
                  ('2015-11-17T10:00:00-08:00', '2015-11-17T11:00:00-08:00'),
                  ('2015-11-17T16:00:00-08:00', '2015-11-18T10:00:00-08:00'),
                  ('2015-11-18T11:00:00-08:00', '2015-11-18T14:00:00-08:00')]

    meeting_times = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
                      'end': {'dateTime': '2015-11-16T10:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-16T13:00:00-08:00'},
                      'end': {'dateTime': '2015-11-16T14:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-16T14:00:00-08:00'},
                      'end': {'dateTime': '2015-11-16T15:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-16T16:00:00-08:00'},
                      'end': {'dateTime': '2015-11-16T17:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T10:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T11:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T16:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T17:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T09:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T10:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T11:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T12:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T12:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T13:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-18T13:00:00-08:00'},
                      'end': {'dateTime': '2015-11-18T14:00:00-08:00'}}]

    assert meeting_times == get_meeting_times(free_times)


def get_meeting_times_9_test():
    """
    Tests one day with free time all day.
    """
    free_times = [('2015-11-17T09:00:00-08:00', '2015-11-17T17:00:00-08:00')]

    meeting_times = [{'start': {'dateTime': '2015-11-17T09:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T10:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T10:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T11:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T11:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T12:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T12:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T13:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T13:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T14:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T14:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T15:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T15:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T16:00:00-08:00'}},
                     {'start': {'dateTime': '2015-11-17T16:00:00-08:00'},
                      'end': {'dateTime': '2015-11-17T17:00:00-08:00'}}]

    assert meeting_times == get_meeting_times(free_times)


def get_busy_dict_1_test():
    """
    Tests all day events that start before and end during the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'date': '2015-11-12'},
               'end': {'date': '2015-11-16'}}]

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_2_test():
    """
    Tests all day events that start during and end after the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'date': '2015-11-20'},
               'end': {'date': '2015-11-22'}}]

    busy = {'2015-11-20T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-20T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-20T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_3_test():
    """
    Tests all day, 2 day events that start during and end during the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'date': '2015-11-18'},
               'end': {'date': '2015-11-20'}}]

    busy = {'2015-11-18T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-18T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-19T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_4_test():
    """
    Test all day, 1 day events that start during and end during the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'date': '2015-11-19'},
               'end': {'date': '2015-11-20'}}]

    busy = {'2015-11-19T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-19T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-20T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_5_test():
    """
    Test all day events that start before and end after the
    interval.
    """

    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'date': '2015-11-15'},
               'end': {'date': '2015-11-21'}}]

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-20T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_6_test():
    """
    Tests sequential all day events during the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'date': '2015-11-16'},
               'end': {'date': '2015-11-17'}},
              {'start': {'date': '2015-11-17'},
               'end': {'date': '2015-11-18'}}]

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}},
            '2015-11-17T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-17T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-17T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_7_test():
    """
    Tests one day events that start before and end during the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'dateTime': '2015-11-16T08:00:00-08:00'},
               'end': {'dateTime': '2015-11-16T10:00:00-08:00'}}]

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T10:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_8_test():
    """
    Tests one day events that start during and end after the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
               'end': {'dateTime': '2015-11-16T18:00:00-08:00'}}]

    busy = {'2015-11-16T10:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_9_test():
    """
    Tests one day events that start during and end during the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
               'end': {'dateTime': '2015-11-16T11:00:00-08:00'}}]

    busy = {'2015-11-16T10:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T11:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_10_test():
    """
    Tests one day events that start before and end after the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'dateTime': '2015-11-16T08:00:00-08:00'},
               'end': {'dateTime': '2015-11-16T18:00:00-08:00'}}]

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_dict_11_test():
    """
    Tests sequential one day events during the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    events = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
               'end': {'dateTime': '2015-11-16T10:00:00-08:00'}},
              {'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
               'end': {'dateTime': '2015-11-16T11:00:00-08:00'}}]

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T10:00:00-08:00'}},
            '2015-11-16T10:00:00-08:00':
            {'start': {'dateTime': '2015-11-17T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-17T11:00:00-08:00'}}}

    busy_test = get_busy_dict(events, begin_date, end_date)

    for event in busy_test:
        assert event in busy


def get_busy_list_1_test():
    """
    Tests sequential all day busy times.
    """
    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}},
            '2015-11-17T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-17T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-17T17:00:00-08:00'}}}

    busy_list = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
                  'end': {'dateTime': '2015-11-17T17:00:00-08:00'}}]

    assert busy_list == get_busy_list(busy)


def get_busy_list_2_test():
    """
    Tests overlapping all day busy times and busy times within the same day.
    """

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}},
            '2015-11-16T10:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T11:00:00-08:00'}}}

    busy_list = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
                  'end': {'dateTime': '2015-11-16T17:00:00-08:00'}}]

    assert busy_list == get_busy_list(busy)


def get_busy_list_3_test():
    """
    Tests sequential busy times within the same day.
    """

    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T10:00:00-08:00'}},
            '2015-11-16T10:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T11:00:00-08:00'}}}

    busy_list = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
                  'end': {'dateTime': '2015-11-16T11:00:00-08:00'}}]

    assert busy_list == get_busy_list(busy)


def get_busy_list_4_test():
    """
    Tests sequential all day busy times and busy times within the same day.
    """
    busy = {'2015-11-16T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}},
            '2015-11-17T09:00:00-08:00':
            {'start': {'dateTime': '2015-11-17T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-17T10:00:00-08:00'}}}

    busy_list = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
                  'end': {'dateTime': '2015-11-17T10:00:00-08:00'}}]

    assert busy_list == get_busy_list(busy)


def get_busy_list_5_test():
    """
    Tests busy dict is empty.
    """
    busy = {}

    busy_list = []

    assert busy_list == get_busy_list(busy)


def get_free_times_1_test():
    """
    Tests no busy times.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = []

    free = [('2015-11-16T09:00:00-08:00', '2015-11-20T17:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_2_test():
    """
    Tests only one busy time at beginning of the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T10:00:00-08:00'}}]

    free = [('2015-11-16T10:00:00-08:00', '2015-11-20T17:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_3_test():
    """
    Tests only one busy time at end of the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-20T16:00:00-08:00'},
             'end': {'dateTime': '2015-11-20T17:00:00-08:00'}}]

    free = [('2015-11-16T09:00:00-08:00', '2015-11-20T16:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_4_test():
    """
    Tests only one busy time in the middle of the interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T11:00:00-08:00'}}]

    free = [('2015-11-16T09:00:00-08:00', '2015-11-16T10:00:00-08:00'),
            ('2015-11-16T11:00:00-08:00', '2015-11-20T17:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_5_test():
    """
    Tests two busy times, one at the beginning and one in the middle of the
    interval.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T10:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-20T16:00:00-08:00'},
             'end': {'dateTime': '2015-11-20T17:00:00-08:00'}}]

    free = [('2015-11-16T10:00:00-08:00', '2015-11-20T16:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_6_test():
    """
    Tests two busy times in the middle of the interval and on the same day.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T11:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-16T12:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T13:00:00-08:00'}}]

    free = [('2015-11-16T09:00:00-08:00', '2015-11-16T10:00:00-08:00'),
            ('2015-11-16T11:00:00-08:00', '2015-11-16T12:00:00-08:00'),
            ('2015-11-16T13:00:00-08:00', '2015-11-20T17:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_7_test():
    """
    Tests two busy times, one in the middle of the start day and one on a
    different day.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T11:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-17T12:00:00-08:00'},
             'end': {'dateTime': '2015-11-17T13:00:00-08:00'}}]

    free = [('2015-11-16T09:00:00-08:00', '2015-11-16T10:00:00-08:00'),
            ('2015-11-16T11:00:00-08:00', '2015-11-17T12:00:00-08:00'),
            ('2015-11-17T13:00:00-08:00', '2015-11-20T17:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_8_test():
    """
    Tests two busy times, one in the middle not on the start day and one on a
    different day.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-17T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-17T11:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-18T12:00:00-08:00'},
             'end': {'dateTime': '2015-11-18T13:00:00-08:00'}}]

    free = [('2015-11-16T09:00:00-08:00', '2015-11-17T10:00:00-08:00'),
            ('2015-11-17T11:00:00-08:00', '2015-11-18T12:00:00-08:00'),
            ('2015-11-18T13:00:00-08:00', '2015-11-20T17:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_9_test():
    """
    Tests two busy times, one in the middle on the start day and one at the end.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T10:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T11:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-20T16:00:00-08:00'},
             'end': {'dateTime': '2015-11-20T17:00:00-08:00'}}]

    free = [('2015-11-16T09:00:00-08:00', '2015-11-16T10:00:00-08:00'),
            ('2015-11-16T11:00:00-08:00', '2015-11-20T16:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_10_test():
    """
    Tests a complex busy schedule.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-18T11:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-19T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-19T13:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-19T15:00:00-08:00'},
             'end': {'dateTime': '2015-11-19T16:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-20T16:00:00-08:00'},
             'end': {'dateTime': '2015-11-20T17:00:00-08:00'}}]

    free = [('2015-11-18T11:00:00-08:00', '2015-11-18T17:00:00-08:00'),
            ('2015-11-19T13:00:00-08:00', '2015-11-19T15:00:00-08:00'),
            ('2015-11-19T16:00:00-08:00', '2015-11-20T16:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def get_free_times_11_test():
    """
    Tests two busy times, last one ends at end of a day that is not the end day.
    """
    begin_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=9, minute=0, second=0, microsecond=0, day=16,
        month=11, year=2015)
    end_date = arrow.get().replace(
        tzinfo=tz.tzlocal(), hour=17, minute=0, second=0, microsecond=0, day=20,
        month=11, year=2015)

    busy = [{'start': {'dateTime': '2015-11-16T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-16T17:00:00-08:00'}},
            {'start': {'dateTime': '2015-11-18T09:00:00-08:00'},
             'end': {'dateTime': '2015-11-18T17:00:00-08:00'}}]

    free = [('2015-11-17T09:00:00-08:00', '2015-11-17T17:00:00-08:00'),
            ('2015-11-19T09:00:00-08:00', '2015-11-20T17:00:00-08:00')]

    assert free == get_free_times(busy, begin_date, end_date)


def is_available_true_test():
    """
    Tests an event that is transparent.
    """
    event = {'transparency': 'transparent'}

    assert is_available(event)


def is_available_false_test():
    """
    Tests an event that is not transparent.
    """
    event = {}

    assert not is_available(event)


def get_start_end_datetime_is_datetime_test():
    """
    Tests an event that is not all day.
    """
    event = {'start': {'dateTime': '2015-11-22T11:36:51.070854-08:00'},
             'end': {'dateTime': '2015-11-22T16:37:58.735355-08:00'}}

    start = arrow.get('2015-11-22T11:36:51.070854-08:00').replace(
        tzinfo=tz.tzlocal())

    end = arrow.get('2015-11-22T16:37:58.735355-08:00').replace(
        tzinfo=tz.tzlocal())

    is_all_day = False

    assert (start, end, is_all_day) == get_start_end_datetime(event)


def get_start_end_datetime_is_date_test():
    """
    Tests an all day event.
    """
    event = {'start': {'date': '2015-11-22T11:36:51.070854-08:00'},
             'end': {'date': '2015-11-22T16:37:58.735355-08:00'}}

    start = arrow.get('2015-11-22T11:36:51.070854-08:00').replace(
        tzinfo=tz.tzlocal())

    end = arrow.get('2015-11-22T16:37:58.735355-08:00').replace(
        tzinfo=tz.tzlocal())

    is_all_day = True

    assert (start, end, is_all_day) == get_start_end_datetime(event)


def interpret_time_test():
    """
    Tests if a time can be interpreted.
    """
    time = '9:00'

    arrow_time = arrow.get(time, 'H:mm').replace(
        tzinfo=tz.tzlocal()).isoformat()

    assert arrow_time == interpret_time(time)


def interpret_date_test():
    """
    Tests if a date can be interpreted.
    """
    date = '12/25/2015'

    arrow_date = arrow.get(date, 'MM/DD/YYYY').replace(
        tzinfo=tz.tzlocal()).isoformat()

    assert arrow_date == interpret_date(date)


def cal_sort_key_test():
    """
    Tests if a calendar is not primary and is selected.
    """
    cal = {'selected': True,
           'kind': 'calendar#calendarListEntry',
           'primary': False,
           'id': 'fcl59tcklie15bv44kafivmmp4@group.calendar.google.com',
           'summary': 'test'}

    assert ('X', ' ', 'test') == cal_sort_key(cal)
