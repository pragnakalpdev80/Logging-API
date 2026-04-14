from flask import Flask, jsonify
from app.extensions import mongo
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)

    @app.route('/', methods=['GET'])
    def home():
        return jsonify({'data': 'connected!'})

    return app
   