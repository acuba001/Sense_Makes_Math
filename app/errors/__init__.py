from flask import Blueprint

bp = Blueprint('errors', __name__)

from . import handlers
from .myErrors import BadApiCallError, BadUrlError, ArithmeticOperationError, TypeMatchError, Error, InternalServerError