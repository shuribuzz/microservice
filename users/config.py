import os

class Config:
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', 8000))
    MONGO_URL = os.getenv('MONGO_URL', '127.0.0.1:27017')
    MIN_USERNAME = int(os.getenv('MIN_USERNAME', 3))
    MAX_USERNAME = int(os.getenv('MAX_USERNAME', 16))
    MIN_PASSWORD = int(os.getenv('MIN_PASSWORD', 8))
    MAX_PASSWORD = int(os.getenv('MAX_PASSWORD', 16))