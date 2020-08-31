from config.configuration import DevelopmentConfig
from app import create_app


#settings_module = os.getenv('APP_SETTINGS_MODULE')
#app = create_app(settings_module)flask
config = DevelopmentConfig

app = create_app(config)


