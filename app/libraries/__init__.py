from flask import Blueprint

bp = Blueprint('libraries', __name__)

from app.libraries.response_formator import strip_html, myResponse
