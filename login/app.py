from flask import (Flask, 
                        g, 
                        redirect, 
                        render_template, 
                        request, 
                        session, 
                        url_for)


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id = 1, username = 'bri', password = 'password'))
users.append(User(id = 2, username= 'jess', password = 'password'))
users.append(User(id = 3, username= 'dylan', password = 'password'))
users.append(User(id = 4, username= 'jarret', password = 'password'))



app = Flask(__name__)
app.secret_key = 'somesecretkey'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        # anywhere we have access to g (pretty much anywhere, we will have access to the user)
        g.user = user

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))   

    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


