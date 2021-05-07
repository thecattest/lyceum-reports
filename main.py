from app_config import app
from app_config import request, send_html, redirect, render_template
from app_config import login_required, current_user
from db_init import *
import os


def main():
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    # from waitress import serve
    # serve(app, host=host, port=port)
    app.run(host=host, port=port)


@app.route("/")
@app.route("/summary")
@app.route("/index")
@login_required
def summary():
    return send_html("main.html")


@app.route("/day")
@login_required
def day():
    gid = request.args.get("id")
    if gid is None or not gid:
        return render_template("error.html", text="Ошибка в ссылке", link="/")
    db = db_session.create_session()
    g = db.query(Group).get(gid)
    db.close()
    if g is None:
        return render_template("error.html", text="Такого класса не существует", link="/")
    if current_user.role == current_user.TYPE.EDITOR \
            and current_user.allowed_group.id != g.id:
        return render_template("error.html", text="Вам сюда нельзя", link="/")
    return send_html("day.html")


@app.route("/summary/group")
@login_required
def summary_group():
    gid = request.args.get("id")
    if gid is None or not gid:
        return render_template("error.html", text="Ошибка в ссылке", link="/")
    db = db_session.create_session()
    g = db.query(Group).get(gid)
    db.close()
    if g is None:
        return render_template("error.html", text="Такого класса не существует", link="/")
    if current_user.role == current_user.TYPE.EDITOR \
            and current_user.allowed_group.id != g.id:
        return render_template("error.html", text="Вам сюда нельзя", link="/")
    return send_html("table.html")


@app.route("/summary/day")
@login_required
def summary_day():
    if current_user.role == current_user.TYPE.EDITOR:
        return render_template("error.html", text="Сюда нельзя", link="/")
    return send_html("table.html")


if __name__ == '__main__':
    main()
