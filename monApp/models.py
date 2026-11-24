from flask_login import UserMixin
from .app import db, login_manager


class Membre(db.Model):
    id_membre = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)

    def __init__(self, nom=None, prenom=None):
        self.nom = nom
        self.prenom = prenom

    def get_id_membre(self):
        return self.id_membre

    def set_id_membre(self, id_membre):
        self.id_membre = id_membre

    def get_nom(self):
        return self.nom

    def set_nom(self, nom):
        self.nom = nom

    def get_prenom(self):
        return self.prenom

    def set_prenom(self, prenom):
        self.prenom = prenom

    def __repr__(self):
        return "<Membre (%s) %s>" % (self.id_membre, self.nom)


class Instrument(db.Model):
    id_instrument = db.Column(db.Integer, primary_key=True)
    libelle_instrument = db.Column(db.String(100), nullable=False)

    def __init__(self, libelle_instrument=None):
        self.libelle_instrument = libelle_instrument

    def get_id_instrument(self):
        return self.id_instrument

    def set_id_instrument(self, id_instrument):
        self.id_instrument = id_instrument

    def get_libelle_instrument(self):
        return self.libelle_instrument

    def set_libelle_instrument(self, libelle_instrument):
        self.libelle_instrument = libelle_instrument

    def __repr__(self):
        return "<Instrument (%s) %s>" % (self.id_instrument, self.libelle_instrument)


class Groupe(db.Model):
    id_groupe = db.Column(db.Integer, primary_key=True)
    nom_groupe = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    liens_photos = db.Column(db.Text)
    liens_reseaux_sociaux = db.Column(db.Text)
    liens_videos = db.Column(db.Text)
    date_heure_arrivee = db.Column(db.DateTime)
    date_heure_depart = db.Column(db.DateTime)

    def __init__(self, nom_groupe=None, description=None, liens_photos=None, liens_reseaux_sociaux=None, liens_videos=None, date_heure_arrivee=None, date_heure_depart=None):
        self.nom_groupe = nom_groupe
        self.description = description
        self.liens_photos = liens_photos
        self.liens_reseaux_sociaux = liens_reseaux_sociaux
        self.liens_videos = liens_videos
        self.date_heure_arrivee = date_heure_arrivee
        self.date_heure_depart = date_heure_depart

    def get_id_groupe(self):
        return self.id_groupe

    def set_id_groupe(self, id_groupe):
        self.id_groupe = id_groupe

    def get_nom_groupe(self):
        return self.nom_groupe

    def set_nom_groupe(self, nom_groupe):
        self.nom_groupe = nom_groupe

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_liens_photos(self):
        return self.liens_photos

    def set_liens_photos(self, liens_photos):
        self.liens_photos = liens_photos

    def get_liens_reseaux_sociaux(self):
        return self.liens_reseaux_sociaux

    def set_liens_reseaux_sociaux(self, liens_reseaux_sociaux):
        self.liens_reseaux_sociaux = liens_reseaux_sociaux

    def get_liens_videos(self):
        return self.liens_videos

    def set_liens_videos(self, liens_videos):
        self.liens_videos = liens_videos

    def get_date_heure_arrivee(self):
        return self.date_heure_arrivee

    def set_date_heure_arrivee(self, date_heure_arrivee):
        self.date_heure_arrivee = date_heure_arrivee

    def get_date_heure_depart(self):
        return self.date_heure_depart

    def set_date_heure_depart(self, date_heure_depart):
        self.date_heure_depart = date_heure_depart

    def __repr__(self):
        return "<Groupe (%s) %s>" % (self.id_groupe, self.nom_groupe)


class StyleMusical(db.Model):
    __tablename__ = "style_musical"
    id_style = db.Column(db.Integer, primary_key=True)
    libelle_style = db.Column(db.String(100), nullable=False)
    id_style_parent = db.Column(db.Integer, db.ForeignKey("style_musical.id_style"))

    def __init__(self, libelle_style=None, id_style_parent=None):
        self.libelle_style = libelle_style
        self.id_style_parent = id_style_parent

    def get_id_style(self):
        return self.id_style

    def set_id_style(self, id_style):
        self.id_style = id_style

    def get_libelle_style(self):
        return self.libelle_style

    def set_libelle_style(self, libelle_style):
        self.libelle_style = libelle_style

    def get_id_style_parent(self):
        return self.id_style_parent

    def set_id_style_parent(self, id_style_parent):
        self.id_style_parent = id_style_parent

    def __repr__(self):
        return "<StyleMusical (%s) %s>" % (self.id_style, self.libelle_style)


class TypeBillet(db.Model):
    __tablename__ = "type_billet"
    id_type_billet = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Numeric(10, 2), nullable=False)

    def __init__(self, libelle=None, prix=None):
        self.libelle = libelle
        self.prix = prix

    def get_id_type_billet(self):
        return self.id_type_billet

    def set_id_type_billet(self, id_type_billet):
        self.id_type_billet = id_type_billet

    def get_libelle(self):
        return self.libelle

    def set_libelle(self, libelle):
        self.libelle = libelle

    def get_prix(self):
        return self.prix

    def set_prix(self, prix):
        self.prix = prix

    def __repr__(self):
        return "<TypeBillet (%s) %s>" % (self.id_type_billet, self.libelle)


class Journee(db.Model):
    date_jour = db.Column(db.Date, primary_key=True)
    heure_debut_officielle = db.Column(db.Time, nullable=False)
    heure_fin_officielle = db.Column(db.Time, nullable=False)

    def __init__(self, date_jour=None, heure_debut_officielle=None, heure_fin_officielle=None):
        self.date_jour = date_jour
        self.heure_debut_officielle = heure_debut_officielle
        self.heure_fin_officielle = heure_fin_officielle

    def get_date_jour(self):
        return self.date_jour

    def set_date_jour(self, date_jour):
        self.date_jour = date_jour

    def get_heure_debut_officielle(self):
        return self.heure_debut_officielle

    def set_heure_debut_officielle(self, heure_debut_officielle):
        self.heure_debut_officielle = heure_debut_officielle

    def get_heure_fin_officielle(self):
        return self.heure_fin_officielle

    def set_heure_fin_officielle(self, heure_fin_officielle):
        self.heure_fin_officielle = heure_fin_officielle

    def __repr__(self):
        return "<Journee (%s) %s>" % (self.date_jour, self.heure_debut_officielle)


class Lieu(db.Model):
    id_lieu = db.Column(db.Integer, primary_key=True)
    nom_lieu = db.Column(db.String(150), nullable=False)
    adresse = db.Column(db.String(255), nullable=False)
    jauge_max = db.Column(db.Integer, nullable=False)

    def __init__(self, nom_lieu=None, adresse=None, jauge_max=None):
        self.nom_lieu = nom_lieu
        self.adresse = adresse
        self.jauge_max = jauge_max

    def get_id_lieu(self):
        return self.id_lieu

    def set_id_lieu(self, id_lieu):
        self.id_lieu = id_lieu

    def get_nom_lieu(self):
        return self.nom_lieu

    def set_nom_lieu(self, nom_lieu):
        self.nom_lieu = nom_lieu

    def get_adresse(self):
        return self.adresse

    def set_adresse(self, adresse):
        self.adresse = adresse

    def get_jauge_max(self):
        return self.jauge_max

    def set_jauge_max(self, jauge_max):
        self.jauge_max = jauge_max

    def __repr__(self):
        return "<Lieu (%s) %s>" % (self.id_lieu, self.nom_lieu)


class Hebergement(db.Model):
    id_hebergement = db.Column(db.Integer, primary_key=True)
    nom_hebergement = db.Column(db.String(150), nullable=False)
    adresse = db.Column(db.String(255), nullable=False)
    capacite_places_par_jour = db.Column(db.Integer, nullable=False)

    def __init__(self, nom_hebergement=None, adresse=None, capacite_places_par_jour=None):
        self.nom_hebergement = nom_hebergement
        self.adresse = adresse
        self.capacite_places_par_jour = capacite_places_par_jour

    def get_id_hebergement(self):
        return self.id_hebergement

    def set_id_hebergement(self, id_hebergement):
        self.id_hebergement = id_hebergement

    def get_nom_hebergement(self):
        return self.nom_hebergement

    def set_nom_hebergement(self, nom_hebergement):
        self.nom_hebergement = nom_hebergement

    def get_adresse(self):
        return self.adresse

    def set_adresse(self, adresse):
        self.adresse = adresse

    def get_capacite_places_par_jour(self):
        return self.capacite_places_par_jour

    def set_capacite_places_par_jour(self, capacite_places_par_jour):
        self.capacite_places_par_jour = capacite_places_par_jour

    def __repr__(self):
        return "<Hebergement (%s) %s>" % (self.id_hebergement, self.nom_hebergement)


class DateAchat(db.Model):
    __tablename__ = "date_achat"
    date_achat = db.Column(db.DateTime, primary_key=True)

    def __init__(self, date_achat=None):
        self.date_achat = date_achat

    def get_date_achat(self):
        return self.date_achat

    def set_date_achat(self, date_achat):
        self.date_achat = date_achat

    def __repr__(self):
        return "<DateAchat (%s) %s>" % (self.date_achat, self.date_achat)


class DateNuit(db.Model):
    __tablename__ = "date_nuit"
    date_nuit = db.Column(db.Date, primary_key=True)

    def __init__(self, date_nuit=None):
        self.date_nuit = date_nuit

    def get_date_nuit(self):
        return self.date_nuit

    def set_date_nuit(self, date_nuit):
        self.date_nuit = date_nuit

    def __repr__(self):
        return "<DateNuit (%s) %s>" % (self.date_nuit, self.date_nuit)


class Evenement(db.Model):
    id_evenement = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150), nullable=False)
    type_evenement = db.Column(db.String(100), nullable=False)
    date_heure_debut = db.Column(db.DateTime, nullable=False)
    duree = db.Column(db.Integer, nullable=False)
    temps_montage = db.Column(db.Integer)
    temps_demontage = db.Column(db.Integer)
    est_gratuit = db.Column(db.Boolean, default=False)
    est_public = db.Column(db.Boolean, default=True)
    date_jour = db.Column(db.Date, db.ForeignKey("journee.date_jour"), nullable=False)
    id_lieu = db.Column(db.Integer, db.ForeignKey("lieu.id_lieu"), nullable=False)
    journee = db.relationship("Journee", backref=db.backref("evenements", lazy="dynamic"))
    lieu = db.relationship("Lieu", backref=db.backref("evenements", lazy="dynamic"))

    def __init__(self, titre=None, type_evenement=None, date_heure_debut=None, duree=None, temps_montage=None, temps_demontage=None, est_gratuit=None, est_public=None, date_jour=None, id_lieu=None):
        self.titre = titre
        self.type_evenement = type_evenement
        self.date_heure_debut = date_heure_debut
        self.duree = duree
        self.temps_montage = temps_montage
        self.temps_demontage = temps_demontage
        self.est_gratuit = est_gratuit
        self.est_public = est_public
        self.date_jour = date_jour
        self.id_lieu = id_lieu

    def get_id_evenement(self):
        return self.id_evenement

    def set_id_evenement(self, id_evenement):
        self.id_evenement = id_evenement

    def get_titre(self):
        return self.titre

    def set_titre(self, titre):
        self.titre = titre

    def get_type_evenement(self):
        return self.type_evenement

    def set_type_evenement(self, type_evenement):
        self.type_evenement = type_evenement

    def get_date_heure_debut(self):
        return self.date_heure_debut

    def set_date_heure_debut(self, date_heure_debut):
        self.date_heure_debut = date_heure_debut

    def get_duree(self):
        return self.duree

    def set_duree(self, duree):
        self.duree = duree

    def get_temps_montage(self):
        return self.temps_montage

    def set_temps_montage(self, temps_montage):
        self.temps_montage = temps_montage

    def get_temps_demontage(self):
        return self.temps_demontage

    def set_temps_demontage(self, temps_demontage):
        self.temps_demontage = temps_demontage

    def get_est_gratuit(self):
        return self.est_gratuit

    def set_est_gratuit(self, est_gratuit):
        self.est_gratuit = est_gratuit

    def get_est_public(self):
        return self.est_public

    def set_est_public(self, est_public):
        self.est_public = est_public

    def get_date_jour(self):
        return self.date_jour

    def set_date_jour(self, date_jour):
        self.date_jour = date_jour

    def get_id_lieu(self):
        return self.id_lieu

    def set_id_lieu(self, id_lieu):
        self.id_lieu = id_lieu

    def __repr__(self):
        return "<Evenement (%s) %s>" % (self.id_evenement, self.titre)


