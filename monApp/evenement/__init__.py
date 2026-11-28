from flask import Blueprint

evenement_bp = Blueprint('evenement', __name__, template_folder='templates')

from . import routes
