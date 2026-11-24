# Fabrique de l'application [Source : TP 4 — create_app ; TP 5 — config_class ; TP 6 — login_manager]
from flask import Flask
from .app import db, login_manager


def create_app(config_class="config.ProductionConfig"):
    app = Flask(__name__)

    # Confg options - Make sure you created a 'config.py' file.
    app.config.from_object(config_class)

    # Initialisation des extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Import des modèles pour qu'ils soient connus au démarrage [Source : TP 2]
    from . import models

    # Enregistrement des blueprints [Source : TP 4 ; TP 6 — auth_bp]
    from monApp.menu import menu_bp
    from monApp.auth import auth_bp
    from monApp.billeterie import billeterie_bp
    from monApp.paiement import paiement_bp
    app.register_blueprint(menu_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(billeterie_bp)
    app.register_blueprint(paiement_bp)

    # Enregistrement des commandes personnalisées [Source : TP 4]
    from .commands import register_commands
    register_commands(app)

    from flask_bootstrap5 import Bootstrap
    Bootstrap(app)

    return app
