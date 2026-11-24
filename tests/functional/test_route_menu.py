def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "Le Festival phare d'Orléans".encode() in response.data
    assert b"navbar-festiuto" not in response.data
    assert b'href="/compte/"' in response.data


def test_index_connecte(client, testapp):
    from monApp.app import db
    from monApp.commands import hacher
    from monApp.models import Spectateur
    from tests.functional import login
    with testapp.app_context():
        db.session.add(Spectateur(nom="Leroy", prenom="Emma", email="emma@mail.com", mot_de_passe=hacher("emma")))
        db.session.commit()
    response = login(client, "emma@mail.com", "emma", "/index/")
    assert response.request.path == "/index/"
    assert b"navbar-festiuto" in response.data
    assert "Réservez Maintenant".encode() not in response.data


def test_index_slash(client):
    response = client.get('/index/')
    assert response.status_code == 200
