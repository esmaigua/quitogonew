from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from sqlalchemy import text
import jwt
import datetime
import os

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400
    
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409
    
    hashed = generate_password_hash(data["password"])
    new_user = User(
        email=data["email"], 
        password=hashed, 
        is_admin=data.get("is_admin", False)
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400
    
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401
    
    # CAMBIO: Usar "id" en lugar de "user_id" y "token" en lugar de "access_token"
    token = jwt.encode({
        "id": user.id,  # CAMBIO: "id" en lugar de "user_id"
        "email": user.email,
        "is_admin": user.is_admin,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, os.getenv("SECRET_KEY"), algorithm="HS256")
    
    # CAMBIO: Retornar "token" en lugar de "access_token"
    return jsonify({"token": token}), 200

@auth_bp.route("/me", methods=["GET"])
def me():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token required"}), 401
    
    token = auth_header.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 403
    
    # CAMBIO: Usar "id" en lugar de "user_id" para compatibilidad
    return jsonify({
        "id": payload["id"],  # CAMBIO: "id" en lugar de "user_id"
        "email": payload["email"],
        "is_admin": payload["is_admin"]
    })

@auth_bp.route("/health", methods=["GET"])
def health():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500