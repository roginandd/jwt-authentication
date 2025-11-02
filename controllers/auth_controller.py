from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)

auth_bp = Blueprint('auth_bp', __name__)

# Dummy user
default_user = {
    "username": "roginand",
    "password": "gwapo123"
}

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == default_user["username"] and password == default_user["password"]:
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200
    else:
        return jsonify(msg="Invalid credentials"), 401


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
