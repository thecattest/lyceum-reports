import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Group(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=False)
    letter = sqlalchemy.Column(sqlalchemy.String(3), unique=False, nullable=False)

    students = orm.relation("Student", back_populates="group")
    days = orm.relation("Day", back_populates="group")
    users = orm.relation("User", back_populates="allowed_group")

    def get_json(self, with_students=False):
        group_json = self.to_dict(only=('id', 'number', 'letter'))
        if with_students:
            group_json["students"] = []
            for st in self.students:
                group_json["students"].append(st.get_json())
        return group_json

    def __repr__(self):
        return f"<Group {self.id} {self.number}{self.letter}>"
