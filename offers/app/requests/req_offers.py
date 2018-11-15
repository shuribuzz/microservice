from motor.motor_asyncio import AsyncIOMotorClient
from sanic import Blueprint, response
from sanic_jwt import exceptions, protected
from sanic.exceptions import ServerError
from time import time
from uuid import uuid4

from config import Config


#инициализация блюпринт в приложении
bp_offer = Blueprint('offers', url_prefix='/offer')

#при старте сервера создаём монгу
@bp_offer.listener('before_server_start')
async def setup_connection(app, loop):
    global db
    client = AsyncIOMotorClient(Config.MONGO_URL, io_loop=loop)
    db = client.microservices_db

#cоздание объявления
@bp_offer.post('/create')
@protected()
async def create(request):
    user_id = request.json.get('user_id')
    title = request.json.get('title')
    text = request.json.get('text')

    user_id = str(user_id)
    title = str(title)
    text = str(text)
    offer_id = str(uuid4())
    created_at = int(time())

    if not title or len(title) < Config.MIN_TITLE or len(title) > Config.MAX_TITLE:
        raise ServerError("Title must be less than 30 and more than 10 characters ", status_code=400)
    elif not text or len(text) < Config.MIN_TEXT or len(text) > Config.MAX_TEXT:
        raise ServerError("Text must be less than 100 and more than 20 characters ", status_code=400)
    elif not user_id:
        raise ServerError("User not found", status_code=400)

    user = await db.users.find_one({'user_id': user_id})

    user['offers_ids'].append(offer_id)
    db.users.update_one({'user_id': user_id}, {"$set": user}, upsert=False)

    await db.offers.insert_one({
        'offer_id': offer_id,
        'user_id': user_id,
        'title': title,
        'text': text,
        'created_at': created_at
    })

    return response.json({'offer_id': offer_id}, status=201)

#получения объявлений
@bp_offer.post('/')
@protected()
async def get_offers(request):
    user_id = request.json.get('user_id')
    offer_id = request.json.get('offer_id')

    if offer_id is not None:
        offer = await db.offers.find_one({'offer_id': offer_id})

        if offer is None :
            raise ServerError("Offer not found", status_code=400)

        return response.json({'user_id': offer.get('user_id'),
                              'title': offer.get('title'),
                              'text': offer.get('text'),
                              'created_at': offer.get('created_at')}, status=201)
    elif user_id is not None:
        offers_list = []
        user = await db.users.find_one({'user_id': user_id})

        if user is None :
            raise ServerError("User not found", status_code=400)

        offers_ids = user.get('offers_ids')
        for offer_id in offers_ids:
            offer = await db.offers.find_one({'offer_id': offer_id})
            offer_dict = {'offer_id': offer.get('offer_id'),
                          'title': offer.get('title'),
                          'text': offer.get('text'),
                          'create_at': offer.get('create_at')}
            offers_list.append(offer_dict)
        return response.json({'offers_list': offers_list})









