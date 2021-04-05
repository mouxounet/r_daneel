#!/usr/bin/env python3
# coding:utf8

"""
Programme : Bot discord pour démo ISI2020 | Script de surveillance
Auteur : Rémi Sombrun
Date : 20/03/2021
Todo :
"""

import os

# Fonctions


def open_fic(fichier, mode):
    """Fonction qui ouvre le fichier"""
    try:
        entree = open(fichier, mode)
    except:
        print("Problème à l'ouverture du fichier")
    else:
        return entree


def verifie_logs(surveillance, ficlog):
    """ Regarde dans le fichier de surveillance, 
        -> renvoie un tableau avec les lignes du fichier.
        -> vide le fichier de surveillance
        -> copie les lignes dans le fichier log
    """
    entree = open_fic(surveillance, 'r+')
    sortie = open_fic(ficlog, 'a')
    tableau = []
    for ligne in entree.readlines():
        tableau.append(ligne.rstrip())
        sortie.write(ligne.rstrip())
        sortie.write("\n")
    entree.truncate(0)
    return tableau


if __name__ == "__main__":
    print(verifie_logs("fichier_surveillance.txt", "log.txt"))
