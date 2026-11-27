import datetime
from monApp.app import db
from monApp.commands import hacher
from monApp.models import (Acheter, DateAchat, Evenement, Groupe, Journee, Lieu, MettreEnFavori, PreferenceStyle,
                           PreInscrire, Spectateur, StyleMusical, TypeBillet)
from tests.functional import login


def remplir_base(testapp):
    with testapp.app_context():
        db.session.add(Spectateur(nom="Leroy", prenom="Emma", email="emma@mail.com", mot_de_passe=hacher("emma")))
        unStyle = StyleMusical(libelle_style="Rock")
        unStyle.set_id_style(1)
        db.session.add(unStyle)
        for id_groupe, nom in [(1, "Muse"), (2, "Indochine")]:
            unGroupe = Groupe(nom_groupe=nom)
            unGroupe.set_id_groupe(id_groupe)
            db.session.add(unGroupe)
        unType = TypeBillet(libelle="Pass festival", prix=79.99)
        unType.set_id_type_billet(1)
        db.session.add(unType)
        db.session.add(DateAchat(date_achat=datetime.datetime(2026, 6, 1, 9, 0)))
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
        db.session.commit()


def remplir_espace_d_emma(testapp):
    with testapp.app_context():
        db.session.add(Acheter(id_spectateur=1, id_type_billet=1, date_achat=datetime.datetime(2026, 6, 1, 9, 0)))
        db.session.add(PreInscrire(id_spectateur=1, id_evenement=1))
        db.session.add(PreferenceStyle(id_spectateur=1, id_style=1, note=5))
        db.session.add(MettreEnFavori(id_spectateur=1, id_groupe=1))
        db.session.commit()


def test_mon_espace_demande_une_connexion(client):
    response = client.get('/mon-espace/', follow_redirects=True)
    assert response.request.path == "/connexion/"


def test_mon_espace_vide(client, testapp):
    remplir_base(testapp)
    login(client, "emma@mail.com", "emma", "")
    page = client.get('/mon-espace/').data.decode()
    assert "Bonjour Emma" in page
    assert "emma@mail.com" in page
    assert "pas encore de billet" in page
    assert "aucun concert" in page
    assert "pas encore noté de style" in page
    assert "pas encore de groupe favori" in page


def test_mon_espace_rempli(client, testapp):
    remplir_base(testapp)
    remplir_espace_d_emma(testapp)
    login(client, "emma@mail.com", "emma", "")
    page = client.get('/mon-espace/').data.decode()
    assert "Pass festival" in page
    assert "01/06/2026" in page
    assert "Concert Muse" in page
    assert "Rock : +5" in page
    assert 'href="/artistes/1/"' in page
    assert 'href="/artistes/2/"' not in page


def test_le_lien_mon_espace_dans_le_menu(client, testapp):
    remplir_base(testapp)
    login(client, "emma@mail.com", "emma", "")
    response = client.get('/artistes/')
    assert b'href="/mon-espace/"' in response.data


def test_ajouter_puis_retirer_un_favori(client, testapp):
    remplir_base(testapp)
    login(client, "emma@mail.com", "emma", "")
    page = client.get('/artistes/2/').data.decode()
    assert "Ajouter à mes favoris" in page

    page = client.post('/artistes/2/favori/', follow_redirects=True).data.decode()
    assert "Indochine est ajouté à vos favoris" in page
    assert "Retirer de mes favoris" in page
    with testapp.app_context():
        assert MettreEnFavori.query.filter_by(id_spectateur=1, id_groupe=2).first() is not None

    page = client.post('/artistes/2/favori/', follow_redirects=True).data.decode()
    assert "Indochine est retiré de vos favoris" in page
    with testapp.app_context():
        assert MettreEnFavori.query.filter_by(id_spectateur=1, id_groupe=2).first() is None


def test_pas_de_bouton_favori_si_deconnecte(client, testapp):
    remplir_base(testapp)
    page = client.get('/artistes/2/').data.decode()
    assert "Ajouter à mes favoris" not in page
    response = client.post('/artistes/2/favori/', follow_redirects=True)
    assert response.request.path == "/connexion/"
