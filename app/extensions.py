from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


db = SQLAlchemy()
migrate =Migrate()
mongo = PyMongo()
jwt = JWTManager()

def get_user_or_ip():
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            return f"user:{identity}"
    except Exception:
        pass
    return get_remote_address()


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per hour"],
    storage_uri="redis://localhost:6379/0",
)

auth_limiter = Limiter(
    key_func=get_user_or_ip,
    default_limits=["10 per hour"],
    storage_uri="redis://localhost:6379/0",
)