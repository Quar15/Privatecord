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
from flask_socketio import SocketIO, send, join_room, leave_room

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

socketio = SocketIO(app, cors_allowed_origins = "*")

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
# Socketio Functions
#----------------------------------------------------------------------------#

@socketio.on('message')
def handle_message(message, room="General"):
    print("Received message:", message)
    if message != "User connected!":
        send(message, to=room)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room (' + room + ').', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)

@socketio.on('connect')
def test_connect(auth):
    logging.info('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    logging.info('Client disconnected')

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

    return render_template("pages/index.html")

#----------------------------------------------------------------------------#
# Flask Error handlers
#----------------------------------------------------------------------------#

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


#----------------------------------------------------------------------------#
# Launch
#----------------------------------------------------------------------------#

def main():
    # serve(app, host="0.0.0.0", port=8080, threads=6)
    socketio.run(app, host="localhost")


if __name__ == "__main__":
    main()