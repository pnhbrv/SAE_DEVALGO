from flask import Blueprint
preference_bp = Blueprint('preference', __name__, template_folder='templates')
from . import routes
