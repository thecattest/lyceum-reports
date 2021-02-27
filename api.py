from flask import Blueprint, jsonify, make_response, abort, request
from datetime import date, timedelta
from db_init import *
from request_parsers import GetDayParser


api_blueprint = Blueprint("api", __name__,
                          template_folder="templates")


@api_blueprint.route("/api/summary")
def get_summary():
    db = db_session.create_session()
    groups = db.query(Group).all()
    summary = []
    today = date.today()
    yesterday = today - timedelta(days=1)
    for g in groups:
        group_json = g.to_dict(only=('id', 'number', 'letter'))
        group_json["days"] = {
            "today": {"date": today.strftime("%Y-%m-%d")},
            "yesterday": {"date": yesterday.strftime("%Y-%m-%d")}
        }
        try:
            today_absent = db.query(Day).filter(Day.group == g, Day.date == today).first().absent
            group_json["days"]["today"]["status"] = "ok"
            group_json["days"]["today"]["students"] = [st.surname for st in today_absent]
        except AttributeError:
            group_json["days"]["today"]["status"] = "empty"
        try:
            yesterday_absent = db.query(Day).filter(Day.group == g, Day.date == yesterday).first().absent
            group_json["days"]["yesterday"]["status"] = "ok"
            group_json["days"]["yesterday"]["students"] = [st.surname for st in yesterday_absent]
        except AttributeError:
            group_json["days"]["yesterday"]["status"] = "empty"
        summary.append(group_json)
    return make_response(jsonify(summary), 200)


@api_blueprint.route("/api/day/<int:group_id>", methods=["GET"])
def get_day(group_id):
    args = GetDayParser.parse_args()
    db = db_session.create_session()
    group = db.query(Group).get(group_id)
    if group is None:
        abort(404)
    day = db.query(Day).filter(Day.group_id == group_id, Day.date == args.date).first()
    try:
        absent = day.absent
    except AttributeError:
        absent = []

    return make_response(jsonify({
        "name": str(group.number) + group.letter,
        "id": group.id,
        "students": [{
            "name": st.surname + " " + st.name,
            "id": st.id,
            "absent": st.id in [a.id for a in absent]
        } for st in group.students]
    }), 200)


@api_blueprint.route("/api/day", methods=["POST"])
def update_day():
    pass
