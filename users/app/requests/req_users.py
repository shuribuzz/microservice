from motor.motor_asyncio import AsyncIOMotorClient
from sanic import Blueprint, response
from sanic_jwt import exceptions
from sanic.exceptions import ServerError
from time import time
from uuid import uuid4

from config import Config


#инициализация блюпринт в приложении
bp_user = Blueprint('users', url_prefix='/user')

#при старте сервера создаём подключение к экземпляру монги, расположенному на хосте Config.MONGO_URL
@bp_user.listener('before_server_start')
async def setup_connection(app, loop):
    global db
    client = AsyncIOMotorClient(Config.MONGO_URL, io_loop=loop)
    db = client.microservices_db

#регистрация пользователя
@bp_user.post("/registry")
async def register(request):
    username = request.json.get('username')
    password = request.json.get('password')

    username = str(username)
    password = str(password)
    user_id = str(uuid4())
    created_at = int(time())

    if not username or len(username) < Config.MIN_USERNAME or len(username) > Config.MAX_USERNAME:
        raise ServerError("Name must be less than 16 and more than 3 characters ", status_code=400)
    elif not password or len(password) < Config.MIN_PASSWORD or len(password) > Config.MAX_PASSWORD:
        raise ServerError("Password must be less than 16 and more than 8 characters ", status_code=400)
    elif await db.users.find_one({'username': username}):
        raise ServerError("This user is already in use", status_code=400)

    await db.users.insert_one({
        'user_id': user_id,
        'username': username,
        'password': password,
        'created_at': created_at,
        'offers_ids': []})

    return response.json({'user_id': user_id}, status=201)

#авторизация пользователя
async def authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")


    user = await db.users.find_one({'username': username})
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if password != user.get('password'):
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user

#получение пользователя
@bp_user.get("/<user_id>/")
async def get_user(request, user_id):
    user_id = str(user_id)

    user = await db.users.find_one({'user_id': user_id})

    if user is None:
        raise ServerError("User not found", status_code=400)

    return response.json({"username": user.get("username"),
                          "created_at": user.get("created_at"),
                          "offers_ids": user.get("offers_ids")}, status=200)
