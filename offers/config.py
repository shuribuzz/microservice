import os

class Config:
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', 8001))
    MONGO_URL = os.getenv('MONGO_URL', '127.0.0.1:27017')
    MIN_TITLE = int(os.getenv('MIN_TITLE', 10))
    MAX_TITLE = int(os.getenv('MAX_TITLE', 30))
    MIN_TEXT = int(os.getenv('MIN_TEXT', 20))
    MAX_TEXT = int(os.getenv('MAX_TEXT', 100))