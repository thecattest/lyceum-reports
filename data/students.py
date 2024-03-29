import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Student(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'students'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=False)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))

    group = orm.relation("Group")
    days = orm.relation("Day",
                        secondary="students_to_days")

    def __repr__(self):
        return f"<Student {self.id} {self.surname} {self.name}>"
