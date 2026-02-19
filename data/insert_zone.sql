USE virus_z;

-- ======================
-- ZONES DE QUARANTAINE (FRANCE)
-- ======================

-- 1) Paris — Pitié-Salpêtrière
INSERT INTO adresse (ligne1, code_postal, ville, latitude, longitude)
VALUES ('47 Boulevard de l''Hôpital', '75013', 'Paris', 48.837079, 2.365043);
SET @adr_id = LAST_INSERT_ID();
INSERT INTO lieu_quarantaine (nom, type, adresse_id)
VALUES ('Groupe hospitalier Pitié-Salpêtrière', 'HOPITAL', @adr_id);

-- 2) Marseille — La Timone
INSERT INTO adresse (ligne1, code_postal, ville, latitude, longitude)
VALUES ('264 Rue Saint-Pierre', '13005', 'Marseille', 43.290436, 5.402049);
SET @adr_id = LAST_INSERT_ID();
INSERT INTO lieu_quarantaine (nom, type, adresse_id)
VALUES ('Hôpital de la Timone (AP-HM)', 'HOPITAL', @adr_id);

-- 3) Lyon — Édouard-Herriot
INSERT INTO adresse (ligne1, code_postal, ville, latitude, longitude)
VALUES ('5 Place d''Arsonval', '69003', 'Lyon', 45.743612, 4.880319);
SET @adr_id = LAST_INSERT_ID();
INSERT INTO lieu_quarantaine (nom, type, adresse_id)
VALUES ('Hôpital Édouard-Herriot (HCL)', 'HOPITAL', @adr_id);

-- 4) Bordeaux — Pellegrin
INSERT INTO adresse (ligne1, code_postal, ville, latitude, longitude)
VALUES ('Place Amélie Raba-Léon', '33000', 'Bordeaux', 44.830310, -0.603290);
SET @adr_id = LAST_INSERT_ID();
INSERT INTO lieu_quarantaine (nom, type, adresse_id)
VALUES ('Hôpital Pellegrin (CHU Bordeaux)', 'HOPITAL', @adr_id);

-- 5) Toulouse — Purpan
INSERT INTO adresse (ligne1, code_postal, ville, latitude, longitude)
VALUES ('Place du Dr Joseph Baylac', '31059', 'Toulouse', 43.608600, 1.401676);
SET @adr_id = LAST_INSERT_ID();
INSERT INTO lieu_quarantaine (nom, type, adresse_id)
VALUES ('Hôpital Purpan (CHU Toulouse)', 'HOPITAL', @adr_id);

-- 6) Lille — CHU Lille
INSERT INTO adresse (ligne1, code_postal, ville, latitude, longitude)
VALUES ('1 Place de Verdun', '59045', 'Lille', 50.620000, 3.140000);
SET @adr_id = LAST_INSERT_ID();
INSERT INTO lieu_quarantaine (nom, type, adresse_id)
VALUES ('CHU de Lille — Place de Verdun', 'HOPITAL', @adr_id);

-- 7) Strasbourg — Nouvel Hôpital Civil
INSERT INTO adresse (ligne1, code_postal, ville, latitude, longitude)
VALUES ('1 Place de l''Hôpital', '67091', 'Strasbourg', 48.575961, 7.743571);
SET @adr_id = LAST_INSERT_ID();
INSERT INTO lieu_quarantaine (nom, type, adresse_id)
VALUES ('Nouvel Hôpital Civil (HUS)', 'HOPITAL', @adr_id);

-- 8) Nantes — Hôtel-Dieu
INSERT INTO adresse (ligne1, code_postal, ville, latitude, longitude)
VALUES ('1 Place Alexis-Ricordeau', '44093', 'Nantes', 47.211913, -1.554070);
SET @adr_id = LAST_INSERT_ID();
INSERT INTO lieu_quarantaine (nom, type, adresse_id)
VALUES ('Hôtel-Dieu (CHU Nantes)', 'HOPITAL', @adr_id);
