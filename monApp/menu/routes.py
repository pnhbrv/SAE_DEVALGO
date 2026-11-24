# Vues du menu (TP 3 et 4)
from flask import render_template
from . import menu_bp


@menu_bp.route('/')
@menu_bp.route('/index/')
def index():
    return render_template("index.html", title="Fest'IUT'O")
