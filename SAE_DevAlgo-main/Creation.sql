USE DBo22504741;

CREATE TABLE MEMBRE (
    id_membre INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL
);

CREATE TABLE INSTRUMENT (
    id_instrument INT AUTO_INCREMENT PRIMARY KEY,
    libelle_instrument VARCHAR(100) NOT NULL
);

CREATE TABLE GROUPE (
    id_groupe INT AUTO_INCREMENT PRIMARY KEY,
    nom_groupe VARCHAR(150) NOT NULL,
    description TEXT,
    liens_photos TEXT,
    liens_reseaux_sociaux TEXT,
    liens_videos TEXT,
    date_heure_arrivee DATETIME,
    date_heure_depart DATETIME
);

CREATE TABLE STYLE_MUSICAL (
    id_style INT AUTO_INCREMENT PRIMARY KEY,
    libelle_style VARCHAR(100) NOT NULL,
    id_style_parent INT,
    FOREIGN KEY (id_style_parent) REFERENCES STYLE_MUSICAL(id_style) ON DELETE SET NULL
);

CREATE TABLE SPECTATEUR (
    id_spectateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL
);

CREATE TABLE TYPE_BILLET (
    id_type_billet INT AUTO_INCREMENT PRIMARY KEY,
    libelle VARCHAR(100) NOT NULL,
    prix DECIMAL(10, 2) NOT NULL
);

CREATE TABLE JOURNEE (
    date_jour DATE PRIMARY KEY,
    heure_debut_officielle TIME NOT NULL,
    heure_fin_officielle TIME NOT NULL
);

CREATE TABLE LIEU (
    id_lieu INT AUTO_INCREMENT PRIMARY KEY,
    nom_lieu VARCHAR(150) NOT NULL,
    adresse VARCHAR(255) NOT NULL,
    jauge_max INT NOT NULL
);

CREATE TABLE HEBERGEMENT (
    id_hebergement INT AUTO_INCREMENT PRIMARY KEY,
    nom_hebergement VARCHAR(150) NOT NULL,
    adresse VARCHAR(255) NOT NULL,
    capacite_places_par_jour INT NOT NULL
);


CREATE TABLE DATE_ACHAT (
    date_achat DATETIME PRIMARY KEY
);

CREATE TABLE DATE_NUIT (
    date_nuit DATE PRIMARY KEY
);


CREATE TABLE EVENEMENT (
    id_evenement INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(150) NOT NULL,
    type_evenement VARCHAR(100) NOT NULL, 
    date_heure_debut DATETIME NOT NULL,
    duree INT NOT NULL, 
    temps_montage INT, 
    temps_demontage INT, 
    est_gratuit BOOLEAN DEFAULT FALSE,
    est_public BOOLEAN DEFAULT TRUE,
    date_jour DATE NOT NULL,
    id_lieu INT NOT NULL,
    FOREIGN KEY (date_jour) REFERENCES JOURNEE(date_jour),
    FOREIGN KEY (id_lieu) REFERENCES LIEU(id_lieu)
);


--- tables assoc

CREATE TABLE JOUER (
    id_membre INT,
    id_instrument INT,
    PRIMARY KEY (id_membre, id_instrument),
    FOREIGN KEY (id_membre) REFERENCES MEMBRE(id_membre),
    FOREIGN KEY (id_instrument) REFERENCES INSTRUMENT(id_instrument)
);

CREATE TABLE COMPOSER (
    id_membre INT,
    id_groupe INT,
    PRIMARY KEY (id_membre, id_groupe),
    FOREIGN KEY (id_membre) REFERENCES MEMBRE(id_membre),
    FOREIGN KEY (id_groupe) REFERENCES GROUPE(id_groupe)
);

CREATE TABLE EST_SIMILAIRE (
    id_groupe INT,
    id_groupe_similaire INT,
    PRIMARY KEY (id_groupe, id_groupe_similaire),
    FOREIGN KEY (id_groupe) REFERENCES GROUPE(id_groupe),
    FOREIGN KEY (id_groupe_similaire) REFERENCES GROUPE(id_groupe)
);

CREATE TABLE AVOIR_STYLE (
    id_groupe INT,
    id_style INT,
    PRIMARY KEY (id_groupe, id_style),
    FOREIGN KEY (id_groupe) REFERENCES GROUPE(id_groupe),
    FOREIGN KEY (id_style) REFERENCES STYLE_MUSICAL(id_style)
);

