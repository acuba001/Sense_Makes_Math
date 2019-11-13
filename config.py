import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from dotenv import load_dotenv
# from logging.config import dictConfig

# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }},
#     'root': {
#         'level': 'INFO',
#         'handlers': ['wsgi']
#     }
# })

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    DEVELOPMENT = False
    TESTING = False
    STAGING = False
    DEBUG = False

    ADMIN_CONTACT = os.environ.get('ADMIN_CONTACT')
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    # Mail
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SENDER = os.environ.get('MAIL_SENDER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'), base=10)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']

    # security
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SSL_REDIRECT = False

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # Blogger
    BLOGGER_DATA_FETCH_PER_DAY = int(os.environ.get('BLOGGER_DATA_FETCH_PER_DAY', 15))
    BLOGGER_PAGE_BLOG_ID = os.environ.get('BLOGGER_PAGE_BLOG_ID')

    # ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    # Google
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

    # PayPal
    PAYPAL_MODE = os.environ.get('PAYPAL_MODE', 'sandbox')
    PAYPAL_SANDBOX_ACCOUNT = os.environ.get('PAYPAL_SANDBOX_ACCOUNT')
    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
    PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET')

    # Printful
    PRINTFUL_STORE_ID = os.environ.get('PRINTFUL_STORE_ID')
    PRINTFUL_API_KEY = os.environ.get('PRINTFUL_API_KEY')
    PRINTFUL_DATA_FETCH_PER_DAY = int(os.environ.get('PRINTFUL_DATA_FETCH_PER_DAY', 30))
    PRINTFUL_DATA_MAXRESULTS = int(os.environ.get('PRINTFUL_DATA_MAXRESULTS', 100))

    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SSL_REDIRECT = False

    # Spotify
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # YouTube
    YOUTUBE_DATA_FETCH_PER_DAY = int(os.environ.get('YOUTUBE_DATA_FETCH_PER_DAY', 48))
    YOUTUBE_DATA_MAXRESULTS = int(os.environ.get('YOUTUBE_DATA_MAXRESULTS', 30))
    YOUTUBE_CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID')

    @staticmethod
    def init_app(app):
        pass

    @staticmethod
    def configure_stream_logger(app):
        stream_handler = logging.StreamHandler()
        stream_handler_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        stream_handler.setFormatter(stream_handler_formatter)
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
        return None

    @staticmethod
    def configure_file_logger(app):
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/sense_makes_math.log', maxBytes=10240, backupCount=10)
        file_handler_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        file_handler.setFormatter(file_handler_formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('Starting Up Sense Makes Math')
        return None

    # email errors to the administrators
    @classmethod
    def configure_mail_logger(cls, app):
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_SENDER,
            toaddrs=[cls.ADMIN_CONTACT],
            subject='Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        mail_handler.setFormatter(mail_handler_formatter)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        return None


class DevelopmentConfig(Config):
    DEVELOPMENT = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db ', 'data-dev.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        cls.configure_stream_logger(app)


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db', 'data-dev.sqlite')

    WTF_CSRF_ENABLED = False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        cls.configure_file_logger(app)
        cls.configure_stream_logger(app)


class StagingConfig(Config):
    STAGING = True
    DEVELOPMENT = False
    DEBUG = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        cls.configure_mail_logger(app)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db', 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        cls.configure_mail_logger(app)


class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle reverse proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig
}
