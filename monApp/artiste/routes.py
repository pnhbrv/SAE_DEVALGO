from datetime import date
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from . import artiste_bp
from .forms import FavoriForm
from monApp.app import db
from monApp.models import AvoirStyle, Evenement, Groupe, Journee, Lieu, MettreEnFavori, Participer, StyleMusical
from monApp.recommandation import groupes_similaires, suggestions_groupes


def styles_avec_sous_genres(id_style):
    lesIds = [id_style]
    for unEnfant in StyleMusical.query.filter_by(id_style_parent=id_style).all():
        lesIds = lesIds + styles_avec_sous_genres(unEnfant.id_style)
    return lesIds


@artiste_bp.route('/artistes/')
def getArtistes():
    recherche = request.args.get('recherche', '').strip()
    style = request.args.get('style', type=int)
    prix = request.args.get('prix')
    jour = request.args.get('date', type=date.fromisoformat)
    lieu = request.args.get('lieu', type=int)

    requete = Groupe.query
    if recherche:
        requete = requete.filter(Groupe.nom_groupe.ilike('%' + recherche + '%'))
    if style:
        requete = requete.join(AvoirStyle, AvoirStyle.id_groupe == Groupe.id_groupe) \
                         .filter(AvoirStyle.id_style.in_(styles_avec_sous_genres(style)))
    if prix in ('gratuit', 'payant') or jour or lieu:
        requete = requete.join(Participer, Participer.id_groupe == Groupe.id_groupe) \
                         .join(Evenement, Evenement.id_evenement == Participer.id_evenement)
        if prix in ('gratuit', 'payant'):
            requete = requete.filter(Evenement.est_gratuit == (prix == 'gratuit'))
        if jour:
            requete = requete.filter(Evenement.date_jour == jour)
        if lieu:
            requete = requete.filter(Evenement.id_lieu == lieu)

    lesGroupes = requete.distinct().order_by(Groupe.nom_groupe).all()

    # suggestions de l'Algo : seulement sur la liste complète, pour un spectateur connecté
    lesSuggestions = []
    if current_user.is_authenticated and not (recherche or style or prix or jour or lieu):
        lesSuggestions = suggestions_groupes(current_user.id_spectateur)

    return render_template('artistes_list.html', title="Artistes", groupes=lesGroupes, suggestions=lesSuggestions,
                        styles=StyleMusical.query.order_by(StyleMusical.id_style).all(),
                        journees=Journee.query.order_by(Journee.date_jour).all(),
                        lieux=Lieu.query.order_by(Lieu.nom_lieu).all(),
                        recherche=recherche, style=style, prix=prix, jour=jour, lieu=lieu)


def lien_video_integree(lien):
    """Adresse à mettre dans une balise iframe pour une vidéo YouTube, ou None si le lien n'est pas une vidéo."""
    if lien is None or "watch?v=" not in lien:
        return None
    id_video = lien.split("watch?v=")[1].split("&")[0]
    return "https://www.youtube.com/embed/" + id_video


@artiste_bp.route('/artistes/<int:id_groupe>/')
def getArtiste(id_groupe):
    unGroupe = Groupe.query.filter_by(id_groupe=id_groupe).first_or_404()

    # chaque membre avec la liste de ses instruments
    lesMembres = []
    for uneComposition in unGroupe.compositions:
        instruments = []
        for unJouer in uneComposition.membre.jouers:
            instruments.append(unJouer.instrument.libelle_instrument)
        lesMembres.append((uneComposition.membre, instruments))

    lesConcerts = Evenement.query.join(Participer, Participer.id_evenement == Evenement.id_evenement)                                  .filter(Participer.id_groupe == id_groupe)                                  .order_by(Evenement.date_heure_debut).all()

    est_favori = False
    if current_user.is_authenticated:
        est_favori = trouver_favori(current_user.id_spectateur, id_groupe) is not None

    return render_template('artiste_fiche.html', title=unGroupe.nom_groupe, groupe=unGroupe, membres=lesMembres,
                           concerts=lesConcerts, similaires=groupes_similaires(unGroupe),
                           video=lien_video_integree(unGroupe.liens_videos),
                           est_favori=est_favori, form_favori=FavoriForm())


def trouver_favori(id_spectateur, id_groupe):
    return MettreEnFavori.query.filter_by(id_spectateur=id_spectateur, id_groupe=id_groupe).first()


@artiste_bp.route('/artistes/<int:id_groupe>/favori/', methods=("POST",))
@login_required
def changerFavori(id_groupe):
    """Ajoute le groupe aux favoris du spectateur, ou l'en retire s'il y est déjà."""
    unGroupe = Groupe.query.filter_by(id_groupe=id_groupe).first_or_404()
    if FavoriForm().validate_on_submit():
        unFavori = trouver_favori(current_user.id_spectateur, id_groupe)
        if unFavori is None:
            db.session.add(MettreEnFavori(id_spectateur=current_user.id_spectateur, id_groupe=id_groupe))
            flash(unGroupe.nom_groupe + " est ajouté à vos favoris.", "succes")
        else:
            db.session.delete(unFavori)
            flash(unGroupe.nom_groupe + " est retiré de vos favoris.", "succes")
        db.session.commit()
    return redirect(url_for('artiste.getArtiste', id_groupe=id_groupe))
