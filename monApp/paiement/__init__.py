from flask import Blueprint

paiement_bp = Blueprint('paiement', __name__, template_folder='templates')

from . import routes
