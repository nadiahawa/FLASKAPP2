from app import app
from flask import render_template
import requests as r
import os
from .services import getallpokes
from .services import morepokedata
from flask_login import login_required

@app.route('/')
def home():
    greeting = 'Welcome to the Flask Pokemone API App!'
    print(greeting)

    return render_template('index.html', g = greeting)

@app.route('/pokedex')
def pokeshow():
    return render_template('pokedex.html')


@app.route('/pokemons', methods = ['GET'])
def allpokes():
    context = getallpokes()
    attributes = morepokedata()
    return render_template('pokemons.html', **context, **attributes)

