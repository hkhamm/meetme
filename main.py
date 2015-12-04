# Gmail
import base64
from email.mime.text import MIMEText

import flask
from flask import Flask
from flask import render_template
from flask import request

# Flask-Mail
from flask.ext.mail import Mail, Message

import logging
import uuid

# Date handling
import arrow  # Replacement for datetime, based on moment.js
from dateutil import tz  # For interpreting local times

# OAuth2  - Google library implementation for convenience
from oauth2client import client
import httplib2  # used in oauth2 flow

# Google API for services
from apiclient import discovery

from busy_times import get_busy_times, get_events
from free_times import get_free_times
from meeting_times import get_meeting_times
from mongo_interface import *

# Globals
app = flask.Flask(__name__)
app.secret_key = str(uuid.uuid4())
app.debug = CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)

# Mail
app.config['MAIL_SERVER'] = 'smtp.uoregon.edu'
app.config['DEFAULT_MAIL_SENDER'] = 'hhamm@uoregon.edu'
app.config['MAIL_USERNAME'] = 'hhamm'
app.config['MAIL_PASSWORD'] = 'Purple-space'
mail = Mail(app)

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = CONFIG.GOOGLE_LICENSE_KEY  # You'll need this
APPLICATION_NAME = 'MeetMe'

# Pages (routed from URLs)


@app.route('/')
@app.route('/index')
def index():
    app.logger.debug('Entering index')
    if 'main-page' not in flask.session:
        init_index_session_values()

    return render_template('index.html')


@app.route('/add-times')
def add_times():
    app.logger.debug('Entering add_times')
    redirect = init_other_session_values('add-times.html', 'add_times')
    if redirect:
        return flask.redirect(flask.url_for('proposal_not_found'))
    return render_template('add-times.html')


@app.route('/finalize-meeting')
def finalize_meeting():
    app.logger.debug('Entering finalize_meeting')
    # if 'key' not in flask.session:
    redirect = init_other_session_values('finalize-meeting.html',
                                         'finalize_meeting')
    if redirect:
        return flask.redirect(flask.url_for('proposal_not_found'))
    init_times_list()
    init_meeting_times()
    return render_template('finalize-meeting.html')


@app.route('/proposal-not-found')
def proposal_not_found():
    app.logger.debug('Entering proposal_not_found')
    return render_template('proposal-not-found.html')


@app.route('/choose')
def choose():
    """
    Renders the main page after a choose request.
    """
    # We'll need authorization to list calendars
    # I wanted to put what follows into a function, but had
    # to pull it back here because the redirect has to be a
    # 'return'
    app.logger.debug('Checking credentials for Google calendar access')
    credentials = valid_credentials()

    if not credentials:
        app.logger.debug('Redirecting to authorization')
        return flask.redirect(flask.url_for('oauth2callback'))

    gcal_service = get_gcal_service(credentials)
    app.logger.debug('Returned from get_gcal_service')
    flask.session['calendars'] = list_calendars(gcal_service)

    return render_template(flask.session['main-page'])


@app.route('/get-times')
def get_times():
    """
    Renders the index.html page after a get-times request.
    """
    app.logger.debug('Checking credentials for Google calendar access')
    credentials = valid_credentials()

    if not credentials:
        app.logger.debug('Redirecting to authorization')
        return flask.redirect(flask.url_for('oauth2callback'))

    gcal_service = get_gcal_service(credentials)
    app.logger.debug('Returned from get_gcal_service')

    flask.session['busy_times'], flask.session['free_times'] = list_times(
        gcal_service)

    return render_template(flask.session['main-page'])


#  Google calendar authorization:
#      Returns us to the main /choose screen after inserting
#      the calendar_service object in the session state.  May
#      redirect to OAuth server first, and may take multiple
#      trips through the oauth2 callback function.
#
#  Protocol for use ON EACH REQUEST:
#     First, check for valid credentials
#     If we don't have valid credentials
#         Get credentials (jump to the oauth2 protocol)
#         (redirects back to /choose, this time with credentials)
#     If we do have valid credentials
#         Get the service object
#
#  The final result of successful authorization is a 'service'
#  object.  We use a 'service' object to actually retrieve data
#  from the Google services. Service objects are NOT serializable ---
#  we can't stash one in a cookie.  Instead, on each request we
#  get a fresh service object from our credentials, which are
#  serializable.
#
#  Note that after authorization we always redirect to /choose;
#  If this is unsatisfactory, we'll need a session variable to use
#  as a 'continuation' or 'return address' to use instead.

