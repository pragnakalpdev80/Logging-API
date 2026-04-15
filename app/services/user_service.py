import hashlib
import re
from flask_jwt_extended import create_access_token,create_refresh_token
from app.models import User
from app.extensions import db


def encrypt_password(password):
    password=hashlib.md5(password.encode()).hexdigest()
    return password

def insert_data(data):
    print(data)
    encrypted_pass=encrypt_password(data["password"])
    user= User(
        email = data["email"],
        username = data["username"],
        password = encrypted_pass,
    )
    db.session.add(user)
    db.session.commit()

class UserValidation:

    @staticmethod
    def register_validation(data):

        if not all([
            data["email"],data["username"],
            data["password"], data["confirm"], 
        ]):
            return None, "All fields required", 400

        if User.query.filter_by(email=data["email"]).first():
            return None, "Email already exists", 400

        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, data["email"]):
            return None, "Invalid Email", 400

        if len(data["password"]) < 6 or len(data["password"]) > 12:
            return None, "Password must be 6-12 chars", 400

        if data["password"] != data["confirm"]:
            return None, "Passwords mismatch", 400

        insert_data(data)

        access_token = create_access_token(identity=data["email"])
        refresh_token = create_refresh_token(identity=data["email"])
        
        return {
            'message': f'User {data["email"]} was created',
            'access_token': access_token,
            'refresh_token': refresh_token
        }, None, 201


    @staticmethod
    def login_validation(data):
        user = User.query.filter_by(email=data["email"]).first()
        if not user:
            return None, "User not found", 404
        if user.password != encrypt_password(data["password"]):
            return None, "Wrong password", 400
        token = create_access_token(identity=str(user.registration_id))
        return {"access_token": token}, None, 200