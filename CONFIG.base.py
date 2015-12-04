"""
Configuration of 'meetme' Flask, MongoDB, Google Calender API app.
Edit to fit development or deployment environment.

"""
# localhost
# PORT = 5000
# DEBUG = True
# MONGO_URL = "mongodb://meetme_user:peach-cobbler@localhost:27017/meetme"

# ix.cs.uoregon.edu
PORT = 7420
DEBUG = False  # Because it's unsafe to run outside localhost
MONGO_URL = "mongodb://meetme_user:peach-cobbler@localhost:4152/meetme"

# both
GOOGLE_LICENSE_KEY = '.client_secret.json'
START_TIME = 9
END_TIME = 17
MAIL_SERVER = 'smtp.uoregon.edu'
DEFAULT_MAIL_SENDER = 'hhamm@uoregon.edu'
