from decimal import Decimal

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user

from monApp.models import TypeBillet
from . import paiement_bp


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
    )
