from flask import Flask, render_template, request, redirect, make_response, session, abort, jsonify
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
    app.run(host='0.0.0.0', port=port)
    # app.run()


if __name__ == '__main__':
    main()
