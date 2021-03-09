from data import db_session
import os
import sqlalchemy as sa
from data.__all_models import *


# db_path = os.path.join("db", "reports.sqlite")
db_path = "reports"

try:
    with open("db_config") as f:
        username, password = f.readline().split()
except FileNotFoundError:
    raise FileNotFoundError("Create file with name db_config in root with username and password to "
                            "database separated with space")
else:
    db_session.global_init(db_path, username, password)
