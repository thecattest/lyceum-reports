from flask import Blueprint, jsonify, make_response, abort, redirect
from datetime import date, timedelta, datetime
from db_init import *
from request_parsers import GetDayParser, UpdateDayParser
from app_config import current_user


api_blueprint = Blueprint("api", __name__,
                          template_folder="templates")

STATUS = 'status'
OK = 'ok'
EMPTY = 'empty'


def check_user_authenticated():
    if not current_user.is_authenticated:
        return False, make_response(jsonify({"error": "not authenticated"}), 403)
    return True, None


@api_blueprint.route("/api/summary")
def get_summary():
    ok, response = check_user_authenticated()
    if not ok:
        return response
    db = db_session.create_session()
    if current_user.role == current_user.TYPE.ADMIN or current_user.role == current_user.TYPE.VIEWER:
        groups = db.query(Group).all()
    else:
        groups = [current_user.allowed_group]
    summary = []
    today = date.today()
    yesterday = today - timedelta(days=1)

    def get_absent(group, dt):
        day = {
            "date": dt.strftime("%Y-%m-%d")
        }
        try:
            absent = db.query(Day).filter(Day.group == group, Day.date == dt).first().absent
            day[STATUS] = OK
            day["students"] = [st.surname for st in absent]
        except AttributeError:
            day[STATUS] = EMPTY
        return day

    for g in groups:
        group_json = g.to_dict(only=('id', 'number', 'letter'))
        days = {
            "today": get_absent(g, today),
            "yesterday": get_absent(g, yesterday)
        }
        group_json["days"] = days
        summary.append(group_json)
    response = {
        "summary": summary, 
        "user_role": current_user.role,
        "roles": {
            current_user.TYPE.NAMES.ADMIN: current_user.TYPE.ADMIN,
            current_user.TYPE.NAMES.VIEWER: current_user.TYPE.VIEWER,
            current_user.TYPE.NAMES.EDITOR: current_user.TYPE.EDITOR
        }
    }
    return make_response(jsonify(response), 200)

    
@api_blueprint.route("/api/day/<int:group_id>", methods=["GET"])
def get_day(group_id):
    ok, response = check_user_authenticated()
    if not ok:
        return response
    args = GetDayParser.parse_args()
    db = db_session.create_session()
    group = db.query(Group).get(group_id)
    if group is None:
        abort(404)
    day = db.query(Day).filter(Day.group_id == group_id, Day.date == args.date).first()
    try:
        absent = day.absent
        status = OK
    except AttributeError:
        absent = []
        status = EMPTY

    return make_response(jsonify({
        "name": str(group.number) + group.letter,
        "id": group.id,
        STATUS: status,
        "students": [{
            "name": st.surname + " " + st.name,
            "id": st.id,
            "absent": st.id in [a.id for a in absent]
        } for st in group.students]
    }), 200)


@api_blueprint.route("/api/day/<int:group_id>", methods=["POST"])
def update_day(group_id):
    ok, response = check_user_authenticated()
    if not ok:
        return response
    args = UpdateDayParser.parse_args()
    db = db_session.create_session()
    group = db.query(Group).get(group_id)
    if group is None:
        abort(404)
    day = db.query(Day).filter(Day.group_id == group_id, Day.date == args.date).first()
    if day is None:
        day = Day()
        day.date = datetime.strptime(args.date, "%Y-%m-%d")
        day.group_id = group_id
        db.add(day)
    try:
        ids = list(map(int, args.ids.split(",")))
    except ValueError:
        ids = []
    print(ids)
    day.absent = []
    for id in ids:
        student = db.query(Student).get(int(id))
        if student is None or student not in group.students:
            abort(400)
        day.absent.append(student)
    db.commit()
    return redirect("/")


@api_blueprint.route("/api/summary/group/<int:group_id>", methods=["GET"])
def get_group_summary(group_id):
    ok, response = check_user_authenticated()
    if not ok:
        return response
    db = db_session.create_session()
    group = db.query(Group).get(group_id)
    if group is None:
        abort(404)
    today = date.today()
    td = timedelta(days=1)
    days = [{
        "date": (today-(td*i)).strftime("%Y-%m-%d"),
        "status": '',
        "students": []
    } for i in range(50)]

    for i in range(len(days)):
        dt = days[i]["date"]
        day = db.query(Day).filter(Day.date == dt, Day.group_id == group_id).first()
        if day is None:
            days[i][STATUS] = EMPTY
        else:
            days[i][STATUS] = OK
            days[i]["students"] = [st.surname for st in day.absent]
    return make_response(jsonify({
        "name": str(group.number) + group.letter,
        "days": days
    }), 200)


@api_blueprint.route("/api/summary/day/<dt>")
def get_day_summary(dt):
    ok, response = check_user_authenticated()
    if not ok:
        return response
    db = db_session.create_session()
    groups = [{
        "id": g.id,
        "name": str(g.number) + g.letter,
        "status": '',
        "students": []
    } for g in db.query(Group).all()]
    for i in range(len(groups)):
        day = db.query(Day).filter(Day.date == dt, Day.group_id == groups[i]["id"]).first()
        if day is None:
            groups[i][STATUS] = EMPTY
        else:
            groups[i][STATUS] = OK
            groups[i]["students"] = [st.surname for st in day.absent]
    return make_response(jsonify({
        "date": dt,
        "groups": groups
    }), 200)
