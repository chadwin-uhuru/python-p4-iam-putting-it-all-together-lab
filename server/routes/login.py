from flask import request, session
from flask_restful import Resource
from models import User

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.authenticate(username, password)
        if not user:
            return {"errors": ["Invalid username or password"]}, 401

        session["user_id"] = user.id
        return {
            "id": user.id,
            "username": user.username,
            "image_url": user.image_url,
            "bio": user.bio
        }, 200
