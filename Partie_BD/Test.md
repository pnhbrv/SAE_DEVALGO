# Tests de la base

## 1. Installation

On a fait les tests avec la base de données de `Gihed MAAMATOU`
Il faudra donc remplacer `o22504741` par `votre login`

```bash
mysql -h servinfo-maria -u o22504741 -p --skip-ssl
```

Dans MariaDB :

```sql
USE DBo22504741;
SOURCE Suppression.sql;
SOURCE Creation.sql;
SOURCE insertion.sql;
```

Ne pas relancer `insertion.sql` sans relancer les deux autres scripts.

## 2. Vérification

```sql
SHOW TABLES;
SHOW FUNCTION STATUS WHERE Db = 'DBo22504741';
SHOW PROCEDURE STATUS WHERE Db = 'DBo22504741';
SHOW TRIGGERS FROM DBo22504741;
```



```sql
SELECT COUNT(*) FROM MEMBRE;
SELECT COUNT(*) FROM GROUPE;
SELECT COUNT(*) FROM STYLE_MUSICAL;
SELECT COUNT(*) FROM EVENEMENT;
SELECT COUNT(*) FROM PRE_INSCRIRE;
SELECT COUNT(*) FROM PARTICIPER;
SELECT COUNT(*) FROM LOGER;
```

Résultats  :

```text
MEMBRE: 9
GROUPE: 10
STYLE_MUSICAL: 10
EVENEMENT: 5
PRE_INSCRIRE: 5
PARTICIPER: 5
LOGER: 7
```

## 3. Billetterie

```sql
SELECT CalculerOccupationLieu(1, '2026-10-12');
-- Résultat : 1

CALL AcheterBilletTransaction(1, 1, '2026-06-21 10:00:00');
```

Relancer pour tester rollback :

```sql
CALL AcheterBilletTransaction(1, 1, '2026-06-21 10:00:00');
-- Erreur 
```

Tester un spectateur sans droit :

```sql
INSERT INTO PRE_INSCRIRE (id_spectateur, id_evenement)
VALUES (4, 1);
-- Erreur 
```

Tester un événement privé :

```sql
UPDATE EVENEMENT SET est_public = FALSE WHERE id_evenement = 1;
INSERT INTO PRE_INSCRIRE (id_spectateur, id_evenement)
VALUES (3, 1);
-- Erreur 
UPDATE EVENEMENT SET est_public = TRUE WHERE id_evenement = 1;
```

Tester la jauge :

```sql
UPDATE LIEU SET jauge_max = 1 WHERE id_lieu = 1;
INSERT INTO PRE_INSCRIRE (id_spectateur, id_evenement)
VALUES (3, 1);
-- Erreur 
UPDATE LIEU SET jauge_max = 5000 WHERE id_lieu = 1;
```

## 4. Hébergements et groupes

```sql
SELECT CalculerDispoHebergement(1, '2026-10-12');
-- Résultat : 76
```

Tester la capacité :

```sql
UPDATE HEBERGEMENT
SET capacite_places_par_jour = 2
WHERE id_hebergement = 1;

INSERT INTO LOGER
    (id_groupe, id_hebergement, date_nuit, nb_places_necessaires)
VALUES (1, 1, '2026-10-15', 3);
-- Erreur 

UPDATE HEBERGEMENT
SET capacite_places_par_jour = 80
WHERE id_hebergement = 1;
```

Tester la taille du groupe :

```sql
INSERT INTO LOGER
    (id_groupe, id_hebergement, date_nuit, nb_places_necessaires)
VALUES (1, 1, '2026-10-15', 1);
-- Erreur 
```

## 5. Recherche et recommandations

```sql
SELECT RechercherGroupesParStyle(1);
SELECT OrganiserJourneeSpectateur(1);
CALL GenererRecommandations(1);
```

Tester les relations similaires :

```sql
CALL AjouterRelationSimilaire(5, 6);

SELECT *
FROM EST_SIMILAIRE
WHERE (id_groupe = 5 AND id_groupe_similaire = 6)
   OR (id_groupe = 6 AND id_groupe_similaire = 5);
-- Deux lignes

DELETE FROM EST_SIMILAIRE
WHERE (id_groupe = 5 AND id_groupe_similaire = 6)
   OR (id_groupe = 6 AND id_groupe_similaire = 5);
```

Tester une boucle de style :

```sql
INSERT INTO STYLE_MUSICAL
    (id_style, libelle_style, id_style_parent)
VALUES (11, 'Style cyclique', 11);
-- Erreur 
```

## 6. Planning

Créer un événement qui marche avant les tests :

```sql
INSERT INTO EVENEMENT (
    id_evenement, titre, type_evenement, date_heure_debut, duree,
    temps_montage, temps_demontage, est_gratuit, est_public,
    date_jour, id_lieu
) VALUES (
    6, 'Test', 'Concert', '2026-10-15 18:00:00', 60,
    10, 10, TRUE, TRUE, '2026-10-15', 1
);
```

Tester une participation qui marche :

```sql
INSERT INTO PARTICIPER (id_groupe, id_evenement)
VALUES (1, 6);
-- Insertion 
```

Tester hébergement :

```sql
CALL InscrireGroupeHebergementTransaction(2, 2, '2026-10-15', 2);
-- Insertion 

CALL InscrireGroupeHebergementTransaction(2, 2, '2026-10-14', 1000);
-- Erreur 
```

## 7. Index

```sql
SHOW INDEX FROM EVENEMENT;
SHOW INDEX FROM AVOIR_STYLE;

EXPLAIN
SELECT * FROM EVENEMENT
WHERE est_public = TRUE AND est_gratuit = FALSE;

EXPLAIN
SELECT * FROM EVENEMENT
WHERE date_heure_debut >= '2026-10-12 00:00:00';

EXPLAIN
SELECT * FROM AVOIR_STYLE
WHERE id_style = 1;
```

Index  :

```text
idx_evt_public
idx_evt_date
idx_groupe_style
```

## 8. Nettoyage

```sql
DELETE FROM PARTICIPER WHERE id_evenement = 6;
DELETE FROM EVENEMENT WHERE id_evenement = 6;
DELETE FROM LOGER
WHERE id_groupe = 2
  AND id_hebergement = 2
  AND date_nuit = '2026-10-15';
```

Pour tout remettre à zéro :

```sql
SOURCE Suppression.sql;
SOURCE Creation.sql;
SOURCE insertion.sql;
```
