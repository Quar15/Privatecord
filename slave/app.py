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
from flask import Flask, redirect, render_template, abort, request, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit, join_room, leave_room

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

@socketio.on('message_master')
def handle_message(data):
    if request.remote_addr not in CONFIG['IP']['masterwhitelist']:
        logging.warning(f'Connection outside whitelist {request.remote_addr}')
    logging.info(f"Received message: '{data['msg']}' from {request.remote_addr}")
    # Send message to other Master Servers
    emit('message_slave', data, broadcast=True, skip_sid=[request.sid])


@socketio.on('message_from_slave')
def handle_message_test(data):
    logging.info(f"Received message: '{data['msg']}' from {request.remote_addr}")


@socketio.on('connect')
def test_connect(auth):
    if request.remote_addr not in CONFIG['IP']['masterwhitelist']:
        logging.warning(f'Connection outside whitelist {request.remote_addr}')
        return
    # Connect to every room (1 for each club)
    join_room('General')
    logging.info('Master Server connected')


@socketio.on('disconnect')
def test_disconnect():
    # Disconnect from every room (1 for each club)

    logging.info('Master Server disconnected')

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

@app.route("/img/upload/<img_src>", methods = ['GET', 'POST'])
def get_img(img_src):
    print('@INFO: Image request')
    image_path = os.path.abspath(os.path.dirname(__file__)) + url_for('static', filename=f'img/upload/{img_src}')
    if os.path.exists(image_path):
        # Send data from absolute path
        return(send_from_directory(os.path.abspath(os.path.dirname(__file__)) + url_for('static', filename=f'img/upload'), img_src, as_attachment=True))
    # If requested file doesn't exist return 404
    abort(404)

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