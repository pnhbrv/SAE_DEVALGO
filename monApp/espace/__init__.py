from flask import Blueprint
espace_bp = Blueprint('espace', __name__, template_folder='templates')
from . import routes
