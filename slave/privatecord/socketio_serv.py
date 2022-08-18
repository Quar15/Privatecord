import logging

# flask
from flask import request
from flask_socketio import send, emit, join_room, leave_room

# local
from privatecord import socketio_flask, CONFIG

#----------------------------------------------------------------------------#
# Socketio Functions
#----------------------------------------------------------------------------#

@socketio_flask.on('message_from_master')
def handle_message(data):
    if request.remote_addr not in CONFIG['IP']['masterwhitelist']:
        logging.warning(f'Connection outside whitelist {request.remote_addr}')
    logging.info(f"Received message: '{data['msg']}' from {request.remote_addr}")
    # Send message to other Master Servers
    emit('message_slave', data, broadcast=True, skip_sid=[request.sid])
    # Save message to database
    


@socketio_flask.on('connect')
def test_connect(auth):
    if request.remote_addr not in CONFIG['IP']['masterwhitelist']:
        logging.warning(f'Connection outside whitelist {request.remote_addr}')
        return
    # Connect to every room (1 for each club)
    join_room('General')
    logging.info('Master Server connected')


@socketio_flask.on('disconnect')
def test_disconnect():
    # Disconnect from every room (1 for each club)

    logging.info('Master Server disconnected')