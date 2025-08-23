from flask import Flask, request, jsonify, session
from flask_migrate import Migrate
from models import db, bcrypt, User, Recipe

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///iam_lab.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "this-is-a-secret-key"

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)

# ----------------- Routes -----------------

# SIGNUP
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    image_url = data.get("image_url")
    bio = data.get("bio")

    if not username or not password:
        return jsonify({"errors": ["Username and password required"]}), 422

    if User.query.filter_by(username=username).first():
        return jsonify({"errors": ["Username already exists"]}), 422

    user = User(username=username, image_url=image_url, bio=bio)
    user.password = password
    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.id
    return jsonify(user.to_dict()), 201


# CHECK SESSION
@app.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"errors": ["Unauthorized"]}), 401

    user = User.query.get(user_id)
    return jsonify(user.to_dict()), 200


# LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.authenticate(password):
        session["user_id"] = user.id
        return jsonify(user.to_dict()), 200

    return jsonify({"errors": ["Invalid username or password"]}), 401


# LOGOUT
@app.route("/logout", methods=["DELETE"])
def logout():
    if "user_id" in session:
        session.pop("user_id")
        return "", 204
    return jsonify({"errors": ["Unauthorized"]}), 401


# GET & CREATE RECIPES
@app.route("/recipes", methods=["GET", "POST"])
def recipes():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"errors": ["Unauthorized"]}), 401

    if request.method == "GET":
        recipes = Recipe.query.all()
        return jsonify([r.to_dict() for r in recipes]), 200

    if request.method == "POST":
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
            return jsonify({"errors": errors}), 422

        recipe = Recipe(
            title=title,
            instructions=instructions,
            minutes_to_complete=minutes_to_complete,
            user_id=user_id
        )
        db.session.add(recipe)
        db.session.commit()
        return jsonify(recipe.to_dict()), 201


if __name__ == "__main__":
    app.run(debug=True)