def valid_credentials():
    """
    Returns OAuth2 credentials if we have valid
    credentials in the session.  This is a 'truthy' value.
    Return None if we don't have credentials, or if they
    have expired or are otherwise invalid.  This is a 'falsy' value.
    :return: a Google OAuth2 credentials object
    """
    if 'credentials' not in flask.session:
        return None

    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials'])

    if credentials.invalid or credentials.access_token_expired:
        return None

    return credentials


def get_gcal_service(credentials):
    """
    We need a Google calendar 'service' object to obtain
    list of calendars, times, etc.  This requires
    authorization. If authorization is already in effect,
    we'll just return with the authorization. Otherwise,
    control flow will be interrupted by authorization, and we'll
    end up redirected back to /choose *without a service object*.
    Then the second call will succeed without additional authorization.
    :param credentials: a Google OAuth2 credentials object
    :return: the service object.
    """
    app.logger.debug('Entering get_gcal_service')
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http_auth)
    app.logger.debug('Returning service')

    return service


# def get_gmail_service(credentials):
#     """
#     Gets the Gmail service object.
#     :param credentials: is a Google OAuth2 credentials object.
#     :return: the service object.
#     """
#     app.logger.debug('Entering get_gmail_service')
#     http_auth = credentials.authorize(httplib2.Http())
#     service = discovery.build('gmail', 'v1', http=http_auth)
#     app.logger.debug('Returning service')
#
#     return service


@app.route('/oauth2callback')
def oauth2callback():
    """
    The 'flow' has this one place to call back to.  We'll enter here
    more than once as steps in the flow are completed, and need to keep
    track of how far we've gotten. The first time we'll do the first
    step, the second time we'll skip the first step and do the second,
    and so on.
    """
    app.logger.debug('Entering oauth2callback')
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRET_FILE,
        scope=SCOPES,
        redirect_uri=flask.url_for('oauth2callback', _external=True))
    # Note we are *not* redirecting above.  We are noting *where*
    # we will redirect to, which is this function.

    # The *second* time we enter here, it's a callback
    # with 'code' set in the URL parameter.  If we don't
    # see that, it must be the first time through, so we
    # need to do step 1.
    app.logger.debug('Got flow')
    if 'code' not in flask.request.args:
        app.logger.debug('Code not in flask.request.args')
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
        # This will redirect back here, but the second time through
        # we'll have the 'code' parameter set
    else:
        # It's the second time through ... we can tell because
        # we got the 'code' argument in the URL.
        app.logger.debug('Code was in flask.request.args')
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        # Now I can build the service and execute the query,
        # but for the moment I'll just log it and go back to
        # the main screen
        app.logger.debug('Got credentials')

        return flask.redirect(flask.url_for('choose'))


#  Option setting:  Buttons or forms that add some
#     information into session state.  Don't do the
#     computation here; use of the information might
#     depend on what other information we have.
#   Setting an option sends us back to the main display
#      page, where we may put the new information to use.

@app.route('/set-range', methods=['POST'])
def set_range():
    """
    User chose a date range with the bootstrap daterange widget.
    :return: redirects to the choose page
    """
    app.logger.debug('Entering set_range')

    daterange = request.form.get('daterange')
    flask.session['daterange'] = daterange

    daterange_parts = daterange.split()
    flask.session['begin_date'] = interpret_date(daterange_parts[0])
    flask.session['end_date'] = interpret_date(daterange_parts[2])

    store_date_range_db(flask.session['begin_date'], flask.session['end_date'])

    app.logger.debug('set_range parsed {} - {}  dates as {} - {}'.format(
        daterange_parts[0], daterange_parts[1],
        flask.session['begin_date'], flask.session['end_date']))

    return flask.redirect(flask.url_for('choose'))


@app.route('/set-checked-calendars', methods=['POST'])
def set_checked_calendars():
    """
    User chose one or more calendars from the list.
    :return: redirects to the get-times page.
    """
    app.logger.debug('Entering set_checked_calendars')
    calendars = request.form.getlist('calendar')

    flask.session['checked_calendars'] = calendars

    return flask.redirect(flask.url_for('get_times'))


@app.route('/destroy-proposal', methods=['POST'])
def destroy_proposal():
    """
    Destroys the proposal in the database and clears the session.
    :return: redirects to the index page.
    """
    app.logger.debug('Entering destroy_proposal')
    remove_all_times_db()
    remove_date_range_db()
    flask.session.clear()
    return flask.redirect(flask.url_for('index'))


@app.route('/add-recipient', methods=['POST'])
def add_recipient():
    recipient = request.form.get('recipient_address')
    if recipient != '':
        flask.session['recipients'].append(recipient)
    return render_template(flask.session['main-page'])


@app.route('/remove-recipient', methods=['POST'])
def remove_recipient():
    recipient = request.form.get('recipient_address')
    # print('recipient {}'.format(recipient))
    flask.session['recipients'].remove(recipient)
    return render_template(flask.session['main-page'])


