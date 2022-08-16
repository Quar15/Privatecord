import logging
from multiprocessing.connection import wait


from flask_socketio import send, join_room, leave_room, emit
import socketio

from privatecord import socketio_flask, sio

#----------------------------------------------------------------------------#
# Socketio Server Functions
#----------------------------------------------------------------------------#

@socketio_flask.on('message')
def handle_message(message, room="General"):
    print("Received message:", message)
    # Send message with metadata to Slave Server
    sio.emit('message_master', {'msg': message, 'room': room})
    # Send message to clients connected with this server
    send(message, to=room)


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
