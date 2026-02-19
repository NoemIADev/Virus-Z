USE virus_z;

-- ======================
-- VIRUS Z (Souche principale)
-- ======================

INSERT INTO virus
(nom, variante, mode_propagation, incubation_min, incubation_max, contagiosite, moyens_detection, commentaire)
VALUES

('Virus Z', 'ALPHA',
 'Morsure, griffure, fluides',
 6, 24, 1,
 'PCR, test antigénique, observation clinique',
 'Souche historique. Transformation rapide, agressivité modérée.'),

('Virus Z', 'RAGE',
 'Morsure, fluides, aérosols en milieu clos',
 2, 12, 2,
 'PCR, observation clinique',
 'Variant hyper-agressif : propagation rapide en milieu clos, attaques violentes et imprévisibles.'),

('Virus Z', 'YASS',
 'Morsure, griffure',
 12, 48, 1,
 'Observation clinique, test rapide',
 'Variant YASS : zombies plus lents et désorientés. Difficultés à s’orienter, se cognent facilement et suivent les sources lumineuses. Risque élevé en meute mais facilement bernables individuellement.');

-- ======================
-- NECROFLUX (Transmission environnementale)
-- ======================

INSERT INTO virus
(nom, variante, mode_propagation, incubation_min, incubation_max, contagiosite, moyens_detection, commentaire)
VALUES

('Nécroflux', 'SPORE',
 'Spores (air), contact surfaces',
 24, 96, 2,
 'PCR, prélèvement air, analyse environnementale',
 'Infection progressive via spores. Zones humides et confinées à haut risque.'),

('Nécroflux', 'BRUME',
 'Aérosols extérieurs (brouillard)',
 12, 72, 2,
 'PCR, capteurs particules atmosphériques',
 'Variant favorisé par l’humidité et le brouillard. Transmission facilitée en extérieur par conditions climatiques adaptées.');

-- ======================
-- VIRUS_ZH (Mutation évoluée du Virus Z)
-- Transmet Virus Z classique uniquement
-- ======================

INSERT INTO virus
(nom, variante, mode_propagation, incubation_min, incubation_max, contagiosite, moyens_detection, commentaire)
VALUES

('Virus_ZH', 'DELEGUE',
 'Morsure, fluides',
 12, 72, 1,
 'Analyse comportementale, séquençage ADN',
 'Mutation évoluée du Virus Z. Conserve une conscience avancée et tente de commander les autres zombies. La transmission engendre un Virus Z standard.'),

('Virus_ZH', 'DUCHESSE',
 'Morsure, fluides',
 18, 96, 1,
 'Analyse neurologique avancée',
 'Mutation rare du Virus Z. Conserve un contrôle quasi total et refuse de se soumettre aux pulsions primaires du virus. Transmission = Virus Z standard.'),

('Virus_ZH', 'DANIT',
 'Morsure, fluides',
 14, 72, 1,
 'Analyse comportementale avancée',
 'Mutation stable et calme du Virus Z. Devient fortement défensif si provoqué ou attaqué et tend à protéger les autres infectés proches. Transmission = Virus Z standard.');
