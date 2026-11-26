import datetime
from monApp.app import db
from monApp.models import (AvoirStyle, Evenement, Groupe, Journee, Lieu, Participer, PreferenceStyle,
                           Spectateur, StyleMusical)
from monApp.recommandation import cache, concerts_conseilles, preferences_du_spectateur, suggestions_groupes

JOUR = datetime.date(2026, 10, 10)


def ajouter_style(id_style, libelle, id_parent=None):
    unStyle = StyleMusical(libelle_style=libelle, id_style_parent=id_parent)
    unStyle.set_id_style(id_style)
    db.session.add(unStyle)


def ajouter_groupe(id_groupe, nom, id_style):
    unGroupe = Groupe(nom_groupe=nom)
    unGroupe.set_id_groupe(id_groupe)
    db.session.add(unGroupe)
    db.session.add(AvoirStyle(id_groupe=id_groupe, id_style=id_style))


def ajouter_concert(id_evenement, id_groupe, heure, duree):
    unEvenement = Evenement(titre="Concert %d" % id_evenement, type_evenement="Concert",
                            date_heure_debut=datetime.datetime(2026, 10, 10, heure, 0), duree=duree,
                            est_gratuit=False, est_public=True, date_jour=JOUR, id_lieu=1)
    unEvenement.set_id_evenement(id_evenement)
    db.session.add(unEvenement)
    db.session.add(Participer(id_groupe=id_groupe, id_evenement=id_evenement))


def remplir_base(testapp):
    # Rock (1) > Punk (2) ; Pop (3) ; Jazz (4)
    with testapp.app_context():
        ajouter_style(1, "Rock")
        ajouter_style(2, "Punk", 1)
        ajouter_style(3, "Pop")
        ajouter_style(4, "Jazz")
        ajouter_groupe(1, "Groupe rock", 1)
        ajouter_groupe(2, "Groupe punk", 2)
        ajouter_groupe(3, "Groupe pop", 3)
        ajouter_groupe(4, "Groupe jazz", 4)
        db.session.add(Spectateur(nom="Leroy", prenom="Emma", email="emma@mail.com", mot_de_passe="x"))
        db.session.add(Journee(date_jour=JOUR, heure_debut_officielle=datetime.time(14, 0),
                               heure_fin_officielle=datetime.time(4, 0)))
        unLieu = Lieu(nom_lieu="Scène", adresse="Orléans", jauge_max=100)
        unLieu.set_id_lieu(1)
        db.session.add(unLieu)
        db.session.commit()
        # Emma aime le rock et refuse la pop
        db.session.add(PreferenceStyle(id_spectateur=1, id_style=1, note=5))
        db.session.add(PreferenceStyle(id_spectateur=1, id_style=3, note=-2))
        db.session.commit()
    cache.invalider()


def noms(groupes):
    resultat = []
    for unGroupe in groupes:
        resultat.append(unGroupe.nom_groupe)
    return resultat


def test_preferences_du_spectateur(testapp):
    remplir_base(testapp)
    with testapp.app_context():
        assert preferences_du_spectateur(1) == {1: 5, 3: -2}
        assert preferences_du_spectateur(99) == {}


def test_suggestions_du_meilleur_au_moins_bon(testapp):
    remplir_base(testapp)
    with testapp.app_context():
        # rock : 5, punk : 5 / (1+1) = 2.5 ; la pop est refusée et le jazz est neutre
        assert noms(suggestions_groupes(1)) == ["Groupe rock", "Groupe punk"]
        assert noms(suggestions_groupes(1, nombre=1)) == ["Groupe rock"]


def test_pas_de_suggestion_sans_preference(testapp):
    remplir_base(testapp)
    with testapp.app_context():
        assert suggestions_groupes(99) == []


def test_concerts_conseilles_sans_chevauchement(testapp):
    remplir_base(testapp)
    with testapp.app_context():
        ajouter_concert(1, 1, 18, 60)     # rock 18h-19h
        ajouter_concert(2, 2, 18, 90)     # punk 18h-19h30 : chevauche le rock, moins bon score
        ajouter_concert(3, 3, 20, 60)     # pop : refusée
        ajouter_concert(4, 4, 21, 60)     # jazz : neutre, mais rien d'autre à cette heure
        db.session.commit()
        evenements, score = concerts_conseilles(1)
        ids = []
        for unEvenement in evenements:
            ids.append(unEvenement.id_evenement)
        assert ids == [1, 4]
        assert round(score, 2) == 5.05


def test_le_cache_est_utilise(testapp):
    remplir_base(testapp)
    with testapp.app_context():
        ajouter_concert(1, 1, 18, 60)
        db.session.commit()
        concerts_conseilles(1)
        # un concert ajouté sans vider le cache ne change pas le résultat déjà calculé
        ajouter_concert(2, 2, 20, 60)
        db.session.commit()
        evenements, score = concerts_conseilles(1)
        assert len(evenements) == 1
        cache.invalider(1)
        evenements, score = concerts_conseilles(1)
        assert len(evenements) == 2
