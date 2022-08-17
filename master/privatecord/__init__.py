# flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_caching import Cache

import socketio

# local
from config.load import CONFIG

#----------------------------------------------------------------------------#
# App Config
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG['DB']['path']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = CONFIG['DATA']['secret']
#app.env = "Production"

cache = Cache(config={
    'CACHE_TYPE': 'FileSystemCache', 
    'CACHE_DIR': 'cache', 
    'CACHE_THRESHOLD': 10,
    'CACHE_DEFAULT_TIMEOUT': 15
})
cache.init_app(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

socketio_flask = SocketIO(app, cors_allowed_origins = "*")
sio = socketio.Client()
sio.connect('http://127.0.0.1:5000')

from privatecord import routes
from privatecord import socketio_serv