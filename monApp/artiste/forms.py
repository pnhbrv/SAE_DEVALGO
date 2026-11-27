from flask_wtf import FlaskForm


class FavoriForm(FlaskForm):
    # aucun champ : le formulaire sert seulement à vérifier le jeton CSRF du bouton « favori »
    pass