CREATE TABLE METTRE_EN_FAVORI (
    id_spectateur INT,
    id_groupe INT,
    PRIMARY KEY (id_spectateur, id_groupe),
    FOREIGN KEY (id_spectateur) REFERENCES SPECTATEUR(id_spectateur),
    FOREIGN KEY (id_groupe) REFERENCES GROUPE(id_groupe)
);

CREATE TABLE ACHETER (
    id_spectateur INT,
    id_type_billet INT,
    date_achat DATETIME,
    PRIMARY KEY (id_spectateur, id_type_billet, date_achat),
    FOREIGN KEY (id_spectateur) REFERENCES SPECTATEUR(id_spectateur),
    FOREIGN KEY (id_type_billet) REFERENCES TYPE_BILLET(id_type_billet),
    FOREIGN KEY (date_achat) REFERENCES DATE_ACHAT(date_achat)
);

CREATE TABLE DONNER_ACCES (
    id_type_billet INT,
    date_jour DATE,
    PRIMARY KEY (id_type_billet, date_jour),
    FOREIGN KEY (id_type_billet) REFERENCES TYPE_BILLET(id_type_billet),
    FOREIGN KEY (date_jour) REFERENCES JOURNEE(date_jour)
);

CREATE TABLE PRE_INSCRIRE (
    id_spectateur INT,
    id_evenement INT,
    PRIMARY KEY (id_spectateur, id_evenement),
    FOREIGN KEY (id_spectateur) REFERENCES SPECTATEUR(id_spectateur),
    FOREIGN KEY (id_evenement) REFERENCES EVENEMENT(id_evenement)
);

CREATE TABLE PARTICIPER (
    id_groupe INT,
    id_evenement INT,
    PRIMARY KEY (id_groupe, id_evenement),
    FOREIGN KEY (id_groupe) REFERENCES GROUPE(id_groupe),
    FOREIGN KEY (id_evenement) REFERENCES EVENEMENT(id_evenement)
);

CREATE TABLE LOGER (
    id_groupe INT,
    id_hebergement INT,
    date_nuit DATE,
    nb_places_necessaires INT NOT NULL,
    PRIMARY KEY (id_groupe, id_hebergement, date_nuit),
    FOREIGN KEY (id_groupe) REFERENCES GROUPE(id_groupe),
    FOREIGN KEY (id_hebergement) REFERENCES HEBERGEMENT(id_hebergement),
    FOREIGN KEY (date_nuit) REFERENCES DATE_NUIT(date_nuit)
);

-- ============================================================
-- Fonctions, procedures et triggers
-- ============================================================

DELIMITER $$

CREATE FUNCTION CalculerOccupationLieu(
    p_id_lieu INT,
    p_date_jour DATE
)
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE v_occupation INT;

    SELECT COUNT(*)
    INTO v_occupation
    FROM PRE_INSCRIRE pi
    INNER JOIN EVENEMENT e
        ON e.id_evenement = pi.id_evenement
    WHERE e.id_lieu = p_id_lieu
      AND e.date_jour = p_date_jour;

    RETURN v_occupation;
END$$

CREATE PROCEDURE AcheterBilletTransaction(
    IN p_id_spectateur INT,
    IN p_id_type_billet INT,
    IN p_date_achat DATETIME
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    INSERT INTO DATE_ACHAT (date_achat)
    VALUES (p_date_achat);

    INSERT INTO ACHETER (
        id_spectateur,
        id_type_billet,
        date_achat
    ) VALUES (
        p_id_spectateur,
        p_id_type_billet,
        p_date_achat
    );

    COMMIT;
END$$

CREATE FUNCTION nombre_places_logees(
    p_id_hebergement INT,
    p_date_nuit DATE
)
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE v_places INT;

    SELECT COALESCE(SUM(nb_places_necessaires), 0)
    INTO v_places
    FROM LOGER
    WHERE id_hebergement = p_id_hebergement
      AND date_nuit = p_date_nuit;

    RETURN v_places;
END$$

CREATE PROCEDURE inscrire_groupe_hebergement(
    IN p_id_groupe INT,
    IN p_id_hebergement INT,
    IN p_date_nuit DATE,
    IN p_nb_places INT
)
BEGIN
    INSERT INTO LOGER (
        id_groupe,
        id_hebergement,
        date_nuit,
        nb_places_necessaires
    ) VALUES (
        p_id_groupe,
        p_id_hebergement,
        p_date_nuit,
        p_nb_places
    );
END$$

CREATE TRIGGER verifier_places_logement_avant_insertion
BEFORE INSERT ON LOGER
FOR EACH ROW
BEGIN
    DECLARE v_capacite INT;
    DECLARE v_places_occupees INT;

    IF NEW.nb_places_necessaires <= 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Le nombre de places doit etre positif';
    END IF;

    SELECT capacite_places_par_jour
    INTO v_capacite
    FROM HEBERGEMENT
    WHERE id_hebergement = NEW.id_hebergement;

    SET v_places_occupees = nombre_places_logees(
        NEW.id_hebergement,
        NEW.date_nuit
    );

    IF v_places_occupees + NEW.nb_places_necessaires > v_capacite THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La capacite de l hebergement est depassee';
    END IF;
END$$

CREATE TRIGGER verifier_horaires_evenement_avant_insertion
BEFORE INSERT ON EVENEMENT
FOR EACH ROW
BEGIN
    DECLARE v_heure_debut TIME;
    DECLARE v_heure_fin TIME;
    DECLARE v_heure_fin_evenement TIME;

    SELECT heure_debut_officielle, heure_fin_officielle
    INTO v_heure_debut, v_heure_fin
    FROM JOURNEE
    WHERE date_jour = NEW.date_jour;

    SET v_heure_fin_evenement = ADDTIME(
        TIME(NEW.date_heure_debut),
        SEC_TO_TIME(NEW.duree * 60)
    );

    IF DATE(NEW.date_heure_debut) <> NEW.date_jour
       OR TIME(NEW.date_heure_debut) < v_heure_debut
       OR v_heure_fin_evenement > v_heure_fin THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'L evenement depasse les horaires de la journee';
    END IF;
END$$

CREATE TRIGGER TRG_Check_Droit_PreInscription
BEFORE INSERT ON PRE_INSCRIRE
FOR EACH ROW
BEGIN
    DECLARE v_droit INT DEFAULT 0;

    SELECT COUNT(*)
    INTO v_droit
    FROM ACHETER a
    INNER JOIN DONNER_ACCES da
        ON da.id_type_billet = a.id_type_billet
    INNER JOIN EVENEMENT e
        ON e.date_jour = da.date_jour
    WHERE a.id_spectateur = NEW.id_spectateur
      AND e.id_evenement = NEW.id_evenement;

    IF v_droit = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                'Le spectateur ne possede aucun billet donnant acces a cette journee';
    END IF;
END$$

CREATE TRIGGER TRG_Check_Jauge_Lieu
BEFORE INSERT ON PRE_INSCRIRE
FOR EACH ROW
BEGIN
    DECLARE v_id_lieu INT;
    DECLARE v_date_jour DATE;
    DECLARE v_jauge_max INT;
    DECLARE v_occupation INT DEFAULT 0;

    SELECT id_lieu, date_jour
    INTO v_id_lieu, v_date_jour
    FROM EVENEMENT
    WHERE id_evenement = NEW.id_evenement;

    SELECT jauge_max
    INTO v_jauge_max
    FROM LIEU
    WHERE id_lieu = v_id_lieu;

    SET v_occupation = CalculerOccupationLieu(v_id_lieu, v_date_jour);

    IF v_occupation >= v_jauge_max THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La jauge maximale du lieu est atteinte';
    END IF;
END$$

CREATE TRIGGER TRG_Check_PreInscription_Est_Public
BEFORE INSERT ON PRE_INSCRIRE
FOR EACH ROW
BEGIN
    DECLARE v_est_public BOOLEAN;

    SELECT est_public
    INTO v_est_public
    FROM EVENEMENT
    WHERE id_evenement = NEW.id_evenement;

    IF v_est_public = FALSE THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                'La pre-inscription est reservee aux evenements publics';
    END IF;
END$$

CREATE FUNCTION CalculerDispoHebergement(
    p_id_hebergement INT,
    p_date_nuit DATE
)
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE v_capacite INT;
    DECLARE v_places_occupees INT;

    SELECT capacite_places_par_jour
    INTO v_capacite
    FROM HEBERGEMENT
    WHERE id_hebergement = p_id_hebergement;

    SELECT COALESCE(SUM(nb_places_necessaires), 0)
    INTO v_places_occupees
    FROM LOGER
    WHERE id_hebergement = p_id_hebergement
      AND date_nuit = p_date_nuit;

    RETURN v_capacite - v_places_occupees;
END$$

CREATE TRIGGER TRG_Check_Capacite_Hebergement
BEFORE INSERT ON LOGER
FOR EACH ROW
BEGIN
    IF NEW.nb_places_necessaires <= 0
       OR NEW.nb_places_necessaires > CalculerDispoHebergement(
           NEW.id_hebergement,
           NEW.date_nuit
       ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                'La capacite de l hebergement est depassee ou le nombre de lits est invalide';
    END IF;
END$$

CREATE TRIGGER TRG_Check_Taille_Groupe
BEFORE INSERT ON LOGER
FOR EACH ROW
BEGIN
    DECLARE v_nb_membres INT;

    SELECT COUNT(*)
    INTO v_nb_membres
    FROM COMPOSER
    WHERE id_groupe = NEW.id_groupe;

    IF NEW.nb_places_necessaires < v_nb_membres THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                'Le nombre de lits demandes est inferieur a la taille du groupe';
    END IF;
END$$

CREATE TRIGGER TRG_Check_Temps_Repos_Groupe
BEFORE INSERT ON PARTICIPER
FOR EACH ROW
BEGIN
    DECLARE v_conflit INT DEFAULT 0;

    SELECT COUNT(*)
    INTO v_conflit
    FROM PARTICIPER p
    INNER JOIN EVENEMENT e_existant
        ON e_existant.id_evenement = p.id_evenement
    INNER JOIN EVENEMENT e_nouveau
        ON e_nouveau.id_evenement = NEW.id_evenement
    WHERE p.id_groupe = NEW.id_groupe
      AND (
          (
              e_existant.date_heure_debut <= e_nouveau.date_heure_debut
              AND ADDTIME(
                  e_existant.date_heure_debut,
                  SEC_TO_TIME(
                      (e_existant.duree
                       + COALESCE(e_existant.temps_demontage, 0)
                       + COALESCE(e_nouveau.temps_montage, 0)) * 60
                  )
              ) > e_nouveau.date_heure_debut
          )
          OR (
              e_nouveau.date_heure_debut < e_existant.date_heure_debut
              AND ADDTIME(
                  e_nouveau.date_heure_debut,
                  SEC_TO_TIME(
                      (e_nouveau.duree
                       + COALESCE(e_nouveau.temps_demontage, 0)
                       + COALESCE(e_existant.temps_montage, 0)) * 60
                  )
              ) > e_existant.date_heure_debut
          )
      );

    IF v_conflit > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                'Le temps de montage ou de demontage du groupe est insuffisant';
    END IF;
END$$

CREATE TRIGGER TRG_Check_Arrivee_Depart
BEFORE INSERT ON PARTICIPER
FOR EACH ROW
BEGIN
    DECLARE v_date_arrivee DATETIME;
    DECLARE v_date_depart DATETIME;
    DECLARE v_date_debut_evenement DATETIME;
    DECLARE v_date_fin_evenement DATETIME;

    SELECT date_heure_arrivee, date_heure_depart
    INTO v_date_arrivee, v_date_depart
    FROM GROUPE
    WHERE id_groupe = NEW.id_groupe;

    SELECT date_heure_debut,
           ADDTIME(
               date_heure_debut,
        SEC_TO_TIME(duree * 60)
           )
    INTO v_date_debut_evenement, v_date_fin_evenement
    FROM EVENEMENT
    WHERE id_evenement = NEW.id_evenement;

    IF v_date_arrivee > v_date_debut_evenement
       OR v_date_depart < v_date_fin_evenement THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                'Les dates d arrivee et de depart du groupe sont incompatibles avec l evenement';
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE GenererRecommandations(
    IN p_id_spectateur INT
)
BEGIN
    DECLARE v_termine INT DEFAULT 0;
    DECLARE v_id_groupe INT;
    DECLARE v_id_groupe_similaire INT;
    DECLARE recommandations CURSOR FOR
        SELECT mf.id_groupe, es.id_groupe_similaire
        FROM METTRE_EN_FAVORI mf
        INNER JOIN EST_SIMILAIRE es
            ON es.id_groupe = mf.id_groupe
        WHERE mf.id_spectateur = p_id_spectateur;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_termine = 1;

    DROP TEMPORARY TABLE IF EXISTS recommandations_temp;
    CREATE TEMPORARY TABLE recommandations_temp (
        id_groupe INT PRIMARY KEY
    );

    OPEN recommandations;

    boucle_recommandations: LOOP
        FETCH recommandations
        INTO v_id_groupe, v_id_groupe_similaire;

        IF v_termine = 1 THEN
            LEAVE boucle_recommandations;
        END IF;

        INSERT IGNORE INTO recommandations_temp (id_groupe)
        VALUES (v_id_groupe_similaire);
    END LOOP;

    CLOSE recommandations;

    SELECT g.id_groupe, g.nom_groupe, g.description
    FROM recommandations_temp rt
    INNER JOIN GROUPE g
        ON g.id_groupe = rt.id_groupe
    ORDER BY g.nom_groupe;

    DROP TEMPORARY TABLE recommandations_temp;
END$$

CREATE FUNCTION RechercherGroupesParStyle(
    p_id_style INT
)
RETURNS TEXT
READS SQL DATA
BEGIN
    DECLARE v_resultat TEXT;

    WITH RECURSIVE styles_descendants AS (
        SELECT id_style
        FROM STYLE_MUSICAL
        WHERE id_style = p_id_style

        UNION ALL

        SELECT sm.id_style
        FROM STYLE_MUSICAL sm
        INNER JOIN styles_descendants sd
            ON sm.id_style_parent = sd.id_style
    )
    SELECT GROUP_CONCAT(
               DISTINCT CONCAT(g.id_groupe, ': ', g.nom_groupe)
               ORDER BY g.nom_groupe
               SEPARATOR ', '
           )
    INTO v_resultat
    FROM AVOIR_STYLE als
    INNER JOIN styles_descendants sd
        ON sd.id_style = als.id_style
    INNER JOIN GROUPE g
        ON g.id_groupe = als.id_groupe;

    RETURN COALESCE(v_resultat, '');
END$$

CREATE FUNCTION OrganiserJourneeSpectateur(
    p_id_spectateur INT
)
RETURNS TEXT
READS SQL DATA
BEGIN
    DECLARE v_resultat TEXT;

    SELECT GROUP_CONCAT(
               CONCAT(
                   DATE_FORMAT(e.date_heure_debut, '%Y-%m-%d %H:%i'),
                   ' - ',
                   e.titre,
                   ' (',
                   l.nom_lieu,
                   ')'
               )
               ORDER BY e.date_heure_debut
               SEPARATOR ' | '
           )
    INTO v_resultat
    FROM PRE_INSCRIRE pi
    INNER JOIN EVENEMENT e
        ON e.id_evenement = pi.id_evenement
    INNER JOIN LIEU l
        ON l.id_lieu = e.id_lieu
    WHERE pi.id_spectateur = p_id_spectateur;

    RETURN COALESCE(v_resultat, '');
END$$

CREATE PROCEDURE AjouterRelationSimilaire(
    IN p_id_groupe INT,
    IN p_id_groupe_similaire INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    INSERT IGNORE INTO EST_SIMILAIRE (
        id_groupe,
        id_groupe_similaire
    ) VALUES
        (p_id_groupe, p_id_groupe_similaire),
        (p_id_groupe_similaire, p_id_groupe);

    COMMIT;
END$$

CREATE TRIGGER TRG_Check_Boucle_Style
BEFORE INSERT ON STYLE_MUSICAL
FOR EACH ROW
BEGIN
    DECLARE v_style INT;
    DECLARE v_parent INT;
    DECLARE v_termine INT DEFAULT 0;

    SET v_style = NEW.id_style_parent;

    WHILE v_style IS NOT NULL AND v_termine = 0 DO
        IF v_style = NEW.id_style THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT =
                    'La hierarchie des styles contient une boucle';
        END IF;

        SELECT id_style_parent
        INTO v_parent
        FROM STYLE_MUSICAL
        WHERE id_style = v_style;

        IF v_parent IS NULL THEN
            SET v_termine = 1;
        ELSE
            SET v_style = v_parent;
        END IF;
    END WHILE;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER TRG_Check_Chevauchement_Lieu
BEFORE INSERT ON EVENEMENT
FOR EACH ROW
BEGIN
    DECLARE v_conflits INT DEFAULT 0;

    SELECT COUNT(*)
    INTO v_conflits
    FROM EVENEMENT e
    WHERE e.id_lieu = NEW.id_lieu
      AND DATE_SUB(
              NEW.date_heure_debut,
              INTERVAL COALESCE(NEW.temps_montage, 0) MINUTE
          ) < ADDTIME(
              e.date_heure_debut,
              SEC_TO_TIME(
                  (e.duree + COALESCE(e.temps_demontage, 0)) * 60
              )
          )
      AND ADDTIME(
              NEW.date_heure_debut,
              SEC_TO_TIME(
                  (NEW.duree + COALESCE(NEW.temps_demontage, 0)) * 60
              )
          ) > DATE_SUB(
              e.date_heure_debut,
              INTERVAL COALESCE(e.temps_montage, 0) MINUTE
          );

    IF v_conflits > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                'Deux evenements se chevauchent dans le meme lieu';
    END IF;
END$$

CREATE TRIGGER TRG_Check_Inclusion_Journee
BEFORE INSERT ON EVENEMENT
FOR EACH ROW
BEGIN
    DECLARE v_heure_debut TIME;
    DECLARE v_heure_fin TIME;
    DECLARE v_debut_journee DATETIME;
    DECLARE v_fin_journee DATETIME;
    DECLARE v_fin_evenement DATETIME;

    SELECT heure_debut_officielle, heure_fin_officielle
    INTO v_heure_debut, v_heure_fin
    FROM JOURNEE
    WHERE date_jour = NEW.date_jour;

    SET v_debut_journee = TIMESTAMP(NEW.date_jour, v_heure_debut);
    SET v_fin_journee = TIMESTAMP(NEW.date_jour, v_heure_fin);
    IF v_fin_journee < v_debut_journee THEN
        SET v_fin_journee = DATE_ADD(v_fin_journee, INTERVAL 1 DAY);
    END IF;

    SET v_fin_evenement = ADDTIME(
        NEW.date_heure_debut,
        SEC_TO_TIME(NEW.duree * 60)
    );

    IF NEW.date_heure_debut < v_debut_journee
       OR v_fin_evenement > v_fin_journee THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                'L evenement depasse les horaires officiels de la journee';
    END IF;
END$$

CREATE TRIGGER TRG_Check_Ubiquite_Spectateur
BEFORE INSERT ON PRE_INSCRIRE
FOR EACH ROW
BEGIN
    DECLARE v_debut_nouvel_evenement DATETIME;
    DECLARE v_fin_nouvel_evenement DATETIME;
    DECLARE v_conflits INT DEFAULT 0;

    SELECT date_heure_debut,
           ADDTIME(date_heure_debut, SEC_TO_TIME(duree * 60))
    INTO v_debut_nouvel_evenement, v_fin_nouvel_evenement
    FROM EVENEMENT
    WHERE id_evenement = NEW.id_evenement;

    SELECT COUNT(*)
    INTO v_conflits
    FROM PRE_INSCRIRE pi
    INNER JOIN EVENEMENT e
        ON e.id_evenement = pi.id_evenement
    WHERE pi.id_spectateur = NEW.id_spectateur
      AND e.date_heure_debut < v_fin_nouvel_evenement
      AND ADDTIME(e.date_heure_debut, SEC_TO_TIME(e.duree * 60))
          > v_debut_nouvel_evenement;

    IF v_conflits > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                'Le spectateur est deja inscrit sur ce creneau';
    END IF;
END$$

CREATE PROCEDURE InscrireGroupeHebergementTransaction(
    IN p_id_groupe INT,
    IN p_id_hebergement INT,
    IN p_date_nuit DATE,
    IN p_nb_places INT
)
BEGIN
    DECLARE v_capacite INT;
    DECLARE v_places_occupees INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT capacite_places_par_jour
    INTO v_capacite
    FROM HEBERGEMENT
    WHERE id_hebergement = p_id_hebergement
    FOR UPDATE;

    SELECT COALESCE(SUM(nb_places_necessaires), 0)
    INTO v_places_occupees
    FROM LOGER
    WHERE id_hebergement = p_id_hebergement
      AND date_nuit = p_date_nuit
    FOR UPDATE;

    IF p_nb_places <= 0 OR v_places_occupees + p_nb_places > v_capacite THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                'La capacite de l hebergement est depassee ou le nombre de lits est invalide';
    END IF;

    INSERT INTO LOGER (
        id_groupe,
        id_hebergement,
        date_nuit,
        nb_places_necessaires
    ) VALUES (
        p_id_groupe,
        p_id_hebergement,
        p_date_nuit,
        p_nb_places
    );

    COMMIT;
END$$

CREATE INDEX idx_evt_public ON EVENEMENT (est_public, est_gratuit)$$
CREATE INDEX idx_evt_date ON EVENEMENT (date_heure_debut)$$
CREATE INDEX idx_groupe_style ON AVOIR_STYLE (id_style)$$

DELIMITER ;