from datetime import datetime, timedelta
from decimal import Decimal

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from monApp.app import db
from monApp.models import Acheter, DateAchat, TypeBillet
from . import paiement_bp
from .forms import PaiementForm


@paiement_bp.route('/paiement/')
def paiement():
    identifiants = request.args.getlist('id_type_billet')
    if not identifiants:
        identifiants = [str(id_billet) for id_billet in session.get('selected_ticket_ids', [])]
    if not current_user.is_authenticated:
        flash("Veuillez vous connecter pour accéder au paiement.", "danger")
        prochaine_page = url_for('paiement.paiement', id_type_billet=identifiants) if identifiants else url_for('paiement.paiement')
        return redirect(url_for('auth.login', next=prochaine_page))

    try:
        ids_billets = [int(identifiant) for identifiant in identifiants]
    except ValueError:
        flash("La sélection de billets est invalide.", "danger")
        return render_template(
            "paiement.html",
            title="Paiement",
            billets=[],
            total=Decimal("0.00"),
            form=PaiementForm(),
        )

    billets = []
    if ids_billets:
        types_billets = TypeBillet.query.filter(
            TypeBillet.id_type_billet.in_(set(ids_billets))
        ).all()
        billets_par_id = {billet.id_type_billet: billet for billet in types_billets}
        if any(id_billet not in billets_par_id for id_billet in ids_billets):
            flash("Un ou plusieurs billets ne sont plus disponibles.", "danger")
        else:
            billets = [billets_par_id[id_billet] for id_billet in ids_billets]

    total = sum((billet.prix for billet in billets), Decimal("0.00"))
    return render_template(
        "paiement.html",
        title="Paiement",
        billets=billets,
        total=total,
        form=PaiementForm(),
    )


@paiement_bp.route('/achat/insert/', methods=("POST",))
@login_required
def insertAchat():
    unForm = PaiementForm()
    if unForm.validate_on_submit():
        #recherche des billets affichés sur la page de paiement
        lesBillets = []
        for identifiant in request.form.getlist('id_type_billet'):
            unBillet = None
            if identifiant.isdigit():
                unBillet = db.session.get(TypeBillet, int(identifiant))
            if unBillet is None:
                flash("Un ou plusieurs billets ne sont plus disponibles.", "danger")
                return redirect(url_for('billeterie.billeterie'))
            lesBillets.append(unBillet)
        if len(lesBillets) == 0:
            flash("Aucun billet sélectionné.", "danger")
            return redirect(url_for('billeterie.billeterie'))

        #enregistrement d'un achat par billet (paiement fictif)
        #la date d'achat fait partie de la clé de ACHETER : on décale d'une seconde par billet
        #pour pouvoir acheter plusieurs billets du même type en une seule fois
        maintenant = datetime.now().replace(microsecond=0)
        for i in range(len(lesBillets)):
            date_achat = maintenant + timedelta(seconds=i)
            db.session.add(DateAchat(date_achat=date_achat))
            insertedAchat = Acheter(id_spectateur=current_user.id_spectateur,
                                    id_type_billet=lesBillets[i].id_type_billet, date_achat=date_achat)
            db.session.add(insertedAchat)
        db.session.commit()

        session["selected_ticket_ids"] = []
        flash("Paiement confirmé : vos billets sont dans Mon espace.", "succes")
        return redirect(url_for('preference.monEspace'))
    flash("Le paiement n'a pas pu être validé, veuillez réessayer.", "danger")
    return redirect(url_for('paiement.paiement'))
