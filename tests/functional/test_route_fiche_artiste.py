import datetime
from monApp.app import db
from monApp.artiste.routes import lien_video_integree
from monApp.models import (AvoirStyle, Composer, EstSimilaire, Evenement, Groupe, Instrument, Jouer, Journee, Lieu,
                           Membre, Participer, StyleMusical)
from monApp.recommandation import groupes_similaires


def ajouter_groupe(id_groupe, nom, id_style):
    unGroupe = Groupe(nom_groupe=nom, description="Description de " + nom,
                      liens_videos="https://www.youtube.com/watch?v=abc123",
                      liens_reseaux_sociaux="https://www.instagram.com/" + nom)
    unGroupe.set_id_groupe(id_groupe)
    db.session.add(unGroupe)
    db.session.add(AvoirStyle(id_groupe=id_groupe, id_style=id_style))


def remplir_base(testapp):
    # Rock (1) > Punk (2) ; Jazz (3)
    with testapp.app_context():
        for id_style, libelle, parent in [(1, "Rock", None), (2, "Punk", 1), (3, "Jazz", None)]:
            unStyle = StyleMusical(libelle_style=libelle, id_style_parent=parent)
            unStyle.set_id_style(id_style)
            db.session.add(unStyle)
        ajouter_groupe(1, "Muse", 1)
        ajouter_groupe(2, "Green Day", 2)
        ajouter_groupe(3, "Miles", 3)
        ajouter_groupe(4, "Indochine", 1)

        unMembre = Membre(nom="Bellamy", prenom="Matt")
        unMembre.set_id_membre(1)
        unInstrument = Instrument(libelle_instrument="Guitare")
        unInstrument.set_id_instrument(1)
        db.session.add_all([unMembre, unInstrument])
        db.session.add(Composer(id_membre=1, id_groupe=1))
        db.session.add(Jouer(id_membre=1, id_instrument=1))

        jour = datetime.date(2026, 10, 10)
        db.session.add(Journee(date_jour=jour, heure_debut_officielle=datetime.time(14, 0),
                               heure_fin_officielle=datetime.time(4, 0)))
        unLieu = Lieu(nom_lieu="Zénith", adresse="Orléans", jauge_max=100)
        unLieu.set_id_lieu(1)
        db.session.add(unLieu)
        unEvenement = Evenement(titre="Concert Muse", type_evenement="Concert",
                                date_heure_debut=datetime.datetime(2026, 10, 10, 21, 0), duree=90,
                                est_gratuit=False, est_public=True, date_jour=jour, id_lieu=1)
        unEvenement.set_id_evenement(1)
        db.session.add(unEvenement)
        db.session.add(Participer(id_groupe=1, id_evenement=1))
        # l'organisateur a déclaré Miles similaire à Muse
        db.session.add(EstSimilaire(id_groupe=1, id_groupe_similaire=3))
        db.session.commit()


def noms(groupes):
    resultat = []
    for unGroupe in groupes:
        resultat.append(unGroupe.nom_groupe)
    return resultat


def test_fiche_d_un_groupe(client, testapp):
    remplir_base(testapp)
    response = client.get('/artistes/1/')
    assert response.status_code == 200
    page = response.data.decode()
    assert "Muse" in page
    assert "Description de Muse" in page
    assert "Matt Bellamy" in page
    assert "Guitare" in page
    assert "Concert Muse" in page
    assert "Zénith" in page
    assert "https://www.youtube.com/embed/abc123" in page
    assert "https://www.instagram.com/Muse" in page


def test_fiche_d_un_groupe_inconnu(client, testapp):
    remplir_base(testapp)
    response = client.get('/artistes/999/')
    assert response.status_code == 404


def test_les_cartes_menent_a_la_fiche(client, testapp):
    remplir_base(testapp)
    response = client.get('/artistes/')
    assert b'href="/artistes/1/"' in response.data


def test_groupes_similaires(testapp):
    remplir_base(testapp)
    with testapp.app_context():
        muse = Groupe.query.filter_by(id_groupe=1).first()
        # Miles est déclaré similaire, puis l'algo ajoute Indochine (même style : 5)
        # et Green Day (sous-genre du Rock : 5 / (1+1) = 2.5)
        assert noms(groupes_similaires(muse)) == ["Miles", "Indochine", "Green Day"]
        assert noms(groupes_similaires(muse, nombre=2)) == ["Miles", "Indochine"]


def test_lien_video_integree():
    assert lien_video_integree("https://www.youtube.com/watch?v=abc123") == "https://www.youtube.com/embed/abc123"
    assert lien_video_integree("https://www.youtube.com/watch?v=abc123&t=10") == "https://www.youtube.com/embed/abc123"
    assert lien_video_integree("https://www.youtube.com/results?search_query=Adele") is None
    assert lien_video_integree(None) is None
