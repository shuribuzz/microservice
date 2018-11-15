from sanic import Sanic
from sanic_jwt import Initialize
from app.requests import bp_offer



def getapp():
    app = Sanic(__name__)

    # инициализируем экземпляр саник
    Initialize(app,
               cookie_set=True,
               cookie_strict=False,
               auth_mode=False
               )
    # зарегистрируем экземпляр блюпринта в приложении
    app.blueprint(bp_offer)

    return app