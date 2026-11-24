"""Un concert, tel que les algorithmes de recommandation le manipulent."""


class Concert:
    def __init__(self, id, debut, fin, genres=(), score=0.0, lieu=None):
        self.id = id          # EVENEMENT.id_evenement
        self.debut = debut    # EVENEMENT.date_heure_debut
        self.fin = fin        # début + durée (sans montage/démontage)
        self.genres = genres  # ids des styles des groupes qui jouent
        self.score = score    # score calculé pour un spectateur
        self.lieu = lieu      # LIEU.id_lieu (optionnel)