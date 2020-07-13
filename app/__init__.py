from flask import Flask, jsonify
from flask_restful import Api

from app.common.error_handling import ObjectNotFound, AppErrorBaseClass
from app.db import db
from app.clasificacion.api_v1.resources import clasificacion_v1
from .ext import ma, migrate


def create_app(DevelopmentConfig):
    app = Flask(__name__)
    #app.config.from_object(DevelopmentConfig)

    #inicializacion de la configuracion(cambiar)

    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'Desarrollo key'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SHOW_SQLALCHEMY_LOG_MESSAGES'] = False
    app.config['ERROR_404_HELP'] = False
    app.config['ERROR_404_HELP'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SHOW_SQLALCHEMY_LOG_MESSAGES'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://desarrollador3:VzXY#FP$AqNI@64.227.98.56:5432/comparas'


    print(app.config['SQLALCHEMY_DATABASE_URI'])
    # Inicializa las extensiones
    db.init_app(app)

    ma.init_app(app)
    migrate.init_app(app, db)

    # Captura todos los errores 404
    Api(app, catch_all_404s=True)

    # Deshabilita el modo estricto de acabado de una URL con /
    app.url_map.strict_slashes = False

    # Registra los blueprints
    app.register_blueprint(clasificacion_v1)

    # Registra manejadores de errores personalizados
    #register_error_handlers(app)

    return app


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return jsonify({'msg': 'aaaaaaaaa Internal server error'}), 500

    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({'msg': 'aaaaaaaaa Method not allowed'}), 405

    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({'msg': 'aaaaaaaaa Forbidden error'}), 403

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({'msg': 'aaaaaaaaa Not Found error'}), 404

    @app.errorhandler(AppErrorBaseClass)
    def handle_app_base_error(e):
        return jsonify({'aaaaaaaaa msg': str(e)}), 500

    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        return jsonify({'aaaaaaaaa msg': str(e)}), 404