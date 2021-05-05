import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

from hashlib import md5
from werkzeug.security import check_password_hash, generate_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String(100), unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String(95), nullable=True)
    notes = sqlalchemy.Column(sqlalchemy.String(300), unique=False, nullable=True)
    role = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)

    allowed_group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))
    allowed_group = orm.relation("Group")

    def __init__(self):
        self.role = User.TYPE.EDITOR

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"<User {self.id} {self.login} {self.notes} {self.role}>"

    class TYPE:
        ADMIN = 1
        VIEWER = 2
        EDITOR = 3

        class NAMES:
            ADMIN = "admin"
            EDITOR = "editor"
            VIEWER = "viewer"
