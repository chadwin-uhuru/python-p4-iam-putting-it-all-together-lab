from app import app, db
from models import User, Recipe

# --- Connect to app context ---
app.app_context().push()

# --- Reset database ---
db.drop_all()
db.create_all()

# --- Helper to safely create users ---
def create_user(username, password_plain):
    user_fields = User.__table__.columns.keys()  # get all column names
    kwargs = {}
    if "username" in user_fields:
        kwargs["username"] = username
    if "password_hash" in user_fields:
        kwargs["password_hash"] = password_plain  # assuming you hash later or store plaintext for now
    return User(**kwargs)

# --- Create Users ---
user1 = create_user("alice", "password123")
user2 = create_user("bob", "securepass")

db.session.add_all([user1, user2])
db.session.commit()  # commit to assign IDs

# --- Helper to safely create recipes ---
def create_recipe(title, instructions, minutes, user_id):
    recipe_fields = Recipe.__table__.columns.keys()
    kwargs = {}
    if "title" in recipe_fields:
        kwargs["title"] = title
    if "instructions" in recipe_fields:
        kwargs["instructions"] = instructions
    if "minutes_to_complete" in recipe_fields:
        kwargs["minutes_to_complete"] = minutes
    if "user_id" in recipe_fields:
        kwargs["user_id"] = user_id
    return Recipe(**kwargs)

# --- Create Recipes ---
recipe1 = create_recipe(
    "Spaghetti Carbonara",
    "Cook pasta. Fry bacon. Mix eggs and cheese. Combine all ingredients.",
    25,
    user1.id
)

recipe2 = create_recipe(
    "Avocado Toast",
    "Toast bread. Mash avocado. Spread on toast. Season with salt and pepper.",
    10,
    user2.id
)

recipe3 = create_recipe(
    "Chicken Curry",
    "Cook chicken. Add spices. Simmer with coconut milk. Serve with rice.",
    45,
    user1.id
)

db.session.add_all([recipe1, recipe2, recipe3])
db.session.commit()

print("✅ Database seeded successfully!")
