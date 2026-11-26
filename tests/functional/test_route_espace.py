from monApp.app import db
from monApp.commands import hacher
from monApp.models import PreferenceStyle, Spectateur, StyleMusical
from tests.functional import login


def preparer(testapp):
    with testapp.app_context():
        db.session.add_all([Spectateur(nom="Leroy", prenom="Emma", email="emma@mail.com", mot_de_passe=hacher("emma")),
                            StyleMusical("Pop"), StyleMusical("Metal")])
        db.session.commit()


def test_espace_non_connecte(client):
    response = client.get('/espace/')
    assert response.status_code == 302
    assert '/connexion/' in response.headers['Location']


def test_espace_connecte(client, testapp):
    preparer(testapp)
    login(client, "emma@mail.com", "emma", "")
    response = client.get('/espace/')
    assert response.status_code == 200
    assert b"Bonjour Emma Leroy" in response.data
    assert b"Mes styles pr" in response.data


def test_modifier_styles(client, testapp):
    preparer(testapp)
    login(client, "emma@mail.com", "emma", "")
    assert client.get('/espace/styles/').status_code == 200
    response = client.post('/espace/styles/', data={'note_1': 4, 'note_2': -3}, follow_redirects=True)
    assert b"Pop" in response.data and b"Metal" in response.data
    with testapp.app_context():
        assert PreferenceStyle.query.get((1, 1)).note == 4
        assert PreferenceStyle.query.get((1, 2)).note == -3
    client.post('/espace/styles/', data={'note_1': 0, 'note_2': -3})
    with testapp.app_context():
        assert PreferenceStyle.query.get((1, 1)) is None
