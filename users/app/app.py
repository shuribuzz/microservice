from sanic import Sanic
from sanic_jwt import initialize
from app.requests import bp_user, authenticate


def getapp():
    app = Sanic(__name__)

    # инициализируем экземпляр саник
    initialize(app,
               authenticate=authenticate,
               url_prefix='/user/auth',
               )
    # зарегистрируем экземпляр блюпринта в приложении
    app.blueprint(bp_user)

    return app