# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, send_from_directory, redirect, flash, url_for
from flaskext.login import (LoginManager, login_required,
                            login_user, logout_user, UserMixin)
import Image
import csv
import os

DEBUG = True

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
SECRET_KEY = "dniaovcdavpadp"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(__name__)

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active


FILE_PATH = '/tmp/image'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


USERS = {
    1: User(u"Vidal!", 1),
    2: User(u"Javaguirre!", 2),
}

USER_NAMES = dict((u.name, u) for u in USERS.itervalues())

login_manager = LoginManager()
login_manager.setup_app(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    colours = ''
    if request.method == 'POST':
        f = request.files['image']

        if f and allowed_file(f.filename):
            f.save(FILE_PATH)
            im = Image.open('/tmp/image')
            colours = im.getcolors(im.size[0]*im.size[1])

    return render_template('index.html', colours=colours)


@app.route("/export")
@login_required
def export():
    im = Image.open('/tmp/image')
    colours = im.getcolors(im.size[0]*im.size[1])
    f = open(app.config['UPLOAD_FOLDER'] + '/result.csv', 'wb')
    colour_result = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for colour in colours:
        colour_result.writerow(colour)
    f.close()

    return send_from_directory(app.config['UPLOAD_FOLDER'], 'result.csv')


@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        if username in USER_NAMES:
            remember = request.form.get("remember", "no") == "yes"
            if login_user(USER_NAMES[username], remember=remember):
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.debug = DEBUG
    port = int(os.environ.get('PORT', 45412))
    app.run(host='0.0.0.0', port=port)
