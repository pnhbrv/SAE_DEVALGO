import click, logging as lg
import datetime
from hashlib import sha256
from flask.cli import with_appcontext
from .app import db


def hacher(mot_de_passe):
    m = sha256()
    m.update(mot_de_passe.encode())
    return m.hexdigest()


@click.command('loaddb')
@click.argument('filename')
@with_appcontext
def loaddb(filename):

    db.drop_all()
    db.create_all()

    import yaml
    with open(filename, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    from .models import (Membre, Instrument, Groupe, StyleMusical, Spectateur, TypeBillet, Journee,
                         Lieu, Hebergement, DateAchat, DateNuit, Evenement, Jouer, Composer, EstSimilaire,
                         AvoirStyle, MettreEnFavori, Acheter, DonnerAcces, PreInscrire, Participer, Loger,
                         PreferenceStyle)

    for s in data["styles"]:
        unStyle = StyleMusical(libelle_style=s["libelle_style"], id_style_parent=s["id_style_parent"])
        unStyle.set_id_style(s["id_style"])
        db.session.add(unStyle)
    for i in data["instruments"]:
        unInstrument = Instrument(libelle_instrument=i["libelle_instrument"])
        unInstrument.set_id_instrument(i["id_instrument"])
        db.session.add(unInstrument)
    for m in data["membres"]:
        unMembre = Membre(nom=m["nom"], prenom=m["prenom"])
        unMembre.set_id_membre(m["id_membre"])
        db.session.add(unMembre)
    for g in data["groupes"]:
        unGroupe = Groupe(nom_groupe=g["nom_groupe"], description=g["description"], liens_photos=g["liens_photos"],
                          liens_reseaux_sociaux=g["liens_reseaux_sociaux"], liens_videos=g["liens_videos"],
                          date_heure_arrivee=g["date_heure_arrivee"], date_heure_depart=g["date_heure_depart"])
        unGroupe.set_id_groupe(g["id_groupe"])
        db.session.add(unGroupe)
    for s in data["spectateurs"]:
        unSpectateur = Spectateur(nom=s["nom"], prenom=s["prenom"], email=s["email"],
                                  mot_de_passe=hacher(s["mot_de_passe"]), est_admin=s.get("est_admin", False))
        unSpectateur.set_id_spectateur(s["id_spectateur"])
        db.session.add(unSpectateur)
    for t in data["types_billet"]:
        unType = TypeBillet(libelle=t["libelle"], prix=t["prix"])
        unType.set_id_type_billet(t["id_type_billet"])
        db.session.add(unType)
    for j in data["journees"]:
        db.session.add(Journee(date_jour=j["date_jour"],
                               heure_debut_officielle=datetime.time.fromisoformat(j["heure_debut_officielle"]),
                               heure_fin_officielle=datetime.time.fromisoformat(j["heure_fin_officielle"])))
    for l in data["lieux"]:
        unLieu = Lieu(nom_lieu=l["nom_lieu"], adresse=l["adresse"], jauge_max=l["jauge_max"])
        unLieu.set_id_lieu(l["id_lieu"])
        db.session.add(unLieu)
    for h in data["hebergements"]:
        unHebergement = Hebergement(nom_hebergement=h["nom_hebergement"], adresse=h["adresse"],
                                    capacite_places_par_jour=h["capacite_places_par_jour"])
        unHebergement.set_id_hebergement(h["id_hebergement"])
        db.session.add(unHebergement)
    for d in data["dates_achat"]:
        db.session.add(DateAchat(date_achat=d["date_achat"]))
    for d in data["dates_nuit"]:
        db.session.add(DateNuit(date_nuit=d["date_nuit"]))
    db.session.commit()

    for e in data["evenements"]:
        unEvenement = Evenement(titre=e["titre"], type_evenement=e["type_evenement"],
                                date_heure_debut=e["date_heure_debut"], duree=e["duree"],
                                temps_montage=e["temps_montage"], temps_demontage=e["temps_demontage"],
                                est_gratuit=e["est_gratuit"], est_public=e["est_public"],
                                date_jour=e["date_jour"], id_lieu=e["id_lieu"])
        unEvenement.set_id_evenement(e["id_evenement"])
        db.session.add(unEvenement)
    db.session.commit()

    for r in data["jouer"]:
        db.session.add(Jouer(id_membre=r["id_membre"], id_instrument=r["id_instrument"]))
    for r in data["composer"]:
        db.session.add(Composer(id_membre=r["id_membre"], id_groupe=r["id_groupe"]))
    for r in data["est_similaire"]:
        db.session.add(EstSimilaire(id_groupe=r["id_groupe"], id_groupe_similaire=r["id_groupe_similaire"]))
    for r in data["avoir_style"]:
        db.session.add(AvoirStyle(id_groupe=r["id_groupe"], id_style=r["id_style"]))
    for r in data["favoris"]:
        db.session.add(MettreEnFavori(id_spectateur=r["id_spectateur"], id_groupe=r["id_groupe"]))
    for r in data["acheter"]:
        db.session.add(Acheter(id_spectateur=r["id_spectateur"], id_type_billet=r["id_type_billet"],
                               date_achat=r["date_achat"]))
    for r in data["donner_acces"]:
        db.session.add(DonnerAcces(id_type_billet=r["id_type_billet"], date_jour=r["date_jour"]))
    for r in data["pre_inscrire"]:
        db.session.add(PreInscrire(id_spectateur=r["id_spectateur"], id_evenement=r["id_evenement"]))
    for r in data["participer"]:
        db.session.add(Participer(id_groupe=r["id_groupe"], id_evenement=r["id_evenement"]))
    for r in data["loger"]:
        db.session.add(Loger(id_groupe=r["id_groupe"], id_hebergement=r["id_hebergement"],
                             date_nuit=r["date_nuit"], nb_places_necessaires=r["nb_places_necessaires"]))
    for r in data["preferences"]:
        db.session.add(PreferenceStyle(id_spectateur=r["id_spectateur"], id_style=r["id_style"], note=r["note"]))
    db.session.commit()
    lg.warning('Database initialized!')


@click.command('syncdb')
@with_appcontext
def syncdb():
    db.create_all()
    lg.warning('Database synchronized!')


def register_commands(app):
    app.cli.add_command(loaddb)
    app.cli.add_command(syncdb)
