from sanic import Sanic
from sanic_jwt import Initialize
from app.requests import bp_user, authenticate


def getapp():
    app = Sanic(__name__)

    # инициализируем sanic-jwt
    Initialize(app,
               authenticate=authenticate,
               url_prefix='/user/auth',
               auth_mode=True,
               cookie_set=True,
               cookie_strict=False
               )
    # зарегистрируем экземпляр блюпринта в приложении
    app.blueprint(bp_user)

    return app