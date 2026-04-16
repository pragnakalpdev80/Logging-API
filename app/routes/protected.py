from flask import Blueprint, jsonify
from flask_limiter.util import get_remote_address
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, set_access_cookies,unset_jwt_cookies
from app.extensions import limiter, auth_limiter
from app.models.request import Request

protected_bp = Blueprint('protected', __name__)


@protected_bp.route('/', methods=['GET'])
def home():
    return jsonify({"detail":"Hello"}),200

@protected_bp.route("/protected", methods=["GET"])
@auth_limiter.limit("10/hour")
@limiter.limit("2/hour")
@jwt_required()
def get_items():
    return jsonify({"detail":"Hello"}),200
