# proj7-freetimes
Calculates busy and free times using fetched appointment data from a selection of a user's Google calendars.

### Installation and Execution

1) Install and setup mongodb.

2) Download the repository.

3) Obtain a *Client Id* and *Client Secret* for Google [here](https://auth0.com/docs/connections/social/google) and download as a JSON file to `/path/to/proj8-meetme`.

4) Copy CONFIG.base.py to CONFIG.py and edit for your environment. Include 
the client secret JSON file.

5) Setup the virtual enviroment:
```shell
cd /path/to/proj8-meetme
make
```

5) Run the flask app:
```shell
cd /path/to/proj8-meetme
source env/bin/activate
python3 main.py
```

### Usage

Follow the instructions in the web app.


### Resources

#### Website

- [jQuery](https://jquery.com/)
- [Boostrap](http://getbootstrap.com/)
- [Moment](http://momentjs.com/)
- [Jinja2](http://jinja.pocoo.org/)

#### Server

- [Python 3](http://www.python.org)
- [Flask](http://flask.pocoo.org/)
- [Pymongo](https://api.mongodb.org/python/current/)
- [Arrow](http://crsmithdev.com/arrow/)
- [Google oauth2client](https://github.com/google/oauth2client)
- [Google API Client Library for Python](https://developers.google.com/api-client-library/python/)
