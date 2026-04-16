from flask import Blueprint, request, jsonify
from app.services.user_service import UserValidation
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    auth, error, status = UserValidation.register_validation(request.get_json())
    if error:
        print(error)
        return jsonify({"error": error}), status
 
    return jsonify(auth) ,status

@auth_bp.route('/login', methods=['POST'])
def login():
    auth, error, status = UserValidation.login_validation(request.get_json())
    if error:
        print(error)
        return jsonify({"error": error}), status
 
    return jsonify(auth) ,status

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    auth, error, status = UserValidation.logout_validation(jti)
    if error:
        print(error)
        return jsonify({"error": error}), status
 
    return jsonify(auth) ,status

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    auth, error, status = UserValidation.refresh(current_user)

    if error:
        return jsonify({"error": error}), status
 
    return jsonify(auth) ,status


   
