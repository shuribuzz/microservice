from app import getapp
from config import Config


if __name__== '__main__':
    app = getapp()
    app.run(host=Config.HOST,
            port=Config.PORT)