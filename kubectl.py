#!/usr/bin/env python3
# coding:utf8

"""
Programme : Bot discord pour démo ISI2020, partie kubectl
Auteur : Rémi Sombrun
Date : 20/03/2021
Todo : 
"""

import os

# fonctions
def ma_commande_kubectl(*args):
    """Passe une commande kubectl"""
    commande = "kubectl "+" ".join(args)
    sortie = os.popen(commande).read()
    return sortie

def ma_commande_minikube(*args):
    """Passe une commande minikube"""
    commande = "minikube "+" ".join(args)
    sortie = os.popen(commande).read()
    return sortie