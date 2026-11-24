# Tests unitaires des modèles (TP 2)
import datetime
import decimal
from monApp.models import *

def test_membre_init_getters_setters():
    obj = Membre(nom="Texte", prenom="Texte")
    assert obj.get_nom() == "Texte"
    assert obj.get_prenom() == "Texte"
    obj.set_id_membre(5)
    assert obj.get_id_membre() == 5
    obj.set_nom("Texte")
    assert obj.get_nom() == "Texte"
    obj.set_prenom("Texte")
    assert obj.get_prenom() == "Texte"
    assert repr(obj).startswith("<Membre (")

def test_instrument_init_getters_setters():
    obj = Instrument(libelle_instrument="Texte")
    assert obj.get_libelle_instrument() == "Texte"
    obj.set_id_instrument(5)
    assert obj.get_id_instrument() == 5
    obj.set_libelle_instrument("Texte")
    assert obj.get_libelle_instrument() == "Texte"
    assert repr(obj).startswith("<Instrument (")

def test_groupe_init_getters_setters():
    obj = Groupe(nom_groupe="Texte", description="Texte long", liens_photos="Texte long", liens_reseaux_sociaux="Texte long", liens_videos="Texte long", date_heure_arrivee=datetime.datetime(2026, 10, 10, 14, 0), date_heure_depart=datetime.datetime(2026, 10, 10, 14, 0))
    assert obj.get_nom_groupe() == "Texte"
    assert obj.get_description() == "Texte long"
    assert obj.get_liens_photos() == "Texte long"
    assert obj.get_liens_reseaux_sociaux() == "Texte long"
    assert obj.get_liens_videos() == "Texte long"
    assert obj.get_date_heure_arrivee() == datetime.datetime(2026, 10, 10, 14, 0)
    assert obj.get_date_heure_depart() == datetime.datetime(2026, 10, 10, 14, 0)
    obj.set_id_groupe(5)
    assert obj.get_id_groupe() == 5
    obj.set_nom_groupe("Texte")
    assert obj.get_nom_groupe() == "Texte"
    obj.set_description("Texte long")
    assert obj.get_description() == "Texte long"
    obj.set_liens_photos("Texte long")
    assert obj.get_liens_photos() == "Texte long"
    obj.set_liens_reseaux_sociaux("Texte long")
    assert obj.get_liens_reseaux_sociaux() == "Texte long"
    obj.set_liens_videos("Texte long")
    assert obj.get_liens_videos() == "Texte long"
    obj.set_date_heure_arrivee(datetime.datetime(2026, 10, 10, 14, 0))
    assert obj.get_date_heure_arrivee() == datetime.datetime(2026, 10, 10, 14, 0)
    obj.set_date_heure_depart(datetime.datetime(2026, 10, 10, 14, 0))
    assert obj.get_date_heure_depart() == datetime.datetime(2026, 10, 10, 14, 0)
    assert repr(obj).startswith("<Groupe (")

def test_stylemusical_init_getters_setters():
    obj = StyleMusical(libelle_style="Texte", id_style_parent=5)
    assert obj.get_libelle_style() == "Texte"
    assert obj.get_id_style_parent() == 5
    obj.set_id_style(5)
    assert obj.get_id_style() == 5
    obj.set_libelle_style("Texte")
    assert obj.get_libelle_style() == "Texte"
    obj.set_id_style_parent(5)
    assert obj.get_id_style_parent() == 5
    assert repr(obj).startswith("<StyleMusical (")

def test_typebillet_init_getters_setters():
    obj = TypeBillet(libelle="Texte", prix=decimal.Decimal("19.99"))
    assert obj.get_libelle() == "Texte"
    assert obj.get_prix() == decimal.Decimal("19.99")
    obj.set_id_type_billet(5)
    assert obj.get_id_type_billet() == 5
    obj.set_libelle("Texte")
    assert obj.get_libelle() == "Texte"
    obj.set_prix(decimal.Decimal("19.99"))
    assert obj.get_prix() == decimal.Decimal("19.99")
    assert repr(obj).startswith("<TypeBillet (")

