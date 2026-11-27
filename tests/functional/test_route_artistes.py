from monApp.app import db
from monApp.models import Groupe


def ajouter_groupes(testapp):
    with testapp.app_context():
        db.session.add(Groupe(nom_groupe="Angèle"))
        db.session.add(Groupe(nom_groupe="Adele"))
        db.session.commit()


def test_artistes_sans_recherche(client, testapp):
    ajouter_groupes(testapp)
    response = client.get('/artistes/')
    assert response.status_code == 200
    assert "Angèle".encode() in response.data
    assert b"Adele" in response.data
    assert b"liste-artistes" in response.data


def test_artistes_recherche_vide(client, testapp):
    ajouter_groupes(testapp)
    response = client.get('/artistes/?recherche=')
    assert "Angèle".encode() in response.data
    assert b"Adele" in response.data


def test_artistes_recherche(client, testapp):
    ajouter_groupes(testapp)
    response = client.get('/artistes/?recherche=ang')
    assert "Angèle".encode() in response.data
    assert b"Adele" not in response.data


def test_artistes_aucun(client, testapp):
    response = client.get('/artistes/?recherche=zzz')
    assert "Aucun artiste trouvé".encode() in response.data


def ajouter_donnees_filtres(testapp):
    from datetime import date, datetime, time
    from monApp.models import AvoirStyle, Evenement, Journee, Lieu, Participer, StyleMusical
    with testapp.app_context():
        db.session.add_all([StyleMusical("Rock"), StyleMusical("Metal", 1), StyleMusical("Pop"),
                            Groupe(nom_groupe="Gojira"), Groupe(nom_groupe="Angèle"),
                            Journee(date(2026, 10, 10), time(14), time(4)), Journee(date(2026, 10, 11), time(14), time(4)),
                            Lieu("CO'Met", "Orléans", 100), Lieu("Zénith", "Orléans", 100)])
        db.session.commit()
        db.session.add_all([AvoirStyle(id_groupe=1, id_style=2), AvoirStyle(id_groupe=2, id_style=3),
                            Evenement("Concert Gojira", "Concert", datetime(2026, 10, 10, 20), 60,
                                      est_gratuit=True, date_jour=date(2026, 10, 10), id_lieu=1),
                            Evenement("Concert Angèle", "Concert", datetime(2026, 10, 11, 20), 60,
                                      est_gratuit=False, date_jour=date(2026, 10, 11), id_lieu=2)])
        db.session.commit()
        db.session.add_all([Participer(id_groupe=1, id_evenement=1), Participer(id_groupe=2, id_evenement=2)])
        db.session.commit()


def test_artistes_filtres_affiches(client, testapp):
    ajouter_donnees_filtres(testapp)
    response = client.get('/artistes/')
    for texte in ["Filtres", "Style", "Prix", "Date", "Lieu", "Rock", "Gratuit", "10/10/2026", "Zénith"]:
        assert texte.encode() in response.data
    assert b"style=2" in response.data


def test_artistes_filtre_style_sous_genres(client, testapp):
    ajouter_donnees_filtres(testapp)
    response = client.get('/artistes/?style=1')
    assert b"Gojira" in response.data
    assert "Angèle".encode() not in response.data


def test_artistes_filtres_prix_date_lieu(client, testapp):
    ajouter_donnees_filtres(testapp)
    response = client.get('/artistes/?prix=gratuit')
    assert b"Gojira" in response.data and "Angèle".encode() not in response.data
    response = client.get('/artistes/?date=2026-10-11')
    assert "Angèle".encode() in response.data and b"Gojira" not in response.data
    response = client.get('/artistes/?lieu=1')
    assert b"Gojira" in response.data and "Angèle".encode() not in response.data


def test_artistes_filtre_invalide(client, testapp):
    response = client.get('/artistes/?date=nimporte&lieu=abc')
    assert response.status_code == 200


def test_artistes_plusieurs_filtres(client, testapp):
    ajouter_donnees_filtres(testapp)
    response = client.get('/artistes/?style=1&prix=gratuit')
    assert b"Gojira" in response.data and "Angèle".encode() not in response.data
    response = client.get('/artistes/?style=1&prix=payant')
    assert "Aucun artiste trouvé".encode() in response.data


def test_artistes_liens_gardent_les_filtres(client, testapp):
    ajouter_donnees_filtres(testapp)
    response = client.get('/artistes/?style=1')
    assert b'href="/artistes/?style=1&amp;prix=gratuit"' in response.data
