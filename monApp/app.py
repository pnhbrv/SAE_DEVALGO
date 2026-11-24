# Extensions partagées par toute l'application
# [Source : TP 2 — SQLAlchemy ; TP 6 — LoginManager et login_view]
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
