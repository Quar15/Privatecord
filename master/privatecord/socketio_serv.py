import logging
from datetime import date, datetime
from socket import timeout

from flask import request, session
from flask_login import current_user
from flask_socketio import send, join_room, leave_room, emit
import socketio

from privatecord import socketio_flask, sio, cache

#----------------------------------------------------------------------------#
# Socketio Server Functions
#----------------------------------------------------------------------------#

last_msg_data = {'ID': 'Init'}

@socketio_flask.on('message')
def handle_message(data, room="General"):
    global last_msg_data
    # Add date and time to metadata of the message
    data['date'] = str(date.today().strftime("%d.%m.%Y"))
    data['time'] = str(datetime.now().strftime("%H:%M"))
    if(last_msg_data['ID'] == current_user.id):
        data['continue_thread'] = True
    else:
        data['continue_thread'] = False
    print("Received message:", data)
    # Send message to clients connected with this server
    send(data, to=room)
    # Send message with metadata to Slave Server
    sio.emit('message_master', data)
    data['ID'] = current_user.id
    last_msg_data = data

    # Cache (server-side) messages
    if cache.has('messages'):
        cache.set('messages', [*cache.get('messages'), data])
    else:
        cache.set('messages', [data])


@socketio_flask.on('message_from_slave')
def handle_message_from_slave(data):
    print("Received message from slave server:", data['msg'])
    send(data['msg'], to=data['room'])


@socketio_flask.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)


@socketio_flask.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)


@socketio_flask.on('connect')
def test_connect(auth):
    # Connect to every room (1 for each club)
    join_room('General')
    # Load messages from cache (server-side)
    if cache.has('messages'):
        for msg in cache.get('messages'):
            send(msg, to=request.sid)
    logging.info('Client connected')


@socketio_flask.on('disconnect')
def test_disconnect():
    # Disconnect from every room (1 for each club)

    logging.info('Client disconnected')

#----------------------------------------------------------------------------#
# Socketio Client Functions
#----------------------------------------------------------------------------#

def send_msg(data):
    # @TODO: Change creating new client each time to one static client
    sio_server = socketio.Client()
    sio_server.connect('http://127.0.0.1:8080')
    sio_server.emit('message_from_slave', data)


@sio.on('message_slave')
def handle_message_slave(data):
    send_msg(data)