@app.route('/set-meeting-time', methods=['POST'])
def set_meeting_time():
    app.logger.debug('Entering set_meeting_time')
    meeting_time = request.form['meeting_times']
    print('meeting_time {}'.format(meeting_time))
    flask.session['meeting_time'] = meeting_time
    return render_template(flask.session['main-page'])


@app.route('/send-mail', methods=['POST'])
def send_mail():
    """
    Sends the body to the recipients.
    :return:
    """
    recipients = flask.session['recipients']
    subject = request.form.get('subject')
    body = request.form.get('message-body')

    # app.logger.debug('Checking credentials for Gmail access')
    # credentials = valid_credentials()
    #
    # if not credentials:
    #     app.logger.debug('Redirecting to authorization')
    #     return flask.redirect(flask.url_for('oauth2callback'))
    #
    # gmail_service = get_gmail_service(credentials)
    # app.logger.debug('Returned from get_gcal_service')
    #
    # for recipient in recipients:
    #     message = create_message('hkhamm@gmail.com', recipient, subject, body)
    #     send_message(gmail_service, 'me', message)

    message = Message(subject=subject, body=body,
                      sender='hhamm@uoregon.edu',
                      recipients=recipients)
    mail.send(message)
    return render_template(flask.session['main-page'])


#  Initialize session variables

def init_index_session_values():
    """
    Start with some reasonable defaults for date and time ranges.
    Note this must be run in app context ... can't call from main.
    """
    app.logger.debug('Entering init_index_session_values')
    flask.session['main-page'] = 'index.html'
    flask.session['main-route'] = 'index'
    flask.session['key'] = str(uuid.uuid4())
    flask.session['recipients'] = []

    # Default date span = tomorrow to 1 week from now
    now = arrow.now('local')
    tomorrow = now.replace(days=+1)
    nextweek = now.replace(days=+7)

    flask.session['begin_date'] = tomorrow.floor('day').isoformat()
    flask.session['end_date'] = nextweek.ceil('day').isoformat()
    flask.session['daterange'] = '{} - {}'.format(
        tomorrow.format('MM/DD/YYYY'),
        nextweek.format('MM/DD/YYYY'))

    # Default time span each day, 9 to 5
    flask.session['begin_time'] = interpret_time('9am')
    flask.session['end_time'] = interpret_time('5pm')


def init_other_session_values(main_page, main_route):
    """
    Initializes the date range, begin and end dates, and begin and end times.
    :param main_page: is the main page for this session.
    :param main_route: is the main route for this session.
    """
    app.logger.debug('Entering init_other_session_values')
    flask.session['main-page'] = main_page
    flask.session['main-route'] = main_route
    flask.session['recipients'] = []

    try:
        flask.session['key'] = request.args.get('key', 0, type=str)
        date_range = get_date_range_db()
    except:
        app.logger.debug('Key not found, redirecting to proposal_not_found')
        return True

    start = arrow.get(date_range['start'])
    end = arrow.get(date_range['end'])

    flask.session['daterange'] = '{} - {}'.format(start.format('MM/DD/YYYY'),
                                                  end.format('MM/DD/YYYY'))
    flask.session['begin_date'] = start.isoformat()
    flask.session['end_date'] = end.isoformat()

    # Default time span each day, 9 to 5
    flask.session['begin_time'] = interpret_time('9am')
    flask.session['end_time'] = interpret_time('5pm')

    return False


def init_times_list():
    """
    Initializes the free times list.
    """
    busy_dict = get_times_db()
    busy = get_busy_times(busy_dict)
    flask.session['free_times'] = get_free_times(busy,
                                                 flask.session['begin_date'],
                                                 flask.session['end_date'])


def init_meeting_times():
    """
    Initializes the meeting times list.
    """
    flask.session['meeting_times'] = get_meeting_times(
        flask.session['free_times'])


def interpret_time(text):
    """
    Read time in a human-compatible format and
    interpret as ISO format with local timezone.
    May throw exception if time can't be interpreted. In that
    case it will also flash a message explaining accepted formats.
    :param text: a human-compatible time
    :return: an arrow date time object
    """
    app.logger.debug("Decoding time '{}'".format(text))
    time_formats = ["ha", "h:mma", "h:mm a", "H:mm"]

    try:
        as_arrow = arrow.get(text, time_formats).replace(tzinfo=tz.tzlocal())
        app.logger.debug('Succeeded interpreting time')
    except:
        app.logger.debug('Failed to interpret time')
        flask.flash("Time '{}' didn't match accepted formats 13:30 or 1:30pm"
                    .format(text))
        raise

    return as_arrow.isoformat()


