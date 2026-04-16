from flask import Flask, jsonify, request, render_template, g
from app.extensions import mongo, migrate, db, jwt, limiter
from bson.objectid import ObjectId
from config import Config
import logging
from time import strftime
from app.models.request import Request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.routes.auth import auth_bp
from app.routes.protected import protected_bp
from flask_limiter.errors import RateLimitExceeded


logger = logging.getLogger(__name__)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(protected_bp)

    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit(e):
        return jsonify({
            "error": "Rate limit exceeded",
            "message": str(e.description),
        }), 429

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "This endpoint does not exist"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "Method not allowed for this endpoint"
        }), 405
    
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit(e):
        return jsonify({
            "error": "Rate limit exceeded",
            "message": str(e.description),
        }), 429
    
    @app.before_request
    def log_request():
        user = None
        try:
            verify_jwt_in_request(optional=True)
            identity = get_jwt_identity()
            if identity is not None:
                user = identity
        except Exception:
            pass
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        requests = {
            "timestamp": timestamp, 
            "user": user,
            "req_addr":request.remote_addr,
            "method": request.method,
            "scheme": request.scheme,
            "path":request.full_path,
            "data":request.get_data(as_text=True),
            "url":request.url,
        }
        requests = mongo.db.requests.insert_one(requests)
        g.id = str(requests.inserted_id)
        
    @app.after_request
    def log_response(response):
        update_data ={"$set": {"status":response.status,"response_data":response.get_data(as_text=True)} }
        mongo.db.requests.update_one({"_id": ObjectId(g.id)}, update_data)
        return response

    @app.teardown_request
    def teardown_request_handler(exception=None):
        """Execute after each request, even on errors"""
        if exception:
            update_data ={"$set": {"exception":exception} }
            mongo.db.requests.update_one({"_id": ObjectId(g.id)}, update_data)


    return app