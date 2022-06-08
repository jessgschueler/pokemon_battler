import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import pandas as db
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)


# create the application instant
app = Flask(__name__)
# load config from this file
app.config.from_object(__name__)
"""In addition to that, you can use the from_object() method on the config 
object and provide it with an import name of a module. Flask will then initialize 
the variable from that module. Note that in all cases, only variable names that 
are uppercase are considered."""

# Load default config and override config from an env variable
app.config.update(dict
                ('DATABASE' = os.path.join(app.root_path, 'flask.db')
                'SECRET_KEY'='development key",
                 # The SECRET_KEY is needed to keep the client-side sessions secure. Choose that key wisely and as hard to guess and complex as possible.
                'USERNAME'='admin',
                'PASSWORD'='default'))
app.config.from_envvar('FLASK_SETTINGS', silent=True)
# Flask allows you to import multiple configurations and it will use the setting defined in the last import
"""Simply define the environment variable FLASKR_SETTINGS that points to a 
config file to be loaded. The silent switch just tells Flask to not complain 
if no such environment key is set."""

"""dd a method that allows for easy connections to the specified database. 
This can be used to open a connection on request and also from the interactive 
Python shell or a script. This will come in handy later. You can create a simple 
database connection through SQLite and then tell it to use the sqlite3.Row object 
to represent rows. This allows the rows to be treated as if they were dictionaries 
instead of tuples."""


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
