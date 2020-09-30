-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Client :  localhost:8889
-- Généré le :  Ven 14 Avril 2017 à 18:49
-- Version du serveur :  5.6.35
-- Version de PHP :  7.1.1



--
-- Base de données :  `boatLinkDatabase`
--

-- --------------------------------------------------------

--
-- Structure de la table `envoiContinueT`
--

CREATE TABLE `envoiContinuT` (
  `id` INTEGER PRIMARY KEY,
  `tension_batterie` INTEGER NOT NULL,
  `tension_boost` INTEGER NOT NULL,
  `courant_batterie` INTEGER NOT NULL,
  `courant_max_moteur` INTEGER NOT NULL,
  `courant_moteur` INTEGER NOT NULL,
  `capacite_totale_batterie` INTEGER NOT NULL,
  `capacite_dispo_pourc` INTEGER NOT NULL,
  `puissance_inst_moteur` INTEGER NOT NULL,
  `temps_course_possible` INTEGER NOT NULL,
  `vitesse_bateau` INTEGER NOT NULL,
  `heure` INTEGER NOT NULL,
  `minute` INTEGER NOT NULL,
  `seconde` INTEGER NOT NULL,
  `mode_man_course_end` INTEGER NOT NULL,
  `mode_avant_stop_arr` INTEGER NOT NULL,
  `emergency_stop` INTEGER NOT NULL,
  `mode_stop_on` INTEGER NOT NULL,
  `erreur1` INTEGER NOT NULL,
  `erreur2` INTEGER NOT NULL,
  `erreur3` INTEGER NOT NULL,
  `erreur4` INTEGER NOT NULL,
  `erreur5` INTEGER NOT NULL,
  `accel_x` INTEGER NOT NULL,
  `accel_y` INTEGER NOT NULL,
  `accel_z` INTEGER NOT NULL
);

CREATE TABLE `envoiInitT` (
  `id` INTEGER PRIMARY KEY,
  `tension_batterie` INTEGER NOT NULL,
  `tension_boost` INTEGER NOT NULL,
  `courant_batterie` INTEGER NOT NULL,
  `courant_max_moteur` INTEGER NOT NULL,
  `courant_moteur` INTEGER NOT NULL,
  `capacite_totale_batterie` INTEGER NOT NULL,
  `capacite_dispo_batterie` INTEGER NOT NULL,
  `capacite_dispo_pourc` INTEGER NOT NULL,
  `puissance_inst_moteur` INTEGER NOT NULL,
  `temps_course_possible` INTEGER NOT NULL,
  `vitesse_bateau` INTEGER NOT NULL,
  `distance_parc_le` INTEGER NOT NULL,
  `distance_parc_lo` INTEGER NOT NULL,
  `vitesse_min_calc_temps` INTEGER NOT NULL,
  `heure` INTEGER NOT NULL,
  `minute` INTEGER NOT NULL,
  `seconde` INTEGER NOT NULL,
  `jour` INTEGER NOT NULL,
  `mois` INTEGER NOT NULL,
  `annee` INTEGER NOT NULL,
  `erreur1` INTEGER NOT NULL,
  `erreur2` INTEGER NOT NULL,
  `erreur3` INTEGER NOT NULL,
  `erreur4` INTEGER NOT NULL,
  `erreur5` INTEGER NOT NULL,
  `mode_man_course_end` INTEGER NOT NULL,
  `mode_avant_stop_arr` INTEGER NOT NULL,
  `emergency_stop` INTEGER NOT NULL,
  `mode_stop_on` INTEGER NOT NULL,
  `pos_foil1` INTEGER NOT NULL,
  `pos_foil2` INTEGER NOT NULL,
  `pos_capt_moteur1` INTEGER NOT NULL,
  `pos_capt_moteur2` INTEGER NOT NULL,
  `accel_x` INTEGER NOT NULL,
  `accel_y` INTEGER NOT NULL,
  `accel_z` INTEGER NOT NULL,
  `regul_P_gouv` INTEGER NOT NULL,
  `regul_I_gouv` INTEGER NOT NULL,
  `regul_P_foil1` INTEGER NOT NULL,
  `regul_I_foil1` INTEGER NOT NULL,
  `regul_P_foil2` INTEGER NOT NULL,
  `regul_I_foil2` INTEGER NOT NULL,
  `regul_P_courant_m` INTEGER NOT NULL,
  `regul_I_courant_m` INTEGER NOT NULL
);

CREATE TABLE `envoiDemandeT` (
  `id` INTEGER PRIMARY KEY,
  `no_param` INTEGER NOT NULL,
  `param` INTEGER NOT NULL
);

CREATE TABLE `adminT` (
  `pseudo` TEXT PRIMARY KEY,
  `password` TEXT NOT NULL
);

                        
