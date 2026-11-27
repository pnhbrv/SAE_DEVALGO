from flask_wtf import FlaskForm


class PaiementForm(FlaskForm):
    # aucun champ : les billets sont envoyés en champs cachés, le formulaire sert au jeton CSRF
    pass