def test_journee_init_getters_setters():
    obj = Journee(date_jour=datetime.date(2026, 10, 10), heure_debut_officielle=datetime.time(14, 0), heure_fin_officielle=datetime.time(14, 0))
    assert obj.get_date_jour() == datetime.date(2026, 10, 10)
    assert obj.get_heure_debut_officielle() == datetime.time(14, 0)
    assert obj.get_heure_fin_officielle() == datetime.time(14, 0)
    obj.set_date_jour(datetime.date(2026, 10, 10))
    assert obj.get_date_jour() == datetime.date(2026, 10, 10)
    obj.set_heure_debut_officielle(datetime.time(14, 0))
    assert obj.get_heure_debut_officielle() == datetime.time(14, 0)
    obj.set_heure_fin_officielle(datetime.time(14, 0))
    assert obj.get_heure_fin_officielle() == datetime.time(14, 0)
    assert repr(obj).startswith("<Journee (")

def test_lieu_init_getters_setters():
    obj = Lieu(nom_lieu="Texte", adresse="Texte", jauge_max=5)
    assert obj.get_nom_lieu() == "Texte"
    assert obj.get_adresse() == "Texte"
    assert obj.get_jauge_max() == 5
    obj.set_id_lieu(5)
    assert obj.get_id_lieu() == 5
    obj.set_nom_lieu("Texte")
    assert obj.get_nom_lieu() == "Texte"
    obj.set_adresse("Texte")
    assert obj.get_adresse() == "Texte"
    obj.set_jauge_max(5)
    assert obj.get_jauge_max() == 5
    assert repr(obj).startswith("<Lieu (")

def test_hebergement_init_getters_setters():
    obj = Hebergement(nom_hebergement="Texte", adresse="Texte", capacite_places_par_jour=5)
    assert obj.get_nom_hebergement() == "Texte"
    assert obj.get_adresse() == "Texte"
    assert obj.get_capacite_places_par_jour() == 5
    obj.set_id_hebergement(5)
    assert obj.get_id_hebergement() == 5
    obj.set_nom_hebergement("Texte")
    assert obj.get_nom_hebergement() == "Texte"
    obj.set_adresse("Texte")
    assert obj.get_adresse() == "Texte"
    obj.set_capacite_places_par_jour(5)
    assert obj.get_capacite_places_par_jour() == 5
    assert repr(obj).startswith("<Hebergement (")

def test_dateachat_init_getters_setters():
    obj = DateAchat(date_achat=datetime.datetime(2026, 10, 10, 14, 0))
    assert obj.get_date_achat() == datetime.datetime(2026, 10, 10, 14, 0)
    obj.set_date_achat(datetime.datetime(2026, 10, 10, 14, 0))
    assert obj.get_date_achat() == datetime.datetime(2026, 10, 10, 14, 0)
    assert repr(obj).startswith("<DateAchat (")

def test_datenuit_init_getters_setters():
    obj = DateNuit(date_nuit=datetime.date(2026, 10, 10))
    assert obj.get_date_nuit() == datetime.date(2026, 10, 10)
    obj.set_date_nuit(datetime.date(2026, 10, 10))
    assert obj.get_date_nuit() == datetime.date(2026, 10, 10)
    assert repr(obj).startswith("<DateNuit (")

def test_evenement_init_getters_setters():
    obj = Evenement(titre="Texte", type_evenement="Texte", date_heure_debut=datetime.datetime(2026, 10, 10, 14, 0), duree=5, temps_montage=5, temps_demontage=5, est_gratuit=True, est_public=True, date_jour=datetime.date(2026, 10, 10), id_lieu=5)
    assert obj.get_titre() == "Texte"
    assert obj.get_type_evenement() == "Texte"
    assert obj.get_date_heure_debut() == datetime.datetime(2026, 10, 10, 14, 0)
    assert obj.get_duree() == 5
    assert obj.get_temps_montage() == 5
    assert obj.get_temps_demontage() == 5
    assert obj.get_est_gratuit() == True
    assert obj.get_est_public() == True
    assert obj.get_date_jour() == datetime.date(2026, 10, 10)
    assert obj.get_id_lieu() == 5
    obj.set_id_evenement(5)
    assert obj.get_id_evenement() == 5
    obj.set_titre("Texte")
    assert obj.get_titre() == "Texte"
    obj.set_type_evenement("Texte")
    assert obj.get_type_evenement() == "Texte"
    obj.set_date_heure_debut(datetime.datetime(2026, 10, 10, 14, 0))
    assert obj.get_date_heure_debut() == datetime.datetime(2026, 10, 10, 14, 0)
    obj.set_duree(5)
    assert obj.get_duree() == 5
    obj.set_temps_montage(5)
    assert obj.get_temps_montage() == 5
    obj.set_temps_demontage(5)
    assert obj.get_temps_demontage() == 5
    obj.set_est_gratuit(True)
    assert obj.get_est_gratuit() == True
    obj.set_est_public(True)
    assert obj.get_est_public() == True
    obj.set_date_jour(datetime.date(2026, 10, 10))
    assert obj.get_date_jour() == datetime.date(2026, 10, 10)
    obj.set_id_lieu(5)
    assert obj.get_id_lieu() == 5
    assert repr(obj).startswith("<Evenement (")

