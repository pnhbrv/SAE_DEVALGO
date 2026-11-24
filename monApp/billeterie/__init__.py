from flask import Blueprint

billeterie_bp = Blueprint('billeterie', __name__, template_folder='templates')

from . import routes
