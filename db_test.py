"""
Just to test database functions,
outside of Flask.

We want to open our MongoDB database,
insert some memos, and read them back
"""

import arrow
from pymongo import MongoClient
import sys
from bson import ObjectId

import CONFIG

try:
    dbclient = MongoClient(CONFIG.MONGO_URL)
    db = dbclient.meetme
    collection = db.busy_times
except:
    print("Failure opening database. Is Mongo running? Correct password?")
    sys.exit(1)

# try:
#     try:
#         record = {'type': 'busy_times',
#                   'key': 321,
#                   'start': {'dateTime': '2015-11-17T09:00:00-08:00'},
#                   'end': {'dateTime': '2015-11-17T15:00:00-08:00'}}
#         collection.insert(record)
#         message = 'times added.'
#     except:
#         message = 'times not added.'
#     print('inserted')
# except:
#     print('not inserted')

try:
    record = {"type": "busy_times"}
    result = collection.delete_many(record)
    print('busy_times removed')
except:
    print('busy_times not removed')

try:
    record = {"type": "date_range"}
    result = collection.delete_many(record)
    print('date_range removed')
except:
    print('date_range not removed')

busy_times = []
for record in collection.find({"type": "busy_times"}):
    busy_times.append(record)

print(busy_times)

date_range = []
for record in collection.find({"type": "date_range"}):
    date_range.append(record)

print(date_range)