def interpret_date(text):
    """
    Convert text of date to ISO format used internally,
    with the local time zone.
    :param text: an ISO date
    :return: an arrow date time object
    """
    try:
        as_arrow = arrow.get(text, 'MM/DD/YYYY').replace(
            tzinfo=tz.tzlocal())
    except:
        flask.flash("Date '{}' didn't fit expected format MM/DD/YYYY")
        raise

    return as_arrow.isoformat()


def next_day(iso_text):
    """
    ISO date + 1 day (used in query to Google calendar)
    :param iso_text: an ISO date
    :return: an arrow date time object
    """
    as_arrow = arrow.get(iso_text)

    return as_arrow.replace(days=+1).isoformat()


#  Functions (NOT pages) that return some information
# def create_message(sender, to, subject, message_text):
#     """
#     Create a message for an email.
#     :param sender: Email address of the sender.
#     :param to: Email address of the receiver.
#     :param subject: The subject of the email message.
#     :param message_text: The text of the email message.
#     :return: an object containing a base64url encoded email object.
#     """
#     message = MIMEText(message_text)
#     message['to'] = to
#     message['from'] = sender
#     message['subject'] = subject
#
#     return {'raw': base64.urlsafe_b64encode(message.as_string())}
#
#
# def send_message(service, user_id, message):
#     """
#     Sends an email message.
#     :param service: Authorized Gmail API service instance.
#     :param user_id: User's email address. The special value "me" can be used
#     to indicate the authenticated user.
#     :param message: Message to be sent.
#     :return: the sent message.
#     """
#     try:
#         message = (service.users().messages().send(
#             userId=user_id, body=message).execute())
#         print('Message Id: %s' % message['id'])
#         return message
#     except:
#         print('failed to send message')


def list_times(service):
    """
    Lists the times from the selected calendar in ascending order.
    :param service: a google 'service' object
    :return: busy is a sorted list of busy times and free is a sorted list of
    free times for the selected calendar(s)
    """
    app.logger.debug('Entering list_times')

    events = get_events(service)

    busy = get_busy_times(events)
    add_times_db(busy)

    if flask.session['main-page'] == 'add-times.html':
        busy_dict = get_times_db()
        busy = get_busy_times(busy_dict)

    free = get_free_times(busy, flask.session['begin_date'],
                          flask.session['end_date'])

    return busy, free


def list_calendars(service):
    """
    Given a google 'service' object, return a list of
    calendars.  Each calendar is represented by a dict, so that
    it can be stored in the session object and converted to
    json for cookies. The returned list is sorted to have
    the primary calendar first, and selected (that is, displayed in
    Google Calendars web app) calendars before unselected calendars.
    :param service: a google 'service' object
    :return: a sorted list of calendars
    """
    app.logger.debug('Entering list_calendars')
    calendar_list = service.calendarList().list().execute()
    result = []

    for cal in calendar_list['items']:
        kind = cal['kind']
        cal_id = cal['id']

        summary = cal['summary']

        # Optional binary attributes with False as default
        selected = ('selected' in cal) and cal['selected']
        primary = ('primary' in cal) and cal['primary']

        result.append(
            {'kind': kind,
             'id': cal_id,
             'summary': summary,
             'selected': selected,
             'primary': primary
             })

    return sorted(result, key=cal_sort_key)


def cal_sort_key(cal):
    """
    Sort key for the list of calendars:  primary calendar first,
    then other selected calendars, then unselected calendars.
    (" " sorts before "X", and tuples are compared piecewise)
    :param cal: a calendars
    :return: the sorted calendar
    """
    if cal['selected']:
        selected_key = ' '
    else:
        selected_key = 'X'
    if cal['primary']:
        primary_key = ' '
    else:
        primary_key = 'X'

    return primary_key, selected_key, cal['summary']


# Functions used within the templates

@app.template_filter('fmtdate')
def format_arrow_date(date):
    try:
        normal = arrow.get(date)
        return normal.format('ddd MM/DD/YYYY')
    except:
        return '(bad date)'


@app.template_filter('fmttime')
def format_arrow_time(time):
    try:
        normal = arrow.get(time)
        return normal.format('HH:mm')
    except:
        return '(bad time)'


@app.template_filter('fmtdatetime')
def format_arrow_date_time(date_time):
    try:
        normal = arrow.get(date_time)
        return normal.format('HH:mm, dddd, MM/DD/YYYY')
    except:
        return '(bad date)'


if __name__ == '__main__':
    import uuid

    app.secret_key = str(uuid.uuid4())
    app.debug = CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    if CONFIG.DEBUG:
        app.run(port=CONFIG.PORT)
    else:
        app.run(port=CONFIG.PORT, host='0.0.0.0')
