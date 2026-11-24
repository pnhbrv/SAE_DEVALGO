# Fichier de configuration (TP 1 et 5)
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "9c1f6a2e-4b7d-4e0a-9f3b-6d2c8e5a7b14"  # générée avec uuidgen (TP 5)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_SERVE_LOCAL = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'monApp.db')


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
