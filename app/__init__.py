from flask import Flask, jsonify
from app.extensions import db, migrate
from config import DevConfig


def create_app(config_class=DevConfig):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
   