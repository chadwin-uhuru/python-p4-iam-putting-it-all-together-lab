#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker

from config import app, db
from models import User, Recipe

fake = Faker()

def create_users():
    users = []
    for _ in range(5):
        user = User(
            username=fake.user_name(),
            bio=fake.paragraph(),
            image_url=fake.image_url()
        )
        user.password_hash = 'password'
        users.append(user)
    return users

def create_recipes(users):
    recipes = []
    instructions = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
    Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
    """
    
    for _ in range(10):
        recipe = Recipe(
            title=fake.sentence(),
            instructions=instructions,
            minutes_to_complete=randint(15, 120),
            user_id=rc(users).id
        )
        recipes.append(recipe)
    return recipes

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        User.query.delete()
        Recipe.query.delete()
        
        print("Seeding users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()
        
        print("Seeding recipes...")
        recipes = create_recipes(users)
        db.session.add_all(recipes)
        db.session.commit()
        
        print("Done seeding!")