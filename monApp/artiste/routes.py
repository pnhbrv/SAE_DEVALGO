from datetime import date
from flask import render_template, request
from flask_login import current_user
from . import artiste_bp
from monApp.models import AvoirStyle, Evenement, Groupe, Journee, Lieu, Participer, StyleMusical
from monApp.recommandation import suggestions_groupes


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