class Spectateur(db.Model, UserMixin):
    id_spectateur = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(255), nullable=False)

    def __init__(self, nom=None, prenom=None, email=None, mot_de_passe=None):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mot_de_passe = mot_de_passe

    def get_id_spectateur(self):
        return self.id_spectateur

    def set_id_spectateur(self, id_spectateur):
        self.id_spectateur = id_spectateur

    def get_nom(self):
        return self.nom

    def set_nom(self, nom):
        self.nom = nom

    def get_prenom(self):
        return self.prenom

    def set_prenom(self, prenom):
        self.prenom = prenom

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_mot_de_passe(self):
        return self.mot_de_passe

    def set_mot_de_passe(self, mot_de_passe):
        self.mot_de_passe = mot_de_passe

    def get_id(self):
        return self.email

    def __repr__(self):
        return "<Spectateur (%s) %s %s>" % (self.id_spectateur, self.prenom, self.nom)


class Jouer(db.Model):
    __tablename__ = "jouer"
    id_membre = db.Column(db.Integer, db.ForeignKey("membre.id_membre"), primary_key=True)
    id_instrument = db.Column(db.Integer, db.ForeignKey("instrument.id_instrument"), primary_key=True)
    membre = db.relationship("Membre", backref=db.backref("jouers", lazy="dynamic"))
    instrument = db.relationship("Instrument", backref=db.backref("jouers", lazy="dynamic"))

    def __init__(self, id_membre=None, id_instrument=None):
        self.id_membre = id_membre
        self.id_instrument = id_instrument

    def __repr__(self):
        return "<Jouer %s>" % ([self.id_membre, self.id_instrument],)


class Composer(db.Model):
    __tablename__ = "composer"
    id_membre = db.Column(db.Integer, db.ForeignKey("membre.id_membre"), primary_key=True)
    id_groupe = db.Column(db.Integer, db.ForeignKey("groupe.id_groupe"), primary_key=True)
    membre = db.relationship("Membre", backref=db.backref("compositions", lazy="dynamic"))
    groupe = db.relationship("Groupe", backref=db.backref("compositions", lazy="dynamic"))

    def __init__(self, id_membre=None, id_groupe=None):
        self.id_membre = id_membre
        self.id_groupe = id_groupe

    def __repr__(self):
        return "<Composer %s>" % ([self.id_membre, self.id_groupe],)


class EstSimilaire(db.Model):
    __tablename__ = "est_similaire"
    id_groupe = db.Column(db.Integer, db.ForeignKey("groupe.id_groupe"), primary_key=True)
    id_groupe_similaire = db.Column(db.Integer, db.ForeignKey("groupe.id_groupe"), primary_key=True)

    def __init__(self, id_groupe=None, id_groupe_similaire=None):
        self.id_groupe = id_groupe
        self.id_groupe_similaire = id_groupe_similaire

    def __repr__(self):
        return "<EstSimilaire %s>" % ([self.id_groupe, self.id_groupe_similaire],)


class AvoirStyle(db.Model):
    __tablename__ = "avoir_style"
    id_groupe = db.Column(db.Integer, db.ForeignKey("groupe.id_groupe"), primary_key=True)
    id_style = db.Column(db.Integer, db.ForeignKey("style_musical.id_style"), primary_key=True)
    groupe = db.relationship("Groupe", backref=db.backref("styles", lazy="dynamic"))
    style = db.relationship("StyleMusical", backref=db.backref("groupes", lazy="dynamic"))

    def __init__(self, id_groupe=None, id_style=None):
        self.id_groupe = id_groupe
        self.id_style = id_style

    def __repr__(self):
        return "<AvoirStyle %s>" % ([self.id_groupe, self.id_style],)


class MettreEnFavori(db.Model):
    __tablename__ = "mettre_en_favori"
    id_spectateur = db.Column(db.Integer, db.ForeignKey("spectateur.id_spectateur"), primary_key=True)
    id_groupe = db.Column(db.Integer, db.ForeignKey("groupe.id_groupe"), primary_key=True)
    spectateur = db.relationship("Spectateur", backref=db.backref("favoris", lazy="dynamic"))
    groupe = db.relationship("Groupe", backref=db.backref("fans", lazy="dynamic"))

    def __init__(self, id_spectateur=None, id_groupe=None):
        self.id_spectateur = id_spectateur
        self.id_groupe = id_groupe

    def __repr__(self):
        return "<MettreEnFavori %s>" % ([self.id_spectateur, self.id_groupe],)


