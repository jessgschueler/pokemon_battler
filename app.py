from flask import (Flask, 
                    g, 
                    redirect, 
                    render_template, 
                    request, 
                    session, 
                    url_for)


class User:
    """create a class for user"""
    def __init__(self, name, , password):
        # set id, username, and password for user
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

"""set users as a list to store for now"""
columns = ['id', 'username', 'password', 'wins', 'losses']


users = [(1, 'bri', 'password', 0, 0),
         (2, 'jess', 'password', 0, 0),
         (3, 'dylan', 'password', 0, 0),
         (4, 'jarret', 'password', 0, 0)]
users_df = pd.DataFrame(
    users, columns=['id', 'username', 'password', 'wins', 'losses'])


"""create flask app"""
app = Flask(__name__)
# name our secret key something
app.secret_key = 'somesecretkey'




""" before the page asks for user name"""
@app.before_request
def before_request(): 
    # makes user global so we can call on it in other places
    g.user = None
    if 'user_id' in session:
        # checks to see if we have the user in my data base
        user = [x for x in users if x.id == session['user_id']][0]
        # anywhere we have access to g (pretty much anywhere, we will have access to the user)
        g.user = user

@ app.route('/new_user', methods=['GET', 'POST'])
df new_trainer():


@app.route('/login', methods = ['GET', 'POST'])
def login():
    """ create a function to log the user in"""
    if request.method == 'POST':
        # logs the user out if they dont complete the log in successfully 
        session.pop('user_id', None)
        # ask for user name and password
        username = request.form['username']
        password = request.form['password']
        # checks to see if the user is in our info and pulls their info
        user = [x for x in users if x.username == username][0]
        """ see if the username and password are a match"""
        if user and user.password == password:
            # set the id as the user id
            session['user_id'] = user.id
            # set them on the path to their profile
            return redirect(url_for('profile'))

        # if user name fails for some reason, resends them to the log in 
        return redirect(url_for('login'))   

    # 
    return render_template('login.html')

"""set route for profile """
@app.route('/profile')
def profile():
    """    sets route for the profile to attach to the template for it"""    
    return render_template('profile.html')


