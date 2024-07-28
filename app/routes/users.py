from flask import Blueprint, request, jsonify
from app.models import mongo, User
from app.utils.validation import validate_user
from flask_jwt_extended import jwt_required

bp = Blueprint('users', __name__)

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    errors = validate_user(data)
    if errors:
        return jsonify(errors), 400
    user = User(**data)
    mongo.db.users.insert_one(user.to_dict())
    return jsonify({"message": "User created successfully"}), 201

@bp.route('/users/<email>', methods=['GET'])
@jwt_required()
def get_user(email):
    user = mongo.db.users.find_one({"email": email})
    if user:
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404
