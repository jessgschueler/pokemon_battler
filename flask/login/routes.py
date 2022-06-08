"""It is important to provide a user loader 
callback when using Flask-Login. This keeps t
he current user object loaded in that current 
session based on the stored id."""
from flask import render_template

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



"""we will define three routes for this app"""
app = create_app()

# Home route


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html", title="Home")

# Login route


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    return render_template("auth.html", form=form)

# Register route


@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()

    return render_template("auth.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
