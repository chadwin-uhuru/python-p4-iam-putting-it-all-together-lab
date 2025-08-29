from app import app, db, User, Recipe

with app.app_context():  # <-- push app context from Flask app
    # Clear existing data
    Recipe.query.delete()
    User.query.delete()
    db.session.commit()

    # Create users
    user1 = User(username="alice", bio="I love cooking!")
    user1.password = "password1"
    user2 = User(username="bob", bio="I enjoy baking!")
    user2.password = "password2"

    db.session.add_all([user1, user2])
    db.session.commit()

    # Create recipes
    recipe1 = Recipe(
        title="Pancakes",
        instructions="Mix flour, milk, and eggs. Cook on a hot skillet until golden brown on both sides. Serve warm.",
        minutes_to_complete=20,
        user_id=user1.id
    )
    recipe2 = Recipe(
        title="Chocolate Cake",
        instructions="Combine flour, cocoa, sugar, eggs, and butter. Bake at 350F for 30 minutes. Let cool before frosting.",
        minutes_to_complete=45,
        user_id=user2.id
    )

    db.session.add_all([recipe1, recipe2])
    db.session.commit()
    print("Database seeded successfully!")
