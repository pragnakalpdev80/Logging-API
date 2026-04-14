import os
from dotenv import load_dotenv

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    load_dotenv()
    SQLALCHEMY_DATABASE_URI=os.getenv('DB_URL')

class DevConfig(Config):
    load_dotenv()
    SQLALCHEMY_DATABASE_URI=os.getenv('DB_URL')
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False