import logging


from flask_socketio import send, join_room, leave_room
import socketio

from privatecord import socketio_flask


#----------------------------------------------------------------------------#
# Socketio Server Functions
#----------------------------------------------------------------------------#

@socketio_flask.on('message')
def handle_message(message, room="General"):
    print("Received message:", message)
    sio.emit('message_master', {'msg': message, 'room': room})
    send(message, to=room)

@socketio_flask.on('message_slave')
def handle_message(data, room="General"):
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

sio = socketio.Client()
sio.connect('http://127.0.0.1:5000')

# sio2 = socketio.Client()
# sio2.connect('http://127.0.0.1:5000')