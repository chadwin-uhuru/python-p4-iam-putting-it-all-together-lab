from flask import Flask, request, session
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, bcrypt, User, Recipe

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'
CORS(app, supports_credentials=True)

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)  # <-- add migrate

with app.app_context():
    db.create_all()


# --------- Signup ---------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    image_url = data.get("image_url", "")
    bio = data.get("bio", "")

    if not username or not password:
        return {"errors": ["Username and password required"]}, 422

    if User.query.filter_by(username=username).first():
        return {"errors": ["Username already exists"]}, 422

    new_user = User(username=username, image_url=image_url, bio=bio)
    new_user.password = password
    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id
    return new_user.to_dict(), 201


# --------- Login ---------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.authenticate(username, password)
    if not user:
        return {"error": "Invalid credentials"}, 401

    session["user_id"] = user.id
    return user.to_dict(), 200


# --------- Check Session ---------
@app.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "Not logged in"}, 401

    user = User.query.get(user_id)
    return user.to_dict(), 200


# --------- Logout ---------
@app.route("/logout", methods=["DELETE"])
def logout():
    if "user_id" in session:
        session.pop("user_id")
        return "", 204
    return {"error": "Not logged in"}, 401


# --------- Recipes ---------
@app.route("/recipes", methods=["GET", "POST"])
def recipes():
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "Unauthorized"}, 401

    if request.method == "GET":
        all_recipes = Recipe.query.all()
        return {"recipes": [r.to_dict() for r in all_recipes]}, 200

    # POST - create new recipe
    data = request.get_json()
    title = data.get("title")
    instructions = data.get("instructions")
    minutes_to_complete = data.get("minutes_to_complete")

    errors = []
    if not title:
        errors.append("Title is required")
    if not instructions or len(instructions) < 50:
        errors.append("Instructions must be at least 50 characters")
    if not minutes_to_complete:
        errors.append("Minutes to complete is required")

    if errors:
        return {"errors": errors}, 422

    new_recipe = Recipe(
        title=title,
        instructions=instructions,
        minutes_to_complete=minutes_to_complete,
        user_id=user_id
    )
    db.session.add(new_recipe)
    db.session.commit()
    return new_recipe.to_dict(), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
