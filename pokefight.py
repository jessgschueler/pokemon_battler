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

class Pokemon():
    def __init__(self, name, hp, attack, defense, speed):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
    pass

### BATTLE LOGIC ###
def p1_attacking(pokemon1, pokemon2):
    """
    ### Pokemon1 attacks Pokemon2 for p1_dmg

    - p1_dmg: Takes pokemon1's attack and minuses pokemon2's defense having the total equal the damage.
    """
    # Calculate damage for poke2 to take
    p1_dmg = (pokemon1.attack - pokemon2.defense)
    # Can only attack with positive health total
    if pokemon1.hp > 0:
        # Has to have a positive number for damage to deal damage
        if p1_dmg > 0:
            print(f'{pokemon1.name} is attacking {pokemon2.name} for {p1_dmg} damage!')
            # Set poke2's new hp to be health minus damage
            pokemon2.hp = (pokemon2.hp - p1_dmg)
            print(f'Leaving {pokemon2.name} with {pokemon2.hp} hp')
            return pokemon2.hp
        else:
        # Catches if they do not have a damage of above 0
            print(f"{pokemon1.name}'s {p1_dmg} damage is not enough to damage {pokemon2.name}")
            return pokemon2.hp
    else:
    # allows the other pokemon to attack in poke_battle function
        pass

def p2_attacking(pokemon1, pokemon2):
    """
    ### Pokemon2 attacks Pokemon1 for p2_dmg

    - p2_dmg: Takes pokemon2's attack and minuses pokemon1's defense having the total equal the damage.
    """
    # Calculate damage for poke1 to take
    p2_dmg = (pokemon2.attack - pokemon1.defense)
    # Can only attack with positive health total
    if pokemon2.hp > 0:
        # Has to have a positive number for damage to deal damage
        if p2_dmg > 0:
            print(f'{pokemon2.name} is attacking {pokemon1.name} for {p2_dmg} damage!')
            # Set poke2's new hp to be health minus damage
            pokemon1.hp = (pokemon1.hp - p2_dmg)
            print(f'Leaving {pokemon1.name} with {pokemon1.hp} hp')
            return pokemon1.hp
        # Catches if they do not have a damage of above 0    
        else:
            return pokemon1.hp
    # allows the other pokemon to attack in poke_battle function
    else:
        pass

def poke_battle(pokemon1, pokemon2):
    """
    Pits two pokemon against each other, calling p1_attacking() & p2_attacking()
    """
    # Checks to make sure both pokemon have positive damage before while loop
    if (pokemon2.attack - pokemon1.defense) > 0 and (pokemon2.attack - pokemon1.defense) > 0:
        # Runs while both pokemon have positive health.
        while pokemon1.hp > 0 and pokemon2.hp > 0:
            # Determining which poke goes first by comparing speed
            if pokemon1.speed > pokemon2.speed:
                # If pokemon has positive health, it attacks
                if pokemon1.hp > 0:
                    p1_attacking(pokemon1, pokemon2)
                else:
                    # If pokemon has negative health, break loop and return fainted string.
                    return f'{pokemon1.name} has fainted.'
                # If pokemon is still alive after being attacked, it then attacks
                if pokemon2.hp > 0:
                    p2_attacking(pokemon1, pokemon2)
                else:
                    # If pokemon has negative health, break loop and return fainted string.
                    return f'{pokemon2.name} has fainted.'
            else:
                pass
            # This functions the same way as the other speed check, if they have the same speed pokemon2 goes first.
            # This just flips the turn order for which poke is attacking.
            if pokemon2.speed >= pokemon1.speed:
                if pokemon2.hp > 0:
                    p2_attacking(pokemon1, pokemon2)
                else:
                    return f'{pokemon2.name} has fainted.'
                if pokemon1.hp > 0:
                    p1_attacking(pokemon1, pokemon2)
                else:
                    return f'{pokemon1.name} has fainted.'
    # If both poke's have negative damage, compare the attacks and the one with the most wins.
    else:
        if pokemon1.attack > pokemon2.attack:
            return f'{pokemon2.name} has fainted.'
        elif pokemon2.attack > pokemon1.attack:
            return f'{pokemon1.name} has fainted.'
        # If both poke's have the same attack, compare speed.
        else:
            if pokemon1.speed > pokemon2.speed:
                return f'{pokemon2.name} has fainted.'
            elif pokemon2.speed > pokemon1.speed:
                return f'{pokemon1.name} has fainted.'
            # This defaults if ALL the other conditionals have failed. We could have more conditionals to fall into, but eventually someone has to win.
            else:
                f'{pokemon2.name} has fainted.'
                # R.I.P.

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
    HTTP GET: Query for Pokemon 
    """
    global poke_df
    form = PokemonForm()
    if form.validate_on_submit() == True:
        poke_1 = form.poke_1.data
        poke_2 = form.poke_2.data
        if poke_1 in poke_df.index and poke_2 in poke_df.index:
            pokemon1 = Pokemon(poke_1, poke_df.at[poke_1, "hp"], poke_df.at[poke_1, "attack"], poke_df.at[poke_1, "defense"], poke_df.at[poke_1, "speed"])
            pokemon2 = Pokemon(poke_2, poke_df.at[poke_2, "hp"], poke_df.at[poke_2, "attack"], poke_df.at[poke_2, "defense"], poke_df.at[poke_2, "speed"])
            message = poke_battle(pokemon1, pokemon2)
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