#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        json_data = request.get_json()

        try:
            user = User(
                username=json_data.get('username'),
                image_url=json_data.get('image_url'),
                bio=json_data.get('bio')
            )

            user.password_hash = json_data.get('password')

            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id

            return make_response(user.to_dict(), 201)

        except (IntegrityError, ValueError) as err:
            return {'errors': [str(err)]}, 422


class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return make_response(user.to_dict(), 200)
        else:
            return {'errors': ['Unauthorized']}, 401


class Login(Resource):
    def post(self):
        json_data = request.get_json()
        
        user = User.query.filter(User.username == json_data.get('username')).first()

        if user and user.authenticate(json_data.get('password')):
            session['user_id'] = user.id
            return make_response(user.to_dict(), 200)
        else:
            return {'errors': ['Unauthorized']}, 401


class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {}, 204
        else:
            return {'errors': ['Unauthorized']}, 401


class RecipeIndex(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'errors': ['Unauthorized']}, 401

        recipes = Recipe.query.all()
        return [recipe.to_dict() for recipe in recipes], 200

    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'errors': ['Unauthorized']}, 401

        json_data = request.get_json()
        user = User.query.get(user_id)

        try:
            recipe = Recipe(
                title=json_data.get('title'),
                instructions=json_data.get('instructions'),
                minutes_to_complete=json_data.get('minutes_to_complete'),
                user=user
            )

            db.session.add(recipe)
            db.session.commit()
            return make_response(recipe.to_dict(), 201)
        except (IntegrityError, ValueError) as err:
            return {'errors': [str(err)]}, 422

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')

if __name__ == '__main__':
    app.run(port=5555, debug=True)