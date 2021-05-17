from flask import jsonify
from flask_restful import Resource, abort
from datetime import date, timedelta
from db_init import *
from app_config import current_user


def check_user_is_authenticated():
    if not current_user.is_authenticated:
        abort(401)


class GroupsListResource(Resource):
    def get(self):
        # get summary
        check_user_is_authenticated()

        response_json = []
        today_date = date.today()
        yesterday_date = today_date - timedelta(days=1)

        db = db_session.create_session()
        if current_user.all_groups_allowed():
            groups = db.query(Group).all()
        else:
            groups = [current_user.allowed_group]

        for group in groups:
            group_json = group.get_json()
            group_json["days"] = []
            for dt in [today_date, yesterday_date]:
                day = db.query(Day).filter(Day.group == group, Day.date == dt).first()
                if day is not None:
                    day_json = day.get_json()
                    group_json["days"].append(day_json)
            response_json.append(group_json)

        db.close()
        return jsonify(response_json)


class GroupsResource(Resource):
    def get(self, group_id, dt):
        # get
        check_user_is_authenticated()
        db = db_session.create_session()
        group = db.query(Group).get(group_id)
        if group is None:
            abort(404)
        if not current_user.is_group_allowed(group):
            abort(403)

        group_json = group.get_json(with_students=True)
        group_json["days"] = []

        day = db.query(Day).filter(Day.group == group, Day.date == dt).first()
        if day is not None:
            day_json = day.get_json()
            group_json["days"].append(day_json)

        db.close()
        return group_json


# @api_blueprint.route("/api/day/<int:group_id>", methods=["GET"])
# def get_day(group_id):
#     check_user_is_authenticated()
#     args = GetDayParser.parse_args()
#     db = db_session.create_session()
#     group = db.query(Group).get(group_id)
#     if group is None:
#         abort(404)
#     if current_user.role == current_user.TYPE.EDITOR and current_user.allowed_group_id != group.id:
#         abort(403)
#     day = db.query(Day).filter(Day.group_id == group_id, Day.date == args.date).first()
#     try:
#         absent = day.absent
#         status = OK
#     except AttributeError:
#         absent = []
#         status = EMPTY
#     can_edit = current_user.role == current_user.TYPE.ADMIN \
#                or current_user.role == current_user.TYPE.EDITOR and current_user.allowed_group_id == group.id
#     res = {
#         "can_edit": can_edit,
#         "name": str(group.number) + group.letter,
#         "id": group.id,
#         STATUS: status,
#         "students": [{
#             "name": st.surname + " " + st.name,
#             "id": st.id,
#             "absent": st.id in [a.id for a in absent]
#         } for st in group.students]
#     }
#     db.close()
#     return make_response(jsonify(res), 200)
#
#
# @api_blueprint.route("/api/day/<int:group_id>", methods=["POST"])
# def update_day(group_id):
#     check_user_is_authenticated()
#     args = UpdateDayParser.parse_args()
#     db = db_session.create_session()
#     group = db.query(Group).get(group_id)
#     if group is None:
#         abort(404)
#     if current_user.role == current_user.TYPE.VIEWER \
#             or current_user.role == current_user.TYPE.EDITOR and current_user.allowed_group_id != group.id:
#         abort(403)
#     day = db.query(Day).filter(Day.group_id == group_id, Day.date == args.date).first()
#     if day is None:
#         day = Day()
#         day.date = datetime.strptime(args.date, "%Y-%m-%d")
#         day.group_id = group_id
#         db.add(day)
#     try:
#         ids = list(map(int, args.ids.split(",")))
#     except ValueError:
#         ids = []
#     print(ids)
#     day.absent = []
#     for id in ids:
#         student = db.query(Student).get(int(id))
#         if student is None or student not in group.students:
#             abort(400)
#         day.absent.append(student)
#     db.commit()
#     db.close()
#     return redirect("/")
#
#
# @api_blueprint.route("/api/summary/group/<int:group_id>", methods=["GET"])
# def get_group_summary(group_id):
#     check_user_is_authenticated()
#     db = db_session.create_session()
#     group = db.query(Group).get(group_id)
#     if group is None:
#         abort(404)
#     if current_user.role == current_user.TYPE.EDITOR and current_user.allowed_group_id != group.id:
#         abort(403)
#     today = date.today()
#     td = timedelta(days=1)
#     days = [{
#         "date": (today - (td * i)).strftime("%Y-%m-%d"),
#         "status": '',
#         "students": []
#     } for i in range(50)]
#
#     for i in range(len(days)):
#         dt = days[i]["date"]
#         day = db.query(Day).filter(Day.date == dt, Day.group_id == group_id).first()
#         if day is None:
#             days[i][STATUS] = EMPTY
#         else:
#             days[i][STATUS] = OK
#             days[i]["students"] = [st.surname for st in day.absent]
#     db.close()
#     return make_response(jsonify({
#         "name": str(group.number) + group.letter,
#         "days": days
#     }), 200)
#
#
# @api_blueprint.route("/api/summary/day/<dt>")
# def get_day_summary(dt):
#     check_user_is_authenticated()
#     if current_user.role == current_user.TYPE.EDITOR:
#         abort(403)
#     db = db_session.create_session()
#     groups = [{
#         "id": g.id,
#         "name": str(g.number) + g.letter,
#         "status": '',
#         "students": []
#     } for g in db.query(Group).all()]
#     for i in range(len(groups)):
#         day = db.query(Day).filter(Day.date == dt, Day.group_id == groups[i]["id"]).first()
#         if day is None:
#             groups[i][STATUS] = EMPTY
#         else:
#             groups[i][STATUS] = OK
#             groups[i]["students"] = [st.surname for st in day.absent]
#     db.close()
#     return make_response(jsonify({
#         "date": dt,
#         "groups": groups
#     }), 200)
#
#
# @api_blueprint.route("/api/login", methods=["POST"])
# def login_api():
#     args = LoginParser.parse_args()
#     db = db_session.create_session()
#     user = db.query(User).filter(User.login == args.login).first()
#     db.close()
#     if user:
#         if user.check_password(args.password):
#             login_user(user, True)
#             data = {"msg": "ok"}
#             return make_response(jsonify(data), 200)
#         else:
#             data = {"msg": "wrong password"}
#             return make_response(jsonify(data), 401)
#     else:
#         data = {"msg": "wrong login"}
#         return make_response(jsonify(data), 401)
