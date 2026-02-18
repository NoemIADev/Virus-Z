CREATE DATABASE IF NOT EXISTS virus_z;
USE virus_z;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS cas;
DROP TABLE IF EXISTS lieu_quarantaine;
DROP TABLE IF EXISTS adresse;
DROP TABLE IF EXISTS virus;

SET FOREIGN_KEY_CHECKS = 1;

-- ======================
-- VIRUS (COMPLET)
-- ======================
CREATE TABLE virus (
  id INT AUTO_INCREMENT,
  nom VARCHAR(120) NOT NULL,
  variante VARCHAR(120) NOT NULL,
  mode_propagation VARCHAR(120),
  incubation_min INT,
  incubation_max INT,
  contagiosite int,
  moyens_detection VARCHAR(120),
  commentaire TEXT,
  PRIMARY KEY (id)
  UNIQUE KEY uq_virus_nom_variante (nom, variante) 'combinaison unique de virus variant pour eviter les doublon'
) ENGINE=InnoDB;

-- ======================
-- ADRESSE 
-- ======================
CREATE TABLE adresse (
  id INT AUTO_INCREMENT,
  ligne1 VARCHAR(255) NOT NULL,
  code_postal VARCHAR(20) NOT NULL,
  ville VARCHAR(120) NOT NULL,
  latitude DECIMAL(9,6),
  longitude DECIMAL(9,6),
  PRIMARY KEY (id)
) ENGINE=InnoDB;

  

-- ======================
-- LIEU DE QUARANTAINE (lieu réel)
-- ======================
CREATE TABLE lieu_quarantaine (
  id INT AUTO_INCREMENT,
  nom VARCHAR(160) NOT NULL,
  type VARCHAR(50),          -- ex: HOPITAL / HOTEL / GYMNASE / ...
  adresse_id INT NOT NULL,

  PRIMARY KEY (id),
  FOREIGN KEY (adresse_id) REFERENCES adresse(id)
) ENGINE=InnoDB;

-- ======================
-- CAS (liens directs)
-- ======================
CREATE TABLE cas (
  id INT AUTO_INCREMENT,

  nom VARCHAR(100) NOT NULL,
  prenom VARCHAR(100) NOT NULL,
  age INT,
  sexe VARCHAR(20),
  date_infection_estimee DATE,

  virus_id INT NOT NULL,

  mise_en_quarantaine BOOLEAN NOT NULL,
  lieu_quarantaine_id INT NULL,
  quarantaine_date_debut DATE,

  domicile_adresse_id INT NOT NULL,
  travail_adresse_id INT NULL,

  PRIMARY KEY (id),

  FOREIGN KEY (virus_id) REFERENCES virus(id),
  FOREIGN KEY (lieu_quarantaine_id) REFERENCES lieu_quarantaine(id),
  FOREIGN KEY (domicile_adresse_id) REFERENCES adresse(id),
  FOREIGN KEY (travail_adresse_id) REFERENCES adresse(id)
) ENGINE=InnoDB;