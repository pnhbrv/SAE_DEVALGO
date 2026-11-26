from monApp.app import db
from monApp.commands import hacher
from monApp.models import AvoirStyle, Groupe, PreferenceStyle, Spectateur, StyleMusical
from monApp.recommandation import cache
from tests.functional import login


def remplir_base(testapp):
    with testapp.app_context():
        for id_style, libelle in [(1, "Rock"), (2, "Pop")]:
            unStyle = StyleMusical(libelle_style=libelle)
            unStyle.set_id_style(id_style)
            db.session.add(unStyle)
        for id_groupe, nom, id_style in [(1, "Groupe rock", 1), (2, "Groupe pop", 2)]:
            unGroupe = Groupe(nom_groupe=nom)
            unGroupe.set_id_groupe(id_groupe)
            db.session.add(unGroupe)
            db.session.add(AvoirStyle(id_groupe=id_groupe, id_style=id_style))
        db.session.add(Spectateur(nom="Leroy", prenom="Emma", email="emma@mail.com", mot_de_passe=hacher("emma")))
        db.session.commit()
    cache.invalider()


def test_mes_styles_demande_une_connexion(client):
    response = client.get('/mes-styles/', follow_redirects=True)
    assert response.request.path == "/connexion/"


def test_mes_styles_affiche_les_styles(client, testapp):
    remplir_base(testapp)
    login(client, "emma@mail.com", "emma", "")
    response = client.get('/mes-styles/')
    assert response.status_code == 200
    assert b"Rock" in response.data
    assert b'name="note_2"' in response.data


def test_enregistrer_puis_modifier_puis_retirer_une_note(client, testapp):
    remplir_base(testapp)
    login(client, "emma@mail.com", "emma", "")
    response = client.post('/mes-styles/', data={"note_1": "5", "note_2": "-2"}, follow_redirects=True)
    assert "enregistrés".encode() in response.data
    with testapp.app_context():
        assert PreferenceStyle.query.filter_by(id_spectateur=1, id_style=1).first().note == 5
        assert PreferenceStyle.query.filter_by(id_spectateur=1, id_style=2).first().note == -2

    client.post('/mes-styles/', data={"note_1": "3", "note_2": ""})
    with testapp.app_context():
        assert PreferenceStyle.query.filter_by(id_spectateur=1, id_style=1).first().note == 3
        assert PreferenceStyle.query.filter_by(id_spectateur=1, id_style=2).first() is None


def test_une_note_invalide_n_est_pas_enregistree(client, testapp):
    remplir_base(testapp)
    login(client, "emma@mail.com", "emma", "")
    client.post('/mes-styles/', data={"note_1": "0", "note_2": "12"})
    with testapp.app_context():
        assert PreferenceStyle.query.count() == 0


def test_suggestions_sur_la_page_artistes(client, testapp):
    remplir_base(testapp)
    login(client, "emma@mail.com", "emma", "")
    response = client.get('/artistes/')
    assert "Suggestions selon vos goûts".encode() not in response.data

    client.post('/mes-styles/', data={"note_1": "5", "note_2": "-2"})
    page = client.get('/artistes/').data.decode()
    debut = page.index("Suggestions selon vos goûts")
    fin = page.index("Nombre d'artistes")
    assert "Groupe rock" in page[debut:fin]
    assert "Groupe pop" not in page[debut:fin]

    # avec une recherche ou un filtre, on n'affiche que les résultats
    response = client.get('/artistes/?recherche=groupe')
    assert "Suggestions selon vos goûts".encode() not in response.data


def test_mes_concerts_conseilles_sans_preference(client, testapp):
    remplir_base(testapp)
    login(client, "emma@mail.com", "emma", "")
    response = client.get('/mes-concerts-conseilles/')
    assert response.status_code == 200
    assert "pas encore noté de style".encode() in response.data
