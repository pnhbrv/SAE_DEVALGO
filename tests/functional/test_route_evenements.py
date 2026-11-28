from datetime import date, datetime, time
from monApp.app import db
from monApp.models import AvoirStyle, Evenement, Groupe, Journee, Lieu, Participer, StyleMusical


def ajouter_donnees_evenements(testapp):
    with testapp.app_context():
        db.session.add_all([
            StyleMusical("Rock"),
            StyleMusical("Rap", None),
            StyleMusical("Trap", 2),
            Groupe(nom_groupe="Werenoi"),
            Groupe(nom_groupe="Gojira"),
            Journee(date(2026, 10, 14), time(14), time(4)),
            Journee(date(2026, 10, 15), time(14), time(4)),
            Lieu("Pont de l'Europe", "Orléans", 5000),
            Lieu("CO'Met", "Orléans", 9500),
        ])
        db.session.commit()
        db.session.add_all([
            AvoirStyle(id_groupe=1, id_style=3),
            AvoirStyle(id_groupe=2, id_style=1),
            Evenement(
                "Concert d'hommage", "Concert", datetime(2026, 10, 14, 19, 30), 180,
                est_gratuit=False, est_public=True, date_jour=date(2026, 10, 14), id_lieu=1,
            ),
            Evenement(
                "Show Metal", "Concert", datetime(2026, 10, 15, 21, 0), 90,
                est_gratuit=True, est_public=True, date_jour=date(2026, 10, 15), id_lieu=2,
            ),
            Evenement(
                "Balance privée", "Balance", datetime(2026, 10, 14, 16, 0), 30,
                est_gratuit=True, est_public=False, date_jour=date(2026, 10, 14), id_lieu=1,
            ),
        ])
        db.session.commit()
        db.session.add_all([
            Participer(id_groupe=1, id_evenement=1),
            Participer(id_groupe=2, id_evenement=2),
        ])
        db.session.commit()


def test_evenements_liste(client, testapp):
    ajouter_donnees_evenements(testapp)
    response = client.get('/evenements/')
    assert response.status_code == 200
    assert b"Werenoi" in response.data
    assert b"Concert d&#39;hommage" in response.data or b"Concert d'hommage" in response.data
    assert b"Mercredi 14 octobre 19:30 - 22:30" in response.data
    assert b"Inscription payante" in response.data
    assert b"Inscription gratuite" in response.data
    assert b"Pont de l&#39;Europe" in response.data or b"Pont de l'Europe" in response.data
    assert "Balance privée".encode() not in response.data


def test_evenements_recherche_groupe_titre_style(client, testapp):
    ajouter_donnees_evenements(testapp)
    response = client.get('/evenements/?recherche=werenoi')
    assert b"Werenoi" in response.data
    assert b"Gojira" not in response.data

    response = client.get('/evenements/?recherche=hommage')
    assert b"Werenoi" in response.data
    assert b"Gojira" not in response.data

    response = client.get('/evenements/?recherche=trap')
    assert b"Werenoi" in response.data
    assert b"Gojira" not in response.data


def test_evenements_aucun(client, testapp):
    response = client.get('/evenements/?recherche=zzz')
    assert response.status_code == 200
    assert "Aucun événement trouvé".encode() in response.data


def test_evenements_filtres_affiches(client, testapp):
    ajouter_donnees_evenements(testapp)
    response = client.get('/evenements/')
    for texte in ["Filtres", "Style", "Prix", "Date", "Lieu", "Rock", "Gratuit", "14/10/2026", "CO'Met"]:
        assert texte.encode() in response.data or texte.replace("'", "&#39;").encode() in response.data
    assert b"style=3" in response.data


def test_evenements_filtre_style_sous_genres(client, testapp):
    ajouter_donnees_evenements(testapp)
    response = client.get('/evenements/?style=2')
    assert b"Werenoi" in response.data
    assert b"Gojira" not in response.data


def test_evenements_filtres_prix_date_lieu(client, testapp):
    ajouter_donnees_evenements(testapp)
    response = client.get('/evenements/?prix=gratuit')
    assert b"Gojira" in response.data and b"Werenoi" not in response.data

    response = client.get('/evenements/?date=2026-10-14')
    assert b"Werenoi" in response.data and b"Gojira" not in response.data

    response = client.get('/evenements/?lieu=2')
    assert b"Gojira" in response.data and b"Werenoi" not in response.data


def test_evenements_filtre_invalide(client, testapp):
    response = client.get('/evenements/?date=nimporte&lieu=abc')
    assert response.status_code == 200


def test_evenements_plusieurs_filtres_et_liens(client, testapp):
    ajouter_donnees_evenements(testapp)
    response = client.get('/evenements/?style=2&prix=payant')
    assert b"Werenoi" in response.data and b"Gojira" not in response.data

    response = client.get('/evenements/?style=2&prix=gratuit')
    assert "Aucun événement trouvé".encode() in response.data

    response = client.get('/evenements/?style=2')
    assert b'href="/evenements/?style=2&amp;prix=gratuit"' in response.data


def test_evenements_conseilles_spectateur_connecte(client, testapp):
    from monApp.commands import hacher
    from monApp.models import PreferenceStyle, Spectateur
    from monApp.recommandation import cache

    ajouter_donnees_evenements(testapp)
    with testapp.app_context():
        db.session.add(Spectateur("Dupont", "Jean", "jean@test.fr", hacher("secret")))
        db.session.commit()
        db.session.add(PreferenceStyle(id_spectateur=1, id_style=2, note=5))
        db.session.commit()
    cache.invalider()

    client.post('/connexion/', data={'Login': 'jean@test.fr', 'Password': 'secret'})
    response = client.get('/evenements/')
    assert response.status_code == 200
    assert "Concerts conseillés selon vos goûts".encode() in response.data

    response_filtre = client.get('/evenements/?prix=gratuit')
    assert "Concerts conseillés selon vos goûts".encode() not in response_filtre.data
