from flask import Blueprint
artiste_bp = Blueprint('artiste', __name__, template_folder='templates')
from . import routes
