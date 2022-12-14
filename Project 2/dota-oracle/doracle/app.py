# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import getpass
import json
import os
import requests as req
from flask import Flask, render_template, request, jsonify, g, redirect, url_for, send_from_directory
from functools import lru_cache

# The ML model files
from model import HeroStats
from utilities import *

package_directory = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------#
# Configs
# ----------------------------------------------------------------------------#

frontend_port = 5000
app = Flask(__name__, static_folder='static', template_folder='templates')

# TODO: Remove before prod
running_user = getpass.getuser()

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
debug_mode = True


# ----------------------------------------------------------------------------#
# Renders
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("index.html", heroes=get_heroes())


@app.route("/explore")
def explore():
    return render_template("explore.html", heroes=get_heroes())


# ----------------------------------------------------------------------------#
# Oracle
# ----------------------------------------------------------------------------#


# <button 1>
@app.route("/suggest1", methods=["POST"])
def suggest1():
    r = request.get_json()
    r["todo"] = "Please rename the button from Suggest1 and implement some functionality here.",

    return jsonify(r)


# <button 2>
@app.route("/suggest2", methods=["POST"])
def suggest2():
    result = request.get_json()

    if len(result['dire']) + len(result['radiant']) < 10:
        result['!error'] = "You need full teams to predict a win percentage🏆"
    else:
        prediction = predict_vs_team(dire=result['dire'], radiant=result['radiant'])[0]
        result['!prediction'] = {
            'Dire': f'{round(prediction[0] * 100, 2)}%',
            'Radiant': f'{round(prediction[1] * 100, 2)}%'
        }
    return jsonify(result)


# <button 3>
@app.route("/suggest3", methods=["POST"])
def suggest3():
    r = request.get_json()
    r["todo"] = "Please rename the button from Suggest3 and implement some functionality here.",

    return jsonify(r)


# ----------------------------------------------------------------------------#
# Explore
# ----------------------------------------------------------------------------#


@app.route("/stats/<int:heroid>", methods=["GET"])
def get_hero_stats(heroid):
    hero_model = get_hero_stat_model()
    win_rate = hero_model.get_winrate(heroid)
    pick_rate = hero_model.get_pickrate(heroid)

    best_paired_with = hero_model.get_best_paired_with_hero(heroid)

    hero = get_hero_by_id(hero_id=heroid)

    hero_name = hero["name"] # wrong
    best_paired_with_name = get_hero_by_id(best_paired_with)["name"]

    hero_stats = {
        "hero": hero_name,
        "win_rate": win_rate,
        "pick_rate": pick_rate,
        "best_paired_with": best_paired_with_name
    }

    print(hero)

    return jsonify(hero_stats)


# ----------------------------------------------------------------------------#
# Helpers
# ----------------------------------------------------------------------------#
def get_hero_by_id(hero_id: int) -> dict:
    heroes = get_heroes()

    for hero in heroes:
        if hero['id'] == hero_id:
            return hero
    return heroes[1]

@lru_cache(maxsize=1)
def get_heroes():
    print(os.getcwd())
    with open(os.path.join(package_directory, "data/heroes.json"), "r") as fp:
        heroes = json.load(fp)

    return heroes


@lru_cache(maxsize=1)
def get_hero_stat_model():
    path_to_model = "/home/dota_oracle_user/models/herostat.pkl"

    hero_stat_model = HeroStats.load(path_to_model)
    return hero_stat_model


if __name__ == '__main__':
    app.jinja_env.cache = {}
    app.run(debug=debug_mode, host='127.0.0.1', port=frontend_port)
