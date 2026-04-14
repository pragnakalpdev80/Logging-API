import os
from dotenv import load_dotenv

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/flaskdb")