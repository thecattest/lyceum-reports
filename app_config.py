from flask import Flask, Response, request, redirect, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# from flask_cors import CORS

from db_init import *
from api import api_blueprint

import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'lyceum_reports_the_best'
# CORS(app)

app.register_blueprint(api_blueprint)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.unauthorized_handler(callback=(lambda: redirect('/login')))


@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    db.expire_on_commit = False
    return db.query(User).get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login_handler():
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form_data = request.form
        form_login = form_data["login"]
        form_password = form_data["password"]
        db = db_session.create_session()
        form_user = db.query(User).filter(User.login == form_login).first()
        if form_user:
            if form_user.check_password(form_password):
                login_user(form_user, True)
                return redirect("/")
            else:
                return render_template("login.html",
                                       alert_title="Ой",
                                       alert_text="Вы ввели неправильный пароль",
                                       login=form_login)
        else:
            return render_template("login.html",
                                   alert_title="Ой",
                                   alert_text="Вы ввели несуществующий логин")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout_handler():
    logout_user()
    return redirect("/login")


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)


def send_html(name):
    content = get_file(os.path.join("templates", name))
    return Response(content, mimetype="text/html")
