import logging
import io, os
import requests
# flask
from flask import redirect, render_template, request, flash, url_for, abort, make_response, send_from_directory
from flask_login import login_user, current_user, logout_user, login_required

# local
from privatecord import app, db, bcrypt, CONFIG
from privatecord.forms import RegistrationForm, LoginForm
from privatecord.models import MasterUser, SlaveServer, MasterUsersServers, generate_user_ID, get_user_joined_servers, get_user_joined_servers_IPs

#----------------------------------------------------------------------------#
# Flask Controllers
#----------------------------------------------------------------------------#

@app.route("/", methods = ['GET'])
def index():
    return render_template("pages/index.html")


@app.route("/chat", methods = ['GET'])
@login_required
def chat():
    return render_template("pages/chat.html", socketio_server_port=CONFIG['IP']['port'])


@app.route("/img/upload/<img_src>", methods = ['GET', 'POST'])
def get_img(img_src):
    image_path = os.path.abspath(os.path.dirname(__file__)) + url_for('static', filename=f'img/upload/{img_src}')
    if os.path.exists(image_path):
        # Send data from absolute path
        return(send_from_directory(os.path.abspath(os.path.dirname(__file__)) + url_for('static', filename=f'img/upload'), img_src, as_attachment=False))
    # If requested file doesn't exist return 404
    abort(404)

@app.route("/remote/img/upload/<img_src>", methods = ['GET', 'POST'])
def get_img_from_slave(img_src):
    response = requests.get(f"http://localhost:5000/img/upload/{img_src}")
    if response.status_code == 200:
        return response.content
    abort(404)

@app.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    return render_template("pages/account.html")


@app.route("/register", methods = ['GET', 'POST'])
def register():
    # Redirect already logged in users
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    form = RegistrationForm()
    # Validate form
    if form.validate_on_submit():
        # Checking for existing users (login, email) is done within form validators
        # Hash password
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create new user
        user = MasterUser(id=generate_user_ID(), username=form.username.data, email=form.email.data, password=hashed_pwd)
        # Commit to db
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        logging.info('New user created')
        return redirect(url_for('login'))

    return render_template("pages/register.html", form=form)


@app.route("/login", methods = ['GET', 'POST'])
def login():
    # Redirect already logged in users
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    form = LoginForm()
    # Validate form
    if form.validate_on_submit():
        # Validate login data
        u = MasterUser.query.filter_by(email=form.email.data).first()
        if u and bcrypt.check_password_hash(u.password, form.password.data):
            # Login user
            login_user(u, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            # Redirect to last page if exists or chat page
            return redirect(next_page) if next_page else redirect(url_for('chat'))
        else:
            flash('Login unsuccessful. Please check email and password', 'error')
    return render_template("pages/login.html", form=form)


@app.route('/logout', methods = ['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))

#----------------------------------------------------------------------------#
# Flask Error handlers
#----------------------------------------------------------------------------#

@app.errorhandler(500)
def internal_error(error):
    logging.warning(f'{error}')
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404