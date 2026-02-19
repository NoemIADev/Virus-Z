USE virus_z;

-- ======================
-- ADRESSES DOMICILE / TRAVAIL
-- ======================

-- On crée quelques adresses réutilisables
INSERT INTO adresse (ligne1, code_postal, ville, latitude, longitude)
VALUES ('12 Rue Victor Hugo', '31000', 'Toulouse', 43.6045, 1.4440);
SET @adr1 = LAST_INSERT_ID();

INSERT INTO adresse (ligne1, code_postal, ville, latitude, longitude)
VALUES ('8 Avenue Jean Médecin', '06000', 'Nice', 43.7010, 7.2650);
SET @adr2 = LAST_INSERT_ID();

INSERT INTO adresse (ligne1, code_postal, ville, latitude, longitude)
VALUES ('5 Rue de la République', '69002', 'Lyon', 45.7600, 4.8357);
SET @adr3 = LAST_INSERT_ID();

INSERT INTO adresse (ligne1, code_postal, ville, latitude, longitude)
VALUES ('22 Boulevard de Strasbourg', '75010', 'Paris', 48.8720, 2.3570);
SET @adr4 = LAST_INSERT_ID();

-- ======================
-- CAS
-- ======================

INSERT INTO cas
(nom, prenom, age, sexe, date_infection_estimee,
 virus_id, mise_en_quarantaine, lieu_quarantaine_id,
 quarantaine_date_debut,
 domicile_adresse_id, travail_adresse_id)
VALUES

('Martin','Lucas',28,'H','2026-02-10',1, TRUE, 1,'2026-02-11', NULL, NULL),

('Dubois','Emma',34,'F','2026-02-09',2, TRUE, 2,'2026-02-10', NULL, NULL),

('Bernard','Hugo',19,'H','2026-02-08',3, FALSE, NULL,NULL, @adr1, NULL),

('Moreau','Chloé',41,'F','2026-02-07',4, TRUE, 3,'2026-02-08', NULL, NULL),

('Laurent','Nathan',30,'H','2026-02-06',5, FALSE, NULL,NULL, @adr2, @adr3),

('Simon','Lina',25,'F','2026-02-05',6, TRUE, 4,'2026-02-06', NULL, NULL),

('Michel','Tom',37,'H','2026-02-04',7, FALSE, NULL,NULL, @adr3, NULL),

('Garcia','Inès',29,'F','2026-02-03',8, TRUE, 5,'2026-02-04', NULL, NULL),

('Roux','Noah',22,'H','2026-02-02',3, FALSE, NULL,NULL, @adr1, @adr4),

('Fournier','Lea',31,'F','2026-02-01',2, TRUE, 6,'2026-02-02', NULL, NULL),

('Girard','Ethan',45,'H','2026-01-31',1, FALSE, NULL,NULL, @adr4, NULL),

('Andre','Camille',27,'F','2026-01-30',4, TRUE, 7,'2026-01-31', NULL, NULL),

('Mercier','Adam',33,'H','2026-01-29',5, FALSE, NULL,NULL, @adr2, @adr1),

('Dupont','Sarah',26,'F','2026-01-28',6, TRUE, 8,'2026-01-29', NULL, NULL),

('Lambert','Julien',39,'H','2026-01-27',3, FALSE, NULL,NULL, @adr3, NULL),

('Bonnet','Manon',21,'F','2026-01-26',8, TRUE, 1,'2026-01-27', NULL, NULL),

('Francois','Maxime',36,'H','2026-01-25',7, FALSE, NULL,NULL, @adr1, @adr2),

('Leclerc','Eva',24,'F','2026-01-24',2, TRUE, 2,'2026-01-25', NULL, NULL),

('Garnier','Leo',32,'H','2026-01-23',1, FALSE, NULL,NULL, @adr4, @adr3),

('Chevalier','Zoé',28,'F','2026-01-22',6, TRUE, 3,'2026-01-23', NULL, NULL);
