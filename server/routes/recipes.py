from flask import request, session
from flask_restful import Resource
from models import db, Recipe, User

class RecipeIndex(Resource):
    def get(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"errors": ["Not logged in"]}, 401

        recipes = Recipe.query.all()
        recipes_data = []
        for r in recipes:
            recipes_data.append({
                "id": r.id,
                "title": r.title,
                "instructions": r.instructions,
                "minutes_to_complete": r.minutes_to_complete,
                "user": {
                    "id": r.user.id,
                    "username": r.user.username,
                    "image_url": r.user.image_url,
                    "bio": r.user.bio
                }
            })
        return recipes_data, 200

    def post(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"errors": ["Not logged in"]}, 401

        data = request.get_json()
        title = data.get("title")
        instructions = data.get("instructions")
        minutes_to_complete = data.get("minutes_to_complete")

        errors = []
        if not title:
            errors.append("Title is required")
        if not instructions or len(instructions) < 50:
            errors.append("Instructions must be at least 50 characters")

        if errors:
            return {"errors": errors}, 422

        recipe = Recipe(
            title=title,
            instructions=instructions,
            minutes_to_complete=minutes_to_complete,
            user_id=user_id
        )
        db.session.add(recipe)
        db.session.commit()

        return {
            "id": recipe.id,
            "title": recipe.title,
            "instructions": recipe.instructions,
            "minutes_to_complete": recipe.minutes_to_complete,
            "user": {
                "id": recipe.user.id,
                "username": recipe.user.username,
                "image_url": recipe.user.image_url,
                "bio": recipe.user.bio
            }
        }, 201
