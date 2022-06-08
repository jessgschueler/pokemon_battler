from flask_login import LoginManager
from flask import session, Flask, redirect, request, render_template, url_for
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


login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"


# db = SQLAlchemy()
# migrate = Migrate()
# bcrypt = Bcrypt()


app = Flask(__name__)
# login manager contains code that lets app and login work together
# login_manager = LoginManager()
# # configure it
# login_manager.init_app(app)
# # set secret Key
app.config["SECRET_KEY"] = 'TQIcpo6gbADjldiP9o9XirAl0LliqYpw'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

login_manager.init_app(app)
# db.init_app(app)
# migrate.init_app(app, db)
# bcrypt.init_app(app)
# Route for handling the login page logic
@app.route('/')
def index():
    return 'you made it'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
