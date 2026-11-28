from flask import abort, render_template
from flask_login import current_user, login_required
from . import admin_bp
from monApp.models import Acheter, Evenement, Groupe, Spectateur


@admin_bp.route('/admin/')
@login_required
def tableauDeBord():
    #seul un organisateur a accès à l'espace administrateur (403 : accès interdit)
    if not current_user.est_admin:
        abort(403)
    nbGroupes = Groupe.query.count()
    nbEvenements = Evenement.query.count()
    nbSpectateurs = Spectateur.query.filter_by(est_admin=False).count()
    nbBillets = Acheter.query.count()
    return render_template("tableau_de_bord.html", title="Espace Administrateur", nbGroupes=nbGroupes,
                           nbEvenements=nbEvenements, nbSpectateurs=nbSpectateurs, nbBillets=nbBillets)
