-- Schéma MySQL simple pour les formulaires cas et virus

CREATE DATABASE IF NOT EXISTS virus_z;

USE virus_z;

-- Table simple pour le formulaire cas
CREATE TABLE IF NOT EXISTS cas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  prenom VARCHAR(100) NOT NULL,
  age INT,
  sexe VARCHAR(20),
  date_infection_estimee DATE,
  virus_contracte VARCHAR(150),
  mise_en_quarantaine BOOLEAN,
  quarantaine_zone VARCHAR(150),
  quarantaine_date_debut DATE,
  domicile_inconnu BOOLEAN,
  domicile_adresse VARCHAR(200),
  domicile_code_postal VARCHAR(20),
  domicile_ville VARCHAR(120),
  travail_inconnu BOOLEAN,
  travail_adresse VARCHAR(200),
  travail_code_postal VARCHAR(20),
  travail_ville VARCHAR(120)
);

-- Table simple pour le formulaire virus
CREATE TABLE IF NOT EXISTS virus (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(150) NOT NULL,
  variante VARCHAR(120),
  mode_propagation VARCHAR(50),
  incubation_min INT,
  incubation_max INT,
  contagiosite INT,
  moyens_detection JSON,
  commentaire TEXT
);
