from flask import Flask
import settings
from exts import *
from apps.user.view import user_bp
from apps.article.view import article_bp
config = {
    'CACHE_TYPE' : 'REDIS',
    'CACHE_REDIS_HOST':'192.168.52.100',
    'CACHE_REDIS_PORT' : 6379
}


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    #配置
    app.config.from_object(settings.Development)
    #蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(article_bp)
    #数据库
    db.init_app(app)

    cahe.init_app(app=app,config=config)

    bs.init_app(app=app)

    return app