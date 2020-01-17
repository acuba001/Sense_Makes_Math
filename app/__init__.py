from flask import Flask, request
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
# from flask_moment import Moment
# from flask_babel import Babel, lazy_gettext as _l
# from flask_pagedown import PageDown

# import os
# import rq
from datetime import datetime as dt
# from elasticsearch import Elasticsearch
# from redis import Redis
from config import config

cache = Cache()
db = SQLAlchemy()
# migrate = Migrate()
mail = Mail()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'
# login.login_message = _l('Please log in to access this page.')
# moment = Moment()
# babel = Babel()
# pagedown = PageDown()


def register_extensions(app):
    cache.init_app(app=app, config={'CACHE_TYPE': app.config['CACHE_TYPE']})
    db.init_app(app)
    # migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    # moment.init_app(app)
    # babel.init_app(app)
    # pagedown.init_app(app)
    # logs.init_app(app)
    # app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    #     if app.config['ELASTICSEARCH_URL'] else None
    # app.redis = Redis.from_url(app.config['REDIS_URL'])
    # app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)

    # if app.config['SSL_REDIRECT']:
    #     from flask_sslify import SSLify
    #     sslify = SSLify(app)
    return None


def register_blueprints(app):
    from .main import main_bp
    app.register_blueprint(main_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    from .errors import errors_bp
    app.register_blueprint(errors_bp)

    return None


def create_app(config_name=None):
    app = Flask(__name__)
    config[config_name].init_app(app)
    app.config.from_object(config[config_name])

    register_extensions(app)

    with app.app_context():
        @app.before_request
        def before_request(request):
# ======================================================
# [NOTE] In app.<component>.init.py...
# 
# Components are captured in a Blueprint and 
# are usable throughout the app. For example,  errors, 
# libraries, main.
#
#   Example 2
# ======================================================
# from flask import Blueprint
# 
# simple_page = Blueprint('simple_page', __name__,
#                         template_folder='templates')
#
# -------------------------------------------------------
            return request

        @app.after_request
        def after_request(response):
            """ Logging after every request. """
            return response

        register_blueprints(app)

# =============================================================================================================================================
# Printful API
#
#
#   SUB                   METHOD        URL                                         PARAMS                      RESPONSE
# =============================================================================================================================================
# Catalog               | GET       | ~/products                                  | NONE            |   { code: 200, result: Product[] }
#                       | GET       | ~/products/variant/{ varId }                | varId           |   { code: 200, result: { var: Variant, prod: Product }}
#                       | GET       | ~/products/{ prodId }                       | prodId          |   { code: 200, result: { prod: Product, var: Variant[] }}
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Products              | GET       | ~/store/products                            | status,         |   { code: 200, result: SyncProduct[], paging: Paging }
#                       |           |                                             | offset,         | 
#                       |           |                                             | limit           |
#                       | POST      | ~/store/products                            | sync_product,   |   { code: 200, result: RequestProductResponse }  
#                       |           |                                             | sync_variants   |  
#                       | GET       | ~/store/products/{ sync_prodId }            | sync_prodId     |   { code: 200, result: { prod: SyncProduct, var: SyncVariant[] }} 
#                       | DELETE    | ~/store/products/{ sync_prodId }            | sync_prodId     |   { code: 200, result: { prod: Product, var: Variant[] }}
#                       | PUT       | ~/store/products/{ sync_prodId }            | sync_product    |   { code: 200, result: RequestProductResponse } 
#                       |           |                                             | sync_variants   |
#                       | POST      | ~/store/products/{ sync_prodId }/variants   | sync_prodId     |   { code: 200, result: RequestVariantResponse }
#                       | GET       | ~/store/variants/{ sync_varId }             | sync_varId      |   { code: 200, result: { prod: SyncVariant, var: SyncProduct }}
#                       | DELETE    | ~/store/variants/{ sync_varId }             | sync_varId      |   { code: 200, result: { prod: SyncVariant, var: SyncProduct }}
#                       | PUT       | ~/store/variants/{ sync_varId }             | sync_varId      |   { code: 200, result: RequestVariantResponse }
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Orders                | GET       | ~/orders                                    | status,         |   { code: 200, result: Order[], paging: Paging }
#                       |           |                                             | offset,         |   
#                       |           |                                             | limit           | 
#                       | POST      | ~/orders                                    | OrderInput,     |   { code: 200, result: Order } 
#                       |           |                                             | confirm,        | 
#                       |           |                                             | update_existing,|
#                       | POST      | ~/orders/estimate-costs                     | OrderInput      |   { code: 200, result: OrderCosts }
#                       | GET       | ~/orders/{ orderId }                        | orderId         |   { code: 200, result: Order}
#                       | DELETE    | ~/orders/{ orderId }                        | orderId         |   { code: 200, result: Order} 
#                       | PUT       | ~/orders/{ orderId }                        | orderId,        |   { code: 200, result: Order} 
#                       |           |                                             | confirm,        |   
#                       |           |                                             | OrderInput      |   
#                       | POST      | ~/orders/{ orderId }/confirm                | orderId         |   { code: 200, result: Order} 
# --------------------------------------------------------------------------------------------------------------------------------------------
# File Library          | GET       | ~/files                                     | status,         |   { code: 200, result: File[], paging: Paging } 
#                       |           |                                             | offset,         |   
#                       |           |                                             | limit           | 
#                       | POST      | ~/files                                     | File            |   { code: 200, result: File }
#                       | GET       | ~/files/{ fileId }                          | fileId          |   { code: 200, result: File }
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Shipping Rate         | POST      | ~/shipping/rates                            | AddressInfo,    |   { code: 200, result: ShippingInfo[] }
#                       |           |                                             | ItemInfo[],     |
#                       |           |                                             | currency        |
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Country/State Code    | GET       | ~/countries                                 | None            |   { code: 200, result: Country[] }
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Tax Rate              | GET       | ~/tax/countries                             | None            |   { code: 200, result: Country[] }   
#                       | POST      | ~/tax/rates                                 | TaxRequest      |   { code: 200, result: TaxInfo }   
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Webhook               |||
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Store Information     ||| 
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Mockup Generator      ||| 
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Warehouse Products    ||| 
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Warehouse Shipments   ||| 
# ---------------------------------------------------------------------------------------------------------------------------------------------
# E-comm Platform Sync  ||| 
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Webhook Simulator     ||| 
# ---------------------------------------------------------------------------------------------------------------------------------------------
        return app
