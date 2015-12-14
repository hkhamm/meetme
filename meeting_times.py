import arrow

import CONFIG

START_TIME = CONFIG.START_TIME
END_TIME = CONFIG.END_TIME


def get_meeting_times(free_times):
    """
    Creates a list of hour long meeting times from a list of free times.
    :param free_times: is a list of free times.
    :return: a list of meeting times.
    """
    meeting_times = []

    for time in free_times:
        start = arrow.get(time[0])
        end = arrow.get(time[1])
        start_date = start.format('YYYYMMDD')
        end_date = end.format('YYYYMMDD')
        start_minute = start.format('mm')

        if start_minute != '00':
            start = start.replace(hours=+1, minute=0)

        if start_date == end_date:
            # handle one day free times
            start_hour = start.format('HH')
            end_hour = end.format('HH')
            hours = int(end_hour) - int(start_hour)
            meeting_start_time = start.isoformat()
            meeting_end_time = start.replace(hours=+1)

            add_meeting_time(meeting_times, meeting_start_time,
                             meeting_end_time.isoformat())

            add_hour_intervals(meeting_times, hours, meeting_end_time)
        else:
            # handle multi-day free times
            days = int(end.format('DD')) - int(start.format('DD')) + 1
            day_start = start
            day_end = start.replace(hour=END_TIME, minute=0)
            meeting_start_time = start
            meeting_end_time = start.replace(hours=+1)

            add_meeting_time(meeting_times, meeting_start_time.isoformat(),
                             meeting_end_time.isoformat())

            for i in range(days):
                if i > 0:
                    day_start = start.replace(days=+1, hour=START_TIME,
                                              minute=0)
                    day_end = day_start.replace(hour=END_TIME, minute=0)
                    free_time_end_hour = end.format('HH')
                    day_end_hour = day_end.format('HH')

                    if free_time_end_hour < day_end_hour:
                        day_end = end

                    meeting_start_time = day_start.isoformat()
                    meeting_end_time = day_start.replace(hours=+1)

                    add_meeting_time(meeting_times, meeting_start_time,
                                     meeting_end_time.isoformat())

                start_hour = day_start.format('HH')
                end_hour = day_end.format('HH')
                hours = int(end_hour) - int(start_hour)

                add_hour_intervals(meeting_times, hours, meeting_end_time)

    for time in meeting_times:
        print(time)

    return meeting_times


def add_meeting_time(meeting_times, start_time, end_time):
    """
    Adds a single meeting time to meeting times.
    :param meeting_times: is the list of meeting times.
    :param start_time: is the start of the meeting time.
    :param end_time: is th end of the meeting time.
    """
    meeting_times.append({'start': {'dateTime': start_time},
                          'end': {'dateTime': end_time}})


def add_hour_intervals(meeting_times, hours, meeting_end_time):
    """
    Adds hour long meeting times from a range to meeting times.
    :param meeting_times: is the list of meeting times.
    :param hours: is the number of hours in the range.
    :param meeting_end_time: is the end of the first meeting time.
    """
    for i in range(hours - 1):
        meeting_start_time = meeting_end_time
        meeting_end_time = meeting_end_time.replace(hours=+1)
        add_meeting_time(meeting_times, meeting_start_time.isoformat(),
                         meeting_end_time.isoformat())
