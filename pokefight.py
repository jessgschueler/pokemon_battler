from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd

def df_import(csv_file):
    poke_df = pd.read_csv(csv_file, index_col="english_name")
    return poke_df

poke_df = df_import('pokemon.csv')

def df_drop_add(dataframe):
    """
    ## df_drop_add(dataframe)
    removes a specific list of columns & adds a 'wins' and 'losses' column

    *dataframe:
    - takes a pandas dataframe
    """
    # Columns to drop from dataframe
    dataframe.drop(columns=[
        'japanese_name',
        'percent_male',
        'percent_female',
        'capture_rate',
        'base_egg_steps',
        'evochain_0',
        'evochain_1',
        'evochain_2',
        'evochain_3',
        'evochain_4',
        'evochain_5',
        'evochain_6',
        'gigantamax',
        'mega_evolution',
        'mega_evolution_alt',
    ],   
        axis=1,
        inplace=True,
    )
    # Columns to add to dataframe
    col_list=['wins','losses']
    for col in col_list:
        if col not in dataframe.columns:
            dataframe['wins']=0
            dataframe['losses']=0
        else:
            pass
    return dataframe

poke_df = df_drop_add(poke_df)   

class Pokemon():
    def __init__(self, name, hp, attack, defense, speed):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
    pass

def p1_attacking(pokemon1, pokemon2):
    p1_dmg = (pokemon1.attack - pokemon2.defense)
    while pokemon1.hp > 0:
        if p1_dmg > 0:
            print(f'{pokemon1.name} is attacking {pokemon2.name} for {p1_dmg} damage!')
            pokemon2.hp = (pokemon2.hp - p1_dmg)
            print(f'Leaving {pokemon2.name} with {pokemon2.hp} hp')
            return pokemon2.hp
        else:
            print("oops")

def p2_attacking(pokemon1, pokemon2):
    p2_dmg = (pokemon2.attack - pokemon1.defense)
    while pokemon2.hp > 0:
        if p2_dmg > 0:
            print(f'{pokemon2.name} is attacking {pokemon1.name} for {p2_dmg} damage!')
            pokemon1.hp = (pokemon1.hp - p2_dmg)
            print(f'Leaving {pokemon1.name} with {pokemon1.hp} hp')
            return pokemon1.hp
        else:
            print("bug")

def poke_battle(pokemon1, pokemon2):
        # poke with most speed goes first, if the same p2 goes first
    while pokemon1.speed >= pokemon2.speed:
        if pokemon1.hp > 0:
            p1_attacking(pokemon1, pokemon2)
        else:
            return f'{pokemon1.name} has fainted.'
            # Update P1 Losses and P2 Wins
        if pokemon2.hp > 0:
            p2_attacking(pokemon1, pokemon2)
        else:
            return f'{pokemon2.name} has fainted.'
            # Update P2 Losses and P1 Wins
    while pokemon2.speed > pokemon1.speed:
        if pokemon2.hp > 0:
            p2_attacking(pokemon1, pokemon2)
        else:
            return f'{pokemon2.name} has fainted.'
            # Update P2 Losses and P1 Wins
        if pokemon1.hp > 0:
            p1_attacking(pokemon1, pokemon2)
        else:
            return f'{pokemon1.name} has fainted.'
            # Update P1 Losses and P2 Wins

def updater(pokemon1, pokemon2, str_message):
    """
    Interprets return of poke_battler() and updates pandas df with win and loss data
    """
    if pokemon1.name in str_message:
        poke_df.at[pokemon1.name, "losses"] += 1
        poke_df.at[pokemon2.name, "wins"] += 1
    elif pokemon2.name in str_message:
        poke_df.at[pokemon2.name, "losses"] += 1
        poke_df.at[pokemon1.name, "wins"] += 1
    else:
        pass

app = Flask(__name__)

app.config["SECRET_KEY"] = 'TQIcpo6gbADjldiP9o9XirAl0LliqYpw'

Bootstrap(app)

class PokemonForm(FlaskForm):
    poke_1 = StringField("Pokemon vs...", validators=[DataRequired()])
    poke_2 = StringField("...Pokemon", validators=[DataRequired()])
    submit = SubmitField('Battle!')

@app.route("/", methods=["GET", "POST"])
def poke_fight():
    """
    Accepts user input and runs it through our battler functions
    """
    global poke_df
    form = PokemonForm()
    if form.validate_on_submit() == True:
        poke_1 = form.poke_1.data
        poke_2 = form.poke_2.data
        if poke_1 == poke_2:
            message = f"{poke_1} won't fight another {poke_2}!"
        elif poke_1 in poke_df.index and poke_2 in poke_df.index:
            pokemon1 = Pokemon(poke_1, poke_df.at[poke_1, "hp"], poke_df.at[poke_1, "attack"], poke_df.at[poke_1, "defense"], poke_df.at[poke_1, "speed"])
            pokemon2 = Pokemon(poke_2, poke_df.at[poke_2, "hp"], poke_df.at[poke_2, "attack"], poke_df.at[poke_2, "defense"], poke_df.at[poke_2, "speed"])
            message = poke_battle(pokemon1, pokemon2)
            updater(pokemon1, pokemon2, message)
        elif poke_1 in poke_df.index and poke_2 not in poke_df.index:
            message = f"{poke_2} is not a valid pokemon!"
        elif poke_1 not in poke_df.index and poke_2 in poke_df.index:
            message = f"{poke_1} is not a valid pokemon!"
        else:
            message = f"{poke_1} and {poke_2} are not valid pokemon!"
    else:
        message = "Choose your Pokemon!"
    return render_template('index.html', form=form, message=message)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)