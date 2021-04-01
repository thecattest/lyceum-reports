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
