from flask import Flask
from .app import db, login_manager


def create_app(config_class="config.ProductionConfig"):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from . import models

    from monApp.menu import menu_bp
    from monApp.auth import auth_bp
    from monApp.artiste import artiste_bp
    from monApp.espace import espace_bp
    app.register_blueprint(menu_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(artiste_bp)
    app.register_blueprint(espace_bp)

    from .commands import register_commands
    register_commands(app)

    from flask_bootstrap5 import Bootstrap
    Bootstrap(app)

    return app
