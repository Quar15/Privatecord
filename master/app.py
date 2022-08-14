# master/app.py - client app handling
# Author: Kacper Janas

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

# system
from operator import or_
import os
import subprocess
import logging
import uuid
from pathlib import Path
from datetime import date

# flask
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

from waitress import serve

# local
from config.load import CONFIG

#----------------------------------------------------------------------------#
# App Config
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG['DB']['path']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET'] = CONFIG['DATA']['secret']
#app.env = "Production"

db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# SQLAlchemy Models
#----------------------------------------------------------------------------#

class Users(db.Model):
    id = db.Column(db.String(36), primary_key=True) # UUID4
    username = db.Column(db.String)
    avatarPath = db.Column(db.String)
    isBot = db.Column(db.Boolean)
    isSystem = db.Column(db.Boolean)

    def __repr__(self):
        return '[User] (' + str(self.id) +  ')'

#----------------------------------------------------------------------------#
# Flask Controllers
#----------------------------------------------------------------------------#

@app.route("/", methods = ['GET'])
def index():
    return render_template("pages/index.html")

@app.route("/chat", methods = ['GET'])
def chat():
    return render_template("pages/chat.html")

@app.route("/create_user", methods = ['POST'])
def create_user():
    u = Users()
    
    # TODO: Check form contents

    # Generate ID
    IDCanBeUsed: bool = False
    # Make sure ID does not exists in the database (very very small chance but it can happen)
    while(not IDCanBeUsed):
        # Generate new ID
        newUserID: str = uuid.uuid4()
        # TODO: Search the db
        IDCanBeUsed = True


    u.id = newUserID

    logging.info('New user created')

    return render_template("pages/index.html")

#----------------------------------------------------------------------------#
# Flask Error handlers
#----------------------------------------------------------------------------#

@app.errorhandler(500)
def internal_error(error):
    logging.warning(f'Error 500. {error}')
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


#----------------------------------------------------------------------------#
# Launch
#----------------------------------------------------------------------------#

def main():
    serve(app, host="0.0.0.0", port=8080, threads=6)
    # socketio.run(app, host="localhost")


if __name__ == "__main__":
    main()