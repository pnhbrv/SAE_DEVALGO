# Vues de la billetterie [Source : TP 3 — render_template ; TP 4 — Blueprint ; maquettes — formules disponibles]
from flask import flash, redirect, render_template, session, url_for
from flask_login import current_user
from . import billeterie_bp
from monApp.models import TypeBillet

# Descriptions associées aux formules de billets selon la maquette
DESCRIPTIONS_BILLETS = {
    "Pass 1 jour": "Accès aux concerts du jour sélectionné",
    "Pass 2 jours": "Accès aux concerts des 2 jours",
    "Pass tout festival": "Accès aux concerts de tout le festival",
    "Pass étudiant": "Accès aux concerts du jour sélectionné",
}

# Données de démonstration alignées sur les types de billets de la base
FORMULES_DEFAUT = [
    {
        "id_type_billet": 1,
        "libelle": "Pass 1 jour",
        "prix": 35.00,
        "description": "Accès aux concerts du jour sélectionné",
    },
    {
        "id_type_billet": 2,
        "libelle": "Pass 2 jours",
        "prix": 60.00,
        "description": "Accès aux concerts des 2 jours",
    },
    {
        "id_type_billet": 3,
        "libelle": "Pass étudiant",
        "prix": 25.00,
        "description": "Accès aux concerts de tout le festival",
    },
    {
        "id_type_billet": 4,
        "libelle": "Pass tout festival",
        "prix": 120.00,
        "description": "Accès aux concerts de tout le festival",
    },
]


@billeterie_bp.route('/billetterie/')
@billeterie_bp.route('/billeterie/')
def billeterie():
    if not current_user.is_authenticated:
        flash("Veuillez vous connecter pour accéder à la billetterie.", "danger")
        return redirect(url_for('auth.login', next=url_for('billeterie.billeterie')))

    # Récupération des types de billets en base [Source : TP 2 — requêtes SQLAlchemy]
    types = TypeBillet.query.all()
    if types:
        billets = []
        for t in types:
            desc = DESCRIPTIONS_BILLETS.get(t.libelle, "Accès aux concerts du festival")
            billets.append({
                "id_type_billet": t.id_type_billet,
                "libelle": t.libelle,
                "prix": float(t.prix),
                "description": desc,
            })
    else:
        billets = FORMULES_DEFAUT

    billets_disponibles = {billet["id_type_billet"] for billet in billets}
    billets_selectionnes = [
        id_billet for id_billet in session.get("selected_ticket_ids", [])
        if id_billet in billets_disponibles
    ]
    session["selected_ticket_ids"] = billets_selectionnes

    return render_template(
        "billeterie.html",
        title="Billeterie",
        billets=billets,
        billets_selectionnes=billets_selectionnes,
    )


@billeterie_bp.route('/billeterie/selection/<int:id_type_billet>/')
def selectionner(id_type_billet):
    if not current_user.is_authenticated:
        flash("Veuillez vous connecter pour réserver votre billet.", "danger")
        return redirect(url_for(
            'auth.login',
            next=url_for('billeterie.selectionner', id_type_billet=id_type_billet),
        ))

    types = TypeBillet.query.all()
    if types:
        billet = next((type_billet for type_billet in types
                       if type_billet.id_type_billet == id_type_billet), None)
        nom_billet = billet.libelle if billet else None
    else:
        billet = next((formule for formule in FORMULES_DEFAUT
                       if formule["id_type_billet"] == id_type_billet), None)
        nom_billet = billet["libelle"] if billet else None

    if nom_billet is None:
        flash("Ce billet n'est pas disponible.", "danger")
        return redirect(url_for('billeterie.billeterie'))

    billets_selectionnes = session.get("selected_ticket_ids", [])
    if id_type_billet in billets_selectionnes:
        billets_selectionnes.remove(id_type_billet)
        flash(f"Vous avez retiré : {nom_billet}.", "succes")
    else:
        billets_selectionnes.append(id_type_billet)
        flash(f"Vous avez sélectionné : {nom_billet}.", "succes")
    session["selected_ticket_ids"] = billets_selectionnes
    return redirect(url_for('billeterie.billeterie'))
