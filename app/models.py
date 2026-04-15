from app.extensions import mongo
from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Request:
    @staticmethod
    def to_dict(item):
        return {
            "id": str(item["_id"]),
            "timestamp": item["timestamp"], 
            "req_addr":item["req_addr"],
            "method": item["method"],
            "scheme": item["scheme"],
            "path":item["path"],
            "status":item["status"],
            "header":item["header"],
            "data":item["data"],
            "url":item["url"],
            "exception":item["exception"],
        }
