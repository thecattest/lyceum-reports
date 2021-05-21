from flask import jsonify
from flask_restful import Resource, abort
from datetime import date, timedelta, datetime
from db_init import *
from app_config import current_user
from json import loads
from request_parsers import LoginParser
from app_config import current_user, login_user


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
            group_json = group.get_json(True)
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
        # get group day
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
        return jsonify(group_json)


class DaysListResource(Resource):
    def post(self):
        # update group day
        check_user_is_authenticated()
        args = Day.get_parser().parse_args()

        db = db_session.create_session()
        group = db.query(Group).get(args.group_id)
        if group is None:
            abort(404)
        if not current_user.is_group_allowed(group):
            abort(403)

        day = db.query(Day).filter(Day.group_id == args.group_id, Day.date == args.date).first()
        if day is None:
            day = Day()
            day.date = datetime.strptime(args.date, "%Y-%m-%d")
            day.group_id = args.group_id
            db.add(day)

        day.absent = []
        if args.absent:
            for student_json in args.absent:
                student_obj = loads(student_json.replace("'", '"'))
                student = db.query(Student).get(student_obj["id"])
                if student is None or student not in group.students:
                    abort(400)
                day.absent.append(student)

        db.commit()
        db.close()


class DaysResource(Resource):
    def get(self, dt):
        # get day summary
        check_user_is_authenticated()
        if current_user.role == current_user.TYPE.EDITOR:
            abort(403)
        db = db_session.create_session()
        groups = [g.get_json(True) for g in db.query(Group).all()]
        for i in range(len(groups)):
            day = db.query(Day).filter(Day.date == dt, Day.group_id == groups[i]["id"]).first()
            if day is not None:
                groups[i]["days"] = [day.get_json()]
        db.close()
        return jsonify(groups)


class PermissionsResource(Resource):
    def post(self):
        # login and get user permissions
        args = LoginParser.parse_args()
        db = db_session.create_session()
        user = db.query(User).filter(User.login == args.login).first()
        db.close()
        if user:
            if user.check_password(args.password):
                login_user(user, True)
                return jsonify({
                    "can_edit": user.can_edit(),
                    "can_view_table": user.can_view_table()
                })
            else:
                abort(401)
        else:
            abort(401)
