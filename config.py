import os
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    @staticmethod
    def init_app(app):
        pass

    #########################
    #   REQUIRED SETTINGS   #
    #########################
    ADMIN_CONTACT = os.environ.get('ADMIN_CONTACT')

    # Blogger
    BLOGGER_PAGE_BLOG_ID = os.environ.get('BLOGGER_PAGE_BLOG_ID')

    # ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    # Google
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

    # # Mail
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # MAIL_SENDER = os.environ.get('MAIL_SENDER')

    # PayPal
    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
    PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET')

    # Printful
    PRINTFUL_STORE_ID = os.environ.get('PRINTFUL_STORE_ID')
    PRINTFUL_API_KEY = os.environ.get('PRINTFUL_API_KEY')

    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SSL_REDIRECT = False

    # Spotify
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # YouTube
    YOUTUBE_CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID')

    #########################
    #   OPTIONAL SETTINGS   #
    #########################

    # Blogger
    BLOGGER_DATA_FETCH_PER_DAY = int(os.environ.get('BLOGGER_DATA_FETCH_PER_DAY', 15))

    # Cache
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')

    # Mail
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'), base=10)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']

    # PayPal
    PAYPAL_MODE = os.environ.get('PAYPAL_MODE', 'sandbox')

    # Printful
    PRINTFUL_DATA_FETCH_PER_DAY = int(os.environ.get('PRINTFUL_DATA_FETCH_PER_DAY', 30))
    PRINTFUL_DATA_MAXRESULTS = int(os.environ.get('PRINTFUL_DATA_MAXRESULTS', 100))

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # or \'sqlite:///' + os.path.join(basedir, 'app.db')

    # YouTube
    YOUTUBE_DATA_FETCH_PER_DAY = int(os.environ.get('YOUTUBE_DATA_FETCH_PER_DAY', 48))
    YOUTUBE_DATA_MAXRESULTS = int(os.environ.get('YOUTUBE_DATA_MAXRESULTS', 30))
    YOUTUBE_DATA_FETCH_PER_DAY = int(os.environ.get('YOUTUBE_DATA_FETCH_PER_DAY') or 48)
    YOUTUBE_DATA_MAXRESULTS = int(os.environ.get('YOUTUBE_DATA_MAXRESULTS') or 10)

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    @classmethod
    def init_app(cls, app):
        cls.configure_stdout_logger(app)


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'
    WTF_CSRF_ENABLED = False
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        cls.configure_file_logger(app)
        cls.configure_stdout_logger(app)


class StagingConfig(Config):
    pass
    # DEVELOPMENT = False
    # DEBUG = True


class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        cls.configure_mail_logger(app)


class HerokuConfig(ProductionConfig):
    #     SSL_REDIRECT = True if os.environ.get('DYNO') else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        # # handle reverse proxy server headers
        # from werkzeug.contrib.fixers import ProxyFix
        # app.wsgi_app = ProxyFix(app.wsgi_app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig
}
