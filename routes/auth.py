from flask import Blueprint, request, jsonify
from models import User
from database import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods =["POST"])
def register():
    data = request.get_json()
    user = User(
        email = data["email"],
        password = data["password"],
        full_name = data["full_name"],
        role = data["role"]

    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

@auth_bp.route("/login", methods = ["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email = data["email"], password = data["password"]).first()
    if user:
        return jsonify({"message": "User logged in successfully"})
    return jsonify({"message": "Invalid user"})