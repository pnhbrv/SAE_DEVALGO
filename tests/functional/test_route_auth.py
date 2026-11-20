# Tests de l'authentification [Source : TP 6 ; TP 5 — tests des formulaires POST]
from monApp.app import db
from monApp.commands import hacher
from monApp.models import Spectateur
from tests.functional import login


def ajouter_comptes(testapp):
    with testapp.app_context():
        db.session.add(Spectateur(nom="Leroy", prenom="Emma", email="emma@mail.com", mot_de_passe=hacher("emma")))
        db.session.commit()


def test_compte(client):
    response = client.get('/compte/')
    assert response.status_code == 200
    assert b"Se connecter" in response.data
    assert "Créer votre compte".encode() in response.data


def test_login_get(client):
    response = client.get('/connexion/?next=/index/')
    assert response.status_code == 200
    assert b'value="/index/"' in response.data


def test_login_spectateur(client, testapp):
    ajouter_comptes(testapp)
    response = login(client, "emma@mail.com", "emma", "")
    assert response.status_code == 200
    assert "Déconnexion".encode() in response.data


def test_login_echec(client, testapp):
    ajouter_comptes(testapp)
    response = login(client, "emma@mail.com", "faux", "")
    assert response.request.path == "/connexion/"
    response = login(client, "inconnu@mail.com", "x", "")
    assert response.request.path == "/connexion/"


def test_logout(client, testapp):
    ajouter_comptes(testapp)
    login(client, "emma@mail.com", "emma", "")
    response = client.get('/deconnexion/', follow_redirects=True)
    assert response.status_code == 200
    assert "Déconnexion".encode() not in response.data
    assert b'href="/compte/"' in response.data


def test_inscription_get(client):
    response = client.get('/inscription/')
    assert response.status_code == 200
    assert b"Bienvenue" in response.data


def test_inscription_post(client, testapp):
    response = client.post('/inscription/', data={"nom": "Faure", "prenom": "Louis", "email": "louis@mail.com",
                                                   "mot_de_passe": "louis"}, follow_redirects=True)
    assert response.request.path == "/connexion/"
    with testapp.app_context():
        unSpectateur = Spectateur.query.filter_by(email="louis@mail.com").first()
        assert unSpectateur.mot_de_passe == hacher("louis")
    response = login(client, "louis@mail.com", "louis", "")
    assert "Déconnexion".encode() in response.data


def test_inscription_email_existant(client, testapp):
    ajouter_comptes(testapp)
    response = client.post('/inscription/', data={"nom": "X", "prenom": "Y", "email": "emma@mail.com",
                                                   "mot_de_passe": "z"})
    assert response.status_code == 200
    assert "Ce mail est déjà utilisé.".encode() in response.data


def test_inscription_champs_vides(client):
    response = client.post('/inscription/', data={})
    assert response.status_code == 200
    assert b"list-group-item-danger" in response.data