class Acheter(db.Model):
    __tablename__ = "acheter"
    id_spectateur = db.Column(db.Integer, db.ForeignKey("spectateur.id_spectateur"), primary_key=True)
    id_type_billet = db.Column(db.Integer, db.ForeignKey("type_billet.id_type_billet"), primary_key=True)
    date_achat = db.Column(db.DateTime, db.ForeignKey("date_achat.date_achat"), primary_key=True)
    spectateur = db.relationship("Spectateur", backref=db.backref("achats", lazy="dynamic"))
    type_billet = db.relationship("TypeBillet", backref=db.backref("achats", lazy="dynamic"))

    def __init__(self, id_spectateur=None, id_type_billet=None, date_achat=None):
        self.id_spectateur = id_spectateur
        self.id_type_billet = id_type_billet
        self.date_achat = date_achat

    def __repr__(self):
        return "<Acheter %s>" % ([self.id_spectateur, self.id_type_billet, self.date_achat],)


class DonnerAcces(db.Model):
    __tablename__ = "donner_acces"
    id_type_billet = db.Column(db.Integer, db.ForeignKey("type_billet.id_type_billet"), primary_key=True)
    date_jour = db.Column(db.Date, db.ForeignKey("journee.date_jour"), primary_key=True)
    type_billet = db.relationship("TypeBillet", backref=db.backref("acces", lazy="dynamic"))
    journee = db.relationship("Journee", backref=db.backref("acces", lazy="dynamic"))

    def __init__(self, id_type_billet=None, date_jour=None):
        self.id_type_billet = id_type_billet
        self.date_jour = date_jour

    def __repr__(self):
        return "<DonnerAcces %s>" % ([self.id_type_billet, self.date_jour],)


class PreInscrire(db.Model):
    __tablename__ = "pre_inscrire"
    id_spectateur = db.Column(db.Integer, db.ForeignKey("spectateur.id_spectateur"), primary_key=True)
    id_evenement = db.Column(db.Integer, db.ForeignKey("evenement.id_evenement"), primary_key=True)
    spectateur = db.relationship("Spectateur", backref=db.backref("pre_inscriptions", lazy="dynamic"))
    evenement = db.relationship("Evenement", backref=db.backref("pre_inscriptions", lazy="dynamic"))

    def __init__(self, id_spectateur=None, id_evenement=None):
        self.id_spectateur = id_spectateur
        self.id_evenement = id_evenement

    def __repr__(self):
        return "<PreInscrire %s>" % ([self.id_spectateur, self.id_evenement],)


class Participer(db.Model):
    __tablename__ = "participer"
    id_groupe = db.Column(db.Integer, db.ForeignKey("groupe.id_groupe"), primary_key=True)
    id_evenement = db.Column(db.Integer, db.ForeignKey("evenement.id_evenement"), primary_key=True)
    groupe = db.relationship("Groupe", backref=db.backref("participations", lazy="dynamic"))
    evenement = db.relationship("Evenement", backref=db.backref("participations", lazy="dynamic"))

    def __init__(self, id_groupe=None, id_evenement=None):
        self.id_groupe = id_groupe
        self.id_evenement = id_evenement

    def __repr__(self):
        return "<Participer %s>" % ([self.id_groupe, self.id_evenement],)


class Loger(db.Model):
    __tablename__ = "loger"
    id_groupe = db.Column(db.Integer, db.ForeignKey("groupe.id_groupe"), primary_key=True)
    id_hebergement = db.Column(db.Integer, db.ForeignKey("hebergement.id_hebergement"), primary_key=True)
    date_nuit = db.Column(db.Date, db.ForeignKey("date_nuit.date_nuit"), primary_key=True)
    nb_places_necessaires = db.Column(db.Integer, nullable=False)
    groupe = db.relationship("Groupe", backref=db.backref("logements", lazy="dynamic"))
    hebergement = db.relationship("Hebergement", backref=db.backref("logements", lazy="dynamic"))

    def __init__(self, id_groupe=None, id_hebergement=None, date_nuit=None, nb_places_necessaires=None):
        self.id_groupe = id_groupe
        self.id_hebergement = id_hebergement
        self.date_nuit = date_nuit
        self.nb_places_necessaires = nb_places_necessaires

    def __repr__(self):
        return "<Loger %s>" % ([self.id_groupe, self.id_hebergement, self.date_nuit, self.nb_places_necessaires],)


@login_manager.user_loader
def load_user(identifiant):
    return Spectateur.query.filter_by(email=identifiant).first()
