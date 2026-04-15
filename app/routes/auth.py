from flask import Blueprint, request, jsonify
from app.services.user_service import UserValidation

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
    print(request.json())
    # auth, error, status = UserValidation.login_validation(request.get_json())
    # if error:
    #     print(error)
    #     return jsonify({"error": error}), status
 
    # return jsonify(auth) ,status
    return jsonify({"detail":"hello"}),200
