from monApp.app import db
from monApp.commands import hacher
from monApp.models import Groupe, Spectateur
from tests.functional import login


def ajouter_comptes(testapp):
    with testapp.app_context():
        db.session.add(Spectateur(nom="Leroy", prenom="Emma", email="emma@mail.com", mot_de_passe=hacher("emma")))
        db.session.add(Spectateur(nom="Festiuto", prenom="Admin", email="admin@mail.com",
                                  mot_de_passe=hacher("admin"), est_admin=True))
        db.session.add(Groupe(nom_groupe="Muse"))
        db.session.commit()


def test_admin_before_login(client):
    response = client.get('/admin/')
    # vérifier redirection vers page Login
    assert response.status_code == 302
    assert "/connexion/?next=%2Fadmin%2F" in response.headers["Location"]


def test_admin_interdit_a_un_spectateur(client, testapp):
    ajouter_comptes(testapp)
    login(client, "emma@mail.com", "emma", "")
    response = client.get('/admin/')
    assert response.status_code == 403


def test_admin_after_login(client, testapp):
    ajouter_comptes(testapp)
    response = login(client, "admin@mail.com", "admin", "/admin/")
    assert response.status_code == 200
    assert response.request.path == "/admin/"
    assert b"Tableau de bord" in response.data
    assert b"Espace Administrateur" in response.data
    # un groupe et un seul spectateur (l'admin n'est pas compté)
    assert response.data.count(b"<td>1</td>") == 2


def test_lien_espace_admin_seulement_pour_l_admin(client, testapp):
    ajouter_comptes(testapp)
    login(client, "emma@mail.com", "emma", "")
    response = client.get('/artistes/')
    assert b'href="/admin/"' not in response.data
    client.get('/deconnexion/')

    login(client, "admin@mail.com", "admin", "")
    response = client.get('/artistes/')
    assert b'href="/admin/"' in response.data
