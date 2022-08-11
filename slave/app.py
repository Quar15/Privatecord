# slave/app.py - text chat handling
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
from flask import Flask, redirect, render_template, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, join_room, leave_room

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
    # Connect to every room (1 for each club)
    
    logging.info('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    # Disconnect from every room (1 for each club)

    logging.info('Client disconnected')

#----------------------------------------------------------------------------#
# Flask Controllers
#----------------------------------------------------------------------------#

# allow only whitelisted IPs (it is not completely secure! if You want to be sure use firewall rules)
@app.before_request
def limit_remote_addr():
    if request.remote_addr not in CONFIG['IP']['masterwhitelist']:
        abort(403)

@app.route("/metadata", methods = ['GET'])
def get_metadata():
    return {
        "name": CONFIG['DATA']['name'],
        "description": CONFIG['DATA']['description'],
    }

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
    socketio.run(app, host="0.0.0.0")


if __name__ == "__main__":
    main()