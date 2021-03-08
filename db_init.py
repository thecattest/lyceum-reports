from data import db_session
import os
import sqlalchemy as sa
from data.__all_models import *


# db_path = os.path.join("db", "reports.sqlite")
db_path = os.path.join("db", "reports")
db_session.global_init(db_path)
