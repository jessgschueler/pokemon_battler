
"""you can create a function and hook it into a flask 
command that initializes the database"""

def init_db():
    # add a function that initializes the database for you, to the application
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


"""When the command executes, Flask will automatically create 
an application context which is bound to the right application."""
@app.cli.command('initdb')
#  app.cli.command() decorator registers a new command with the flask script
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
