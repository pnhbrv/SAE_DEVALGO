# Fabrique de l'application (TP 4, 5 et 6)
from flask import Flask
from .app import db, login_manager


def create_app(config_class="config.ProductionConfig"):
    app = Flask(__name__)

    # configuration (config.py)
    app.config.from_object(config_class)

    # Initialisation des extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Import des modèles pour qu'ils soient connus au démarrage (TP 2)
    from . import models

    # Enregistrement des blueprints (TP 4 et 6)
    from monApp.menu import menu_bp
    from monApp.auth import auth_bp
    from monApp.artiste import artiste_bp
    app.register_blueprint(menu_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(artiste_bp)

    # Enregistrement des commandes personnalisées (TP 4)
    from .commands import register_commands
    register_commands(app)

    from flask_bootstrap5 import Bootstrap
    Bootstrap(app)

    return app
