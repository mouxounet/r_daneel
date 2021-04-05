#!/usr/bin/env python3
# coding:utf8

"""
Programme : Bot discord pour démo ISI2020, partie kubectl
Auteur : Rémi Sombrun
Date : 20/03/2021
Todo : 
"""

# fonctions
def ma_commande_kubectl(*args):
    commande = "kubectl "+" ".join(args)
    return commande