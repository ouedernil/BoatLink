#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Leila Ouederni"
__copyright__ = "HEIAFR 2017, Project BoatLink for HYDROcontest"
__credits__ = ["Leila Ouederni"]
__version__ = "1"
__email__ = "ouederni.l@gmail.com"
__status__ = "Prototype"

import sqlite3


class boatDatabase(object):
    def __init__(self):
        """
        Function: __init__
        --------------------------
        Construct a new boatDatabase object
        """
        self.database = '/home/renard/Desktop/virtualenv/venv/boatLinkDatabase/boatLinkDatabase.db'

    def openConnection(self):
        """
        Function: openConnection
        --------------------------
        Connect to the database
        """
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    def closeConnection(self):
        """
        Function: closeConnection
        --------------------------
        Disconnect from the database
        """
        self.conn.close()

    def insertDataEnvoiContinu(self, tension_batterie, tension_boost, courant_batterie, courant_max_moteur,
                               courant_moteur, capacite_totale_batterie, capacite_dispo_pourc, puissance_inst_moteur,
                               temps_course_possible, vitesse_bateau, heure, minute, seconde, erreur1, erreur2, erreur3,
                               erreur4,
                               erreur5, mode_man_course_end, mode_avant_stop_arr, emergency_stop, mode_stop_on, accel_x,
                               accel_y, accel_z):
        """
        Function: insertDataEnvoiContinu
        --------------------------
        Insert a row in the table envoiContinuT

        tension_batterie: tension batterie
        tension_boost: tension boost
        courant_batterie: courant batterie
        courant_max_moteur: courant max moteur
        courant_moteur: courant moteur
        capacite_totale_batterie: capacite totale de la batterie
        capacite_dispo_pourc: capacite disponible en pourcentage
        puissance_inst_moteur: puissance instantanee moteur
        temps_course_possible: temps de course encore possible
        vitesse_bateau: vitesse du bateau
        heure: heure
        minute: minute 
        seconde: seconde 
        erreur1: erreur 1
        erreur2: erreur 2
        erreur3: erreur 3
        erreur4: erreur 4
        erreur5: erreur 5
        mode_man_course_end: mode manuel course endurance
        mode_avant_stop_arr: mode avant stop arrière
        emergency_stop: emergency stop
        mode_stop_on: mode stop on
        accel_x: accelerometre x
        accel_y: accelerometre y
        accel_z: accelerometre z
        """
        self.openConnection()
        self.cursor.execute('''INSERT INTO envoiContinuT (tension_batterie, tension_boost, courant_batterie, courant_max_moteur,
            courant_moteur, capacite_totale_batterie, capacite_dispo_pourc, puissance_inst_moteur,
            temps_course_possible, vitesse_bateau, heure, minute, seconde, erreur1, erreur2, erreur3, erreur4,
            erreur5, mode_man_course_end, mode_avant_stop_arr, emergency_stop, mode_stop_on,accel_x, accel_y, accel_z)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', (
            tension_batterie, tension_boost, courant_batterie, courant_max_moteur,
            courant_moteur, capacite_totale_batterie, capacite_dispo_pourc, puissance_inst_moteur,
            temps_course_possible, vitesse_bateau, heure, minute, seconde, erreur1, erreur2, erreur3, erreur4,
            erreur5, mode_man_course_end, mode_avant_stop_arr, emergency_stop, mode_stop_on, accel_x, accel_y, accel_z
        ))
        self.conn.commit()

    def insertDataEnvoiInit(self,tension_batterie,tension_boost,courant_batterie,courant_max_moteur,courant_moteur, capacite_totale_batterie,capacite_dispo_batterie,capacite_dispo_pourc,puissance_inst_moteur,temps_course_possible, vitesse_bateau,distance_parc_le,distance_parc_lo,vitesse_min_calc_temps,heure,minute,seconde,jour,mois,annee,erreur1, erreur2,erreur3,erreur4,erreur5,mode_man_course_end,mode_avant_stop_arr,emergency_stop,mode_stop_on,pos_foil1,pos_foil2, pos_capt_moteur1,pos_capt_moteur2,accel_x,accel_y,accel_z,regul_P_gouv,regul_I_gouv,regul_P_foil1,regul_I_foil1, regul_P_foil2,regul_I_foil2,regul_P_courant_m,regul_I_courant_m):
        """
        Function: insertDataEnvoiInit
        --------------------------
        Insert a row in the table envoiContinuT

        tension_batterie: the short MAC address device
        tension_boost: tension boost
        courant_batterie: courant batterie
        courant_max_moteur: courant max moteur
        courant_moteur: courant moteur
        capacite_totale_batterie: capacite totale de la batterie
        capacite_dispo_batterie: capacite disponible de la batterie
        capacite_dispo_pourc: capacite disponible en pourcentage
        puissance_inst_moteur: puissance instantanee moteur
        temps_course_possible: temps de course encore possible
        vitesse_bateau: vitesse du bateau
        distance_parc_leger: distance parcours leger
        distance_parc_lourd: distance parcours lourd
        vitesse_min_calc_temps: vitesse minimum pour calcul de temps
        heure: heure
        minute: minute 
        seconde: seconde 
        jour: jour
        mois: mois
        annee: annee
        erreur1: erreur 1
        erreur2: erreur 2
        erreur3: erreur 3
        erreur4: erreur 4
        erreur5: erreur 5
        mode_man_course_end: mode manuel course endurance
        mode_avant_stop_arr: mode avant stop arrière
        emergency_stop: emergency stop
        mode_stop_on: mode stop on
        pos_foil1: position foil 1
        pos_foil2: position foil 2
        pos_capt_moteur1: position capteur moteur 1
        pos_capt_moteur2: position capteur moteur 2
        accel_x: accelerometre x
        accel_y: accelerometre y
        accel_z: accelerometre z
        regul_P_gouv: regulateur P gouvernail
        regul_I_gouv: regulateur I gouvernail
        regul_P_foil1: regulateur P foil 1
        regul_I_foil1: regulateur I foil 1
        regul_P_foil2: regulateur P foil 2
        regul_I_foil2: regulateur I foil 2
        regul_P_courant_m: regulateur P courant moteur
        regul_I_courant_m: regulateur I courant moteur
        """
        self.openConnection()
        self.cursor.execute('''INSERT INTO envoiInitT(tension_batterie,tension_boost,courant_batterie,courant_max_moteur,courant_moteur, capacite_totale_batterie,capacite_dispo_batterie,capacite_dispo_pourc,puissance_inst_moteur,temps_course_possible, vitesse_bateau,distance_parc_le,distance_parc_lo,vitesse_min_calc_temps,heure,minute,seconde,jour,mois,annee,erreur1, erreur2,erreur3,erreur4,erreur5,mode_man_course_end,mode_avant_stop_arr,emergency_stop,mode_stop_on,pos_foil1,pos_foil2, pos_capt_moteur1,pos_capt_moteur2,accel_x,accel_y,accel_z,regul_P_gouv,regul_I_gouv,regul_P_foil1,regul_I_foil1, regul_P_foil2,regul_I_foil2,regul_P_courant_m,regul_I_courant_m)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',(tension_batterie,tension_boost,courant_batterie,courant_max_moteur,courant_moteur, capacite_totale_batterie,capacite_dispo_batterie,capacite_dispo_pourc,puissance_inst_moteur,temps_course_possible, vitesse_bateau,distance_parc_le,distance_parc_lo,vitesse_min_calc_temps,heure,minute,seconde,jour,mois,annee,erreur1, erreur2,erreur3,erreur4,erreur5,mode_man_course_end,mode_avant_stop_arr,emergency_stop,mode_stop_on,pos_foil1,pos_foil2, pos_capt_moteur1,pos_capt_moteur2,accel_x,accel_y,accel_z,regul_P_gouv,regul_I_gouv,regul_P_foil1,regul_I_foil1, regul_P_foil2,regul_I_foil2,regul_P_courant_m,regul_I_courant_m))
        self.conn.commit()
        print("Set to database")

