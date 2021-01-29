class BaseConfig(object):
    'Configuracion inicial'
    SECRET_KEY = 'Cambiar'
    DEBUG = True
    TESTING = False
    ERROR_404_HELP = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SHOW_SQLALCHEMY_LOG_MESSAGES = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://desarrollador3:VzXY#FP$AqNI@64.227.98.56:5432/comparas'

class AdditionalConfig(object):
    RUTAIMAGENESUSUARIOS = 'http://comparas.pe/imagenes/usuarios/'
    RUTAIMAGENESPRODUCTOS = 'http://comparas.pe/imagenes/productos/'
    RUTAIMAGENESSUPERMERCADOS = 'http://comparas.pe/imagenes/productos/'

    ROL1 = 4    #Comprador
    ROL2 = 3    #Bodeguero
    ROL3 = 2    #Adminstrador

class ProductionConfig(BaseConfig):
    'Configuracion para produccion'
    DEBUG = False
    PROPAGATE_EXCEPTIONS = False
    SECRET_KEY = 'Cambiar con una encriptada'


class DevelopmentConfig(BaseConfig):
    'Configuracion para desarrollo'
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'Desarrollo_key'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SHOW_SQLALCHEMY_LOG_MESSAGES = False
    ERROR_404_HELP = False
