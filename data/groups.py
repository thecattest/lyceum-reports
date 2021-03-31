import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
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

    def __repr__(self):
        return f"<Group {self.id} {self.number}{self.letter}>"
