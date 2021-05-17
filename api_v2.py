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
            group_json = group.to_dict(only=('id', 'number', 'letter'))
            group_json["days"] = []
            for dt in [today_date, yesterday_date]:
                day = db.query(Day).filter(Day.group == group, Day.date == dt).first()
                if day:
                    day_json = day.to_dict(only=('id', 'date', 'group_id'))
                    day_json["absent"] = []
                    for absent in day.absent:
                        day_json["absent"].append(absent.to_dict(only=('id', 'surname', 'name')))
                    group_json["days"].append(day_json)
            response_json.append(group_json)

        db.close()
        return jsonify(response_json)
