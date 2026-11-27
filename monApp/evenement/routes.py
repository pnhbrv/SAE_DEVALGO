from datetime import date, timedelta
from flask import render_template, request
from flask_login import current_user
from sqlalchemy import or_
from . import evenement_bp
from monApp.artiste.routes import styles_avec_sous_genres
from monApp.models import AvoirStyle, Evenement, Groupe, Journee, Lieu, Participer, StyleMusical
from monApp.recommandation import concerts_conseilles

JOURS_FR = ("Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche")
MOIS_FR = (
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
)


def formater_date_fr(une_date):
    """Formate une date en français sans dépendre de la locale du système (ex: Mercredi 14 octobre)."""
    return f"{JOURS_FR[une_date.weekday()]} {une_date.day} {MOIS_FR[une_date.month - 1]}"


def photo_evenement(un_evenement):
    """Renvoie le premier lien photo trouvé parmi les groupes participants, ou None."""
    for une_participation in un_evenement.participations:
        if une_participation.groupe and une_participation.groupe.liens_photos:
            return une_participation.groupe.liens_photos
    return None


def preparer_evenement(un_evenement):
    """Prépare les données d'affichage d'un événement pour le template."""
    heure_fin = un_evenement.date_heure_debut + timedelta(minutes=un_evenement.duree or 0)
    return {
        "evenement": un_evenement,
        "participations": un_evenement.participations.all(),
        "photo": photo_evenement(un_evenement),
        "heure_debut": un_evenement.date_heure_debut.strftime('%H:%M'),
        "heure_fin": heure_fin.strftime('%H:%M'),
        "date_label": formater_date_fr(un_evenement.date_jour),
    }


@evenement_bp.route('/evenements/')
def getEvenements():
    recherche = request.args.get('recherche', '').strip()
    style = request.args.get('style', type=int)
    prix = request.args.get('prix')
    jour = request.args.get('date', type=date.fromisoformat)
    lieu = request.args.get('lieu', type=int)

    requete = Evenement.query.filter(
        or_(Evenement.est_public.is_(True), Evenement.est_public.is_(None))
    )

    if recherche:
        motif = f"%{recherche}%"
        requete = (
            requete.outerjoin(Participer, Participer.id_evenement == Evenement.id_evenement)
            .outerjoin(Groupe, Groupe.id_groupe == Participer.id_groupe)
            .outerjoin(AvoirStyle, AvoirStyle.id_groupe == Groupe.id_groupe)
            .outerjoin(StyleMusical, StyleMusical.id_style == AvoirStyle.id_style)
            .filter(
                or_(
                    Evenement.titre.ilike(motif),
                    Evenement.type_evenement.ilike(motif),
                    Groupe.nom_groupe.ilike(motif),
                    StyleMusical.libelle_style.ilike(motif),
                )
            )
        )

    if style:
        requete = (
            requete.join(Participer, Participer.id_evenement == Evenement.id_evenement)
            .join(AvoirStyle, AvoirStyle.id_groupe == Participer.id_groupe)
            .filter(AvoirStyle.id_style.in_(styles_avec_sous_genres(style)))
        )

    if prix in ('gratuit', 'payant'):
        requete = requete.filter(Evenement.est_gratuit == (prix == 'gratuit'))
    if jour:
        requete = requete.filter(Evenement.date_jour == jour)
    if lieu:
        requete = requete.filter(Evenement.id_lieu == lieu)

    les_evenements = requete.distinct().order_by(
        Evenement.date_jour, Evenement.date_heure_debut
    ).all()

    groupes_par_jour = []
    index_jours = {}
    for un_evenement in les_evenements:
        date_j = un_evenement.date_jour
        if date_j not in index_jours:
            bloc = {
                "date": date_j,
                "label": formater_date_fr(date_j),
                "evenements": [],
            }
            index_jours[date_j] = bloc
            groupes_par_jour.append(bloc)

        index_jours[date_j]["evenements"].append(preparer_evenement(un_evenement))

    # recommandations de l'Algo : seulement sur la liste complète, pour un spectateur connecté
    evenements_conseilles = []
    if current_user.is_authenticated and not (recherche or style or prix or jour or lieu):
        conseilles, _ = concerts_conseilles(current_user.id_spectateur)
        evenements_conseilles = [preparer_evenement(e) for e in conseilles if e is not None]

    return render_template(
        'evenements_list.html',
        title="Événements",
        evenements=les_evenements,
        evenements_conseilles=evenements_conseilles,
        groupes_par_jour=groupes_par_jour,
        styles=StyleMusical.query.order_by(StyleMusical.id_style).all(),
        journees=Journee.query.order_by(Journee.date_jour).all(),
        lieux=Lieu.query.order_by(Lieu.nom_lieu).all(),
        recherche=recherche,
        style=style,
        prix=prix,
        jour=jour,
        lieu=lieu,
    )
