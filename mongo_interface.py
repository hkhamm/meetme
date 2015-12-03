import flask
import sys
from pymongo import MongoClient

import CONFIG

try:
    dbclient = MongoClient(CONFIG.MONGO_URL)
    db = dbclient.meetme
    collection = db.busy_times
except:
    print("Failure opening database. Is Mongo running? Correct password?")
    sys.exit(1)


def add_times_db(new_times):
    """
    Inserts a list of busy times into the database with the given key.
    :param new_times: is a list of busy times to add to the busy times in
    the database.
    """
    times = convert_times(new_times)

    for time in times:
        try:
            record = {'type': 'busy_times',
                      'key': flask.session['key'],
                      'start': time['start'],
                      'end': time['end']}
            collection.insert(record)
            message = 'times added.'
        except:
            message = 'times not added.'

        # print(message)


def get_times_db():
    """
    Returns a dict of all busy times in the database with the given key.
    """
    records = []
    records_dict = {}
    for record in collection.find({'type': 'busy_times',
                                   'key': flask.session['key']}):
        records_dict[record['start']['dateTime']] = {
            'start': {'dateTime': record['start']['dateTime']},
            'end': {'dateTime': record['end']['dateTime']}
        }
    for key in sorted(records_dict):
        records.append(records_dict[key])

    return records


def remove_all_times_db():
    """
    Deletes all busy times from the database for the given key.
    """
    try:
        record = {'type': 'busy_times',
                  'key': flask.session['key']}
        collection.delete_many(record)
        message = 'times removed'
        result = True
    except:
        message = 'times not removed'
        result = False

    # print(message)

    return flask.jsonify(message=message, result=result)


def convert_times(times):
    """
    Converts from Google Calendar events to busy times that include only
    start and end date times.
    :param times: is a list of Google Calendar events.
    :return: a list of busy time dicts with start and end date times.
    """
    new_times = []

    for time in times:
        new_times.append({'start': {'dateTime': time['start']['dateTime']},
                          'end': {'dateTime': time['end']['dateTime']}})

    return new_times


def store_date_range_db(start, end):
    """
    Stores a date range in the database with the given key.
    :param start: is the start of the date range.
    :param end: is the end of the date range.
    """
    try:
        record = {'type': 'date_range',
                  'key': flask.session['key'],
                  'start': start,
                  'end': end}
        collection.insert(record)
        message = 'date_range added.'
    except:
        message = 'date_range not added.'

    # print(message)


def get_date_range_db():
    """
    Gets the date range from the database for the given key.
    :return: the date range as a list of records.
    """
    records = []
    try:
        for record in collection.find({'type': 'date_range',
                                       'key': flask.session['key']}):
            records.append(record)
        message = 'date_range found'
    except:
        message = 'date_range not found'

    # print(message)
    return records[0]


def remove_date_range_db():
    """
    Removes the date range from the database for the given key.
    """
    try:
        collection.delete_one({'type': 'date_range',
                               'key': flask.session['key']})
        message = 'date range removed'
    except:
        message = 'date range not removed'

    # print(message)
