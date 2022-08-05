# Author: Kacper Janas

from operator import or_
import os
import subprocess
import logging
import webbrowser
from pathlib import Path
from datetime import date

#from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request

from waitress import serve


SORT_BY = "YD"

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.env = "Production"

#db = SQLAlchemy(app)



@app.route("/", methods = ['GET'])
def index():


    return render_template("index.html")


def main():
    
    # set config for logging
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s')

    # if db does not exist create one
    #db.create_all()

    # open browser with site
    webbrowser.open("http://localhost:8080")

    serve(app, host="0.0.0.0", port=8080, threads=6)


if __name__ == "__main__":
    main()