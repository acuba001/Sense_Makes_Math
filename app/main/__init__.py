from flask import Blueprint

main_bp = Blueprint('main', __name__)  # , template_folder='templates'

from app.main import routes
from app.api.models import Permission


@main_bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
