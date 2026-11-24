# Configuration des tests [Source : TP 1 ; TP 2 — runner ; TP 5 — base de test]
import pytest
from monApp import create_app
from monApp.app import db


@pytest.fixture
def testapp():
    app = create_app("config.TestingConfig")
    with app.app_context():
        db.create_all()  # creation de la structure de la base de données
    yield app


@pytest.fixture
def client(testapp):
    return testapp.test_client()


@pytest.fixture
def runner(testapp):
    return testapp.test_cli_runner()
