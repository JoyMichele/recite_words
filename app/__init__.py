from flask import Flask
from flask_cors import CORS
from utils.config import ProductionConfig


def create_app(config_name):
    """
    创建app,Flask实例
    :param config_name:
    :return:
    """
    app = Flask(__name__)  # type:Flask

    # 允许跨域
    CORS(app, supports_credentials=True)

    from app import auth, vocabulary, query, download
    # 加载flask环境配置
    app.config.from_object(ProductionConfig)

    # 注册蓝图
    app.register_blueprint(auth.auth)
    app.register_blueprint(vocabulary.voc)
    app.register_blueprint(query.query)
    app.register_blueprint(download.down)
    return app
