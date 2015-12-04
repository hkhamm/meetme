# proj8-freetimes
Calculates a list of hour long meeting times from multiple users Google calendar events. Provides pages to create a new meeting proposal, add additional times, and to choose a meeting time or destroy the meeting proposal.

This can be made available at http://ix.cs.uoregon.edu:7420 upon request.

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
- [Flask-Mail](https://pythonhosted.org/Flask-Mail/)
- [Pymongo](https://api.mongodb.org/python/current/)
- [Arrow](http://crsmithdev.com/arrow/)
- [Google oauth2client](https://github.com/google/oauth2client)
- [Google API Client Library for Python](https://developers.google.com/api-client-library/python/)


### Other Comments

Flask-Mail is pretty straight forward to use, though their docs mistakenly 
list the import as 'from flaskext.mail import Mail' when it should be 'from 
flask.ext.mail import Mail'.

Other than this problem, I only had to copy their sample and modify the 
message for my context. 
