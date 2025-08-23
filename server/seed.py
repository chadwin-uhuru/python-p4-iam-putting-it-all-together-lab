from app import app, db
from models import User, Recipe

with app.app_context():
    print("Deleting all records...")
    Recipe.query.delete()
    User.query.delete()
    db.session.commit()

    print("Creating users...")
    users_data = [
        {"username": "Christina", "password": "password123", "image_url": "http://lewis.com/", "bio": "Other specific data common card."},
        {"username": "James", "password": "password123", "image_url": "http://example.com/james.png", "bio": "Loves cooking."},
        {"username": "Maria", "password": "password123", "image_url": "http://example.com/maria.png", "bio": "Recipe enthusiast."}
    ]

    users = []
    for u in users_data:
        user = User(username=u["username"], image_url=u["image_url"], bio=u["bio"])
        user.password = u["password"]
        db.session.add(user)
        users.append(user)
    db.session.commit()

    print("Creating recipes...")
    recipes_data = [
        {"title": "Pancakes", "instructions": "Mix flour, eggs, milk, and sugar. Cook on skillet until golden brown. Serve with syrup.", "minutes_to_complete": 20, "user": users[0]},
        {"title": "Omelette", "instructions": "Beat eggs, pour into pan, add cheese, fold, and serve. Make sure eggs are fully cooked.", "minutes_to_complete": 10, "user": users[1]},
        {"title": "Chocolate Cake", "instructions": "Combine flour, sugar, cocoa powder, eggs, milk, and butter. Bake at 350°F for 35 minutes. Let it cool and frost.", "minutes_to_complete": 60, "user": users[2]}
    ]

    for r in recipes_data:
        recipe = Recipe(title=r["title"], instructions=r["instructions"], minutes_to_complete=r["minutes_to_complete"], user_id=r["user"].id)
        db.session.add(recipe)

    db.session.commit()
    print("Seeding complete!")
