from flask import Flask, render_template, request, redirect, make_response, session, abort, jsonify, Response
from flask_cors import CORS

from db_init import *
from api import api_blueprint

import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'lyceum_reports_the_best'
CORS(app)


def main():
    app.register_blueprint(api_blueprint)

    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    # from waitress import serve
    # serve(app, host=host, port=port)
    app.run(host=host, port=port)


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
