# Tests de la page d'accueil (TP 1)
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "Le Festival phare d'Orléans".encode() in response.data
    # visiteur : pas de bande violette, le bouton mène à la page compte (connexion / inscription)
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
    # connecté : la bande violette revient, le bouton n'est plus affiché
    assert response.request.path == "/index/"
    assert b"navbar-festiuto" in response.data
    assert "Réservez Maintenant".encode() not in response.data


def test_index_slash(client):
    response = client.get('/index/')
    assert response.status_code == 200


def test_index_lien_artistes(client, testapp):
    # connecté, le bouton « Artiste » de l'accueil mène à la liste des artistes (TP 4 et 6)
    from monApp.app import db
    from monApp.commands import hacher
    from monApp.models import Spectateur
    from tests.functional import login
    with testapp.app_context():
        db.session.add(Spectateur(nom="Leroy", prenom="Emma", email="emma@mail.com", mot_de_passe=hacher("emma")))
        db.session.commit()
    response = login(client, "emma@mail.com", "emma", "/index/")
    assert b'href="/artistes/">Artiste</a>' in response.data
    response = client.get('/artistes/')
    assert response.status_code == 200
    assert b"liste-artistes" in response.data
