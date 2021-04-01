from app_config import app
from app_config import request, send_html, redirect, render_template
from app_config import login_user, logout_user, login_required, current_user
from db_init import *
import os


def main():
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    # from waitress import serve
    # serve(app, host=host, port=port)
    app.run(host=host, port=port)


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


@app.route("/")
@app.route("/summary")
@app.route("/index")
def summary():
    return send_html("main.html")


@app.route("/day")
def day():
    return send_html("day.html")


@app.route("/summary/group")
def summary_group():
    return send_html("table.html")


@app.route("/summary/day")
def summary_day():
    return send_html("table.html")


if __name__ == '__main__':
    main()