def test_spectateur():
    s = Spectateur(nom="Leroy", prenom="Emma", email="emma.leroy@example.com", mot_de_passe="x")
    assert s.get_email() == "emma.leroy@example.com"
    assert s.get_id() == "emma.leroy@example.com"
    s.set_id_spectateur(1)
    assert s.get_id_spectateur() == 1
    for a in ["nom", "prenom", "email", "mot_de_passe"]:
        getattr(s, "set_" + a)("v")
        assert getattr(s, "get_" + a)() == "v"
    assert repr(s) == "<Spectateur (1) v v>"

def test_jouer():
    obj = Jouer(id_membre=5, id_instrument=5)
    assert obj.id_membre == 5
    assert obj.id_instrument == 5
    assert repr(obj).startswith("<Jouer ")

def test_composer():
    obj = Composer(id_membre=5, id_groupe=5)
    assert obj.id_membre == 5
    assert obj.id_groupe == 5
    assert repr(obj).startswith("<Composer ")

def test_estsimilaire():
    obj = EstSimilaire(id_groupe=5, id_groupe_similaire=5)
    assert obj.id_groupe == 5
    assert obj.id_groupe_similaire == 5
    assert repr(obj).startswith("<EstSimilaire ")

def test_avoirstyle():
    obj = AvoirStyle(id_groupe=5, id_style=5)
    assert obj.id_groupe == 5
    assert obj.id_style == 5
    assert repr(obj).startswith("<AvoirStyle ")

def test_mettreenfavori():
    obj = MettreEnFavori(id_spectateur=5, id_groupe=5)
    assert obj.id_spectateur == 5
    assert obj.id_groupe == 5
    assert repr(obj).startswith("<MettreEnFavori ")

def test_acheter():
    obj = Acheter(id_spectateur=5, id_type_billet=5, date_achat=datetime.datetime(2026, 10, 10, 14, 0))
    assert obj.id_spectateur == 5
    assert obj.id_type_billet == 5
    assert obj.date_achat == datetime.datetime(2026, 10, 10, 14, 0)
    assert repr(obj).startswith("<Acheter ")

def test_donneracces():
    obj = DonnerAcces(id_type_billet=5, date_jour=datetime.date(2026, 10, 10))
    assert obj.id_type_billet == 5
    assert obj.date_jour == datetime.date(2026, 10, 10)
    assert repr(obj).startswith("<DonnerAcces ")

def test_preinscrire():
    obj = PreInscrire(id_spectateur=5, id_evenement=5)
    assert obj.id_spectateur == 5
    assert obj.id_evenement == 5
    assert repr(obj).startswith("<PreInscrire ")

def test_participer():
    obj = Participer(id_groupe=5, id_evenement=5)
    assert obj.id_groupe == 5
    assert obj.id_evenement == 5
    assert repr(obj).startswith("<Participer ")

def test_loger():
    obj = Loger(id_groupe=5, id_hebergement=5, date_nuit=datetime.date(2026, 10, 10), nb_places_necessaires=5)
    assert obj.id_groupe == 5
    assert obj.id_hebergement == 5
    assert obj.date_nuit == datetime.date(2026, 10, 10)
    assert obj.nb_places_necessaires == 5
    assert repr(obj).startswith("<Loger ")


def test_load_user(testapp):
    from monApp.app import db
    with testapp.app_context():
        db.session.add(Spectateur(nom="Leroy", prenom="Emma", email="emma.leroy@example.com", mot_de_passe="x"))
        db.session.commit()
        assert load_user("emma.leroy@example.com").nom == "Leroy"
        assert load_user("inconnu@mail.com") is None
