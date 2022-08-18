import os

# flask
from flask import request, abort, send_from_directory, url_for, render_template

# local
from privatecord import app, CONFIG

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