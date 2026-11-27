from flask_wtf import FlaskForm


class PreferencesForm(FlaskForm):
    # pas de champ déclaré : les notes sont lues dans request.form (un champ par style).
    # Le formulaire sert à vérifier le jeton CSRF.
    pass
