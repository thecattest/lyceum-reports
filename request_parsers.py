from flask_restful import reqparse


GetDayParser = reqparse.RequestParser()
# GetDayParser.add_argument("group_id", required=True, type=int)
GetDayParser.add_argument("date", required=True, type=str)

UpdateDayParser = reqparse.RequestParser()
UpdateDayParser.add_argument("date", required=True, type=str)
UpdateDayParser.add_argument("ids", type=str)

LoginParser = reqparse.RequestParser()
LoginParser.add_argument("login", required=True, type=str)
LoginParser.add_argument("password", required=True, type=str)
