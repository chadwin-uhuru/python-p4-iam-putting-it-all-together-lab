from flask import session
from flask_restful import Resource
from models import User

class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"errors": ["Not logged in"]}, 401

        user = User.query.get(user_id)
        return {
            "id": user.id,
            "username": user.username,
            "image_url": user.image_url,
            "bio": user.bio
        }, 200
