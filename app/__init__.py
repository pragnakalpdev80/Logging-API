from flask import Flask, jsonify, request, render_template, g
from app.extensions import mongo, migrate, db, jwt
from bson.objectid import ObjectId
from config import Config
import logging
from time import strftime
from app.models import Request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, set_access_cookies,unset_jwt_cookies
from app.routes.auth import auth_bp
from flask_limiter.errors import RateLimitExceeded


logger = logging.getLogger(__name__)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)

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
    
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({"detail":"Hello"})

    @app.route("/items", methods=["GET"])
    def get_items():
        responses = mongo.db.requests.find()
        # return render_template('index.html', responses=responses)
        return jsonify([Request.to_dict(response) for response in responses])

    @app.before_request
    def log_request():
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        requests = {
            "timestamp": timestamp, 
            "req_addr":request.remote_addr,
            "method": request.method,
            "scheme": request.scheme,
            "path":request.full_path,
            "data":request.data,
            "url":request.url,
        }
        requests = mongo.db.requests.insert_one(requests)
        g.id = str(requests.inserted_id)
        
    @app.after_request
    def log_response(response):
        update_data ={"$set": {"status":response.status} }
        mongo.db.requests.update_one({"_id": ObjectId(g.id)}, update_data)
        return response

    @app.teardown_request
    def teardown_request_handler(exception=None):
        """Execute after each request, even on errors"""
        if exception:
            update_data ={"$set": {"exception":exception} }
            mongo.db.requests.update_one({"_id": ObjectId(g.id)}, update_data)
            
    return app