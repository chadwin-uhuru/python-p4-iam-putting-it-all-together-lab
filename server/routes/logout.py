from flask import session
from flask_restful import Resource

class Logout(Resource):
    def delete(self):
        if "user_id" not in session:
            return {"errors": ["Not logged in"]}, 401

        session.pop("user_id")
        return {}, 204
