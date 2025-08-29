from flask import request, session
from flask_restful import Resource
from models import db, User

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        image_url = data.get("image_url")
        bio = data.get("bio")

        errors = []
        if not username:
            errors.append("Username is required")
        if not password:
            errors.append("Password is required")
        if User.query.filter_by(username=username).first():
            errors.append("Username already taken")
        if errors:
            return {"errors": errors}, 422

        # Create user
        user = User(username=username, password=password, image_url=image_url, bio=bio)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        return {
            "id": user.id,
            "username": user.username,
            "image_url": user.image_url,
            "bio": user.bio
        }, 201
