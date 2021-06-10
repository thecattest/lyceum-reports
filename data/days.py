import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from flask_restful import reqparse

from datetime import datetime


association_table = sqlalchemy.Table('students_to_days', SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('student', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('students.id')),
                                     sqlalchemy.Column('day', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('days.id'))
                                     )


class Day(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'days'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.Date, unique=False, nullable=False)
    updated = sqlalchemy.Column(sqlalchemy.DateTime, unique=False, nullable=False, default=datetime.now)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))

    group = orm.relation("Group")
    absent = orm.relation("Student",
                          secondary="students_to_days")

    def get_json(self):
        day_json = self.to_dict(only=('id', 'date', 'group_id'))
        day_json["absent"] = []
        for absent in self.absent:
            day_json["absent"].append(absent.get_json())
        return day_json

    @staticmethod
    def get_parser():
        parser = reqparse.RequestParser()
        parser.add_argument("group_id", type=str)
        parser.add_argument("date", type=str)
        parser.add_argument("absent", action='append')
        return parser

    def __repr__(self):
        return f"<Day {self.id} {self.date}>"
