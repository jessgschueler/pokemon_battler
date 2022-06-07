from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config["SECRET_KEY"] = 'TQIcpo6gbADjldiP9o9XirAl0LliqYpw'

Bootstrap(app)

class PokemonForm(FlaskForm):
    poke_1 = StringField("Pokemon vs...", validators=[DataRequired()])
    poke_2 = StringField("...Pokemon", validators=[DataRequired()])
    submit = SubmitField('Battle!')


@app.route("/pokedex", methods=["GET", "POST"])
def pokedex_data():
    """
    HTTP GET: Query for Pokemon 
    """
    global poke_df
    form = PokemonForm()
    if form.validate_on_submit():
        poke_1 = form.poke_1.data
        poke_2 = form.poke_2.data
        message = f"{poke_1} VS {poke_2}"
    else:
        message = "Please enter a valid pokemon!"
    return render_template('index.html', form=form, message=message)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)