# master/app.py - client app handling
# Author: Kacper Janas

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from waitress import serve

# local
from privatecord import app, socketio_flask

#----------------------------------------------------------------------------#
# Launch
#----------------------------------------------------------------------------#

def main():
    #serve(app, host="0.0.0.0", port=8080, threads=6)
    socketio_flask.run(app, host="0.0.0.0", port="8080")


if __name__ == "__main__":
    main()