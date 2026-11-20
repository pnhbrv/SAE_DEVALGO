# Vues du menu [Source : TP 3 — render_template ; TP 4 — BluePrint menu]
from flask import render_template
from . import menu_bp


@menu_bp.route('/')
@menu_bp.route('/index/')
def index():
    return render_template("index.html", title="Fest'IUT'O")
