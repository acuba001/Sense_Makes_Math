from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app=app)

from app.main import bp as main_bp
from app.errors import bp as errors_bp

app.register_blueprint(main_bp)
app.register_blueprint(errors_bp)