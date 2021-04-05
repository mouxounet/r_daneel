#!/usr/bin/env python3
# coding:utf8

"""
Programme : Bot discord pour démo ISI2020
Auteur : Rémi Sombrun
Date : 20/03/2021
Todo : Récupérer les events extérieurs
"""

import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import surveillance
import automate
import kubectl

# Variables


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

fichier_surveillance = "fichier_surveillance.txt"
fichier_logs = "log.txt"

salon_test = 822810525892476939
salon_alertes = 823184852429307966
salon_general = 822807737762316321

# Fonctions du robot


@bot.event
async def on_ready():
    """Le robot dit bonjour à la connexion"""
    mon_salon = bot.get_channel(salon_general)
    await mon_salon.send('Bonjour, je suis R. Daneel Olivaw, et je suis de retour en ligne')


@bot.command(name='bonjour', help='le robot dit bonjour')
async def bonjour(ctx, nom="Giskard"):
    """Fonction de Test"""
    await ctx.send(f'Bonjour {nom}, je suis Daneel pour te servir')


@bot.command(name='lois', help='Quelles sont les règles ?')
async def lois(ctx, *args):
    """Les trois lois de la robotique"""
    if not args:
        args = [1, 2, 3]
    les_lois = {
        0: "0) un robot ne peut pas faire de mal à l'humanité, ni, par son inaction, permettre que l'humanité soit blessée",
        1: "1) un robot ne peut blesser un être humain, ou par son inaction, permettre qu'un être humain soit blessé, sauf contradiction avec la loi 0",
        2: "2) un robot doit obéir aux ordres qui lui sont donnés par des êtres humains, sauf quand de tels ordres s'opposent à la Première loi",
        3: "3) un robot doit protéger sa propre existence aussi longtemps qu'une telle protection ne s'oppose pas à la première ou à la deuxième loi",
        4: "!) les Lois doivent être comprises entre 1 et 3"
    }
    for element in args:
        try :
            element = int(element)
        except:
            element = 4
        if element in range(5):
            await ctx.send(les_lois[element])


# Fonctions réservées aux admins


@bot.command(name='repos', help='arrête le robot', pass_context=True)
@commands.has_role("admin")
async def repos(ctx):
    """Fonction d'arrêt du script"""
    await ctx.send("Je vais me fermer pour maintenance, n'oublie pas de me relancer")
    await bot.logout()
    quit()

@bot.command(name="minikube", help='Les commandes kubectl')
@commands.has_role("admin")
async def minikube(ctx, *args):
    """Les commandes minikube"""
    retour = kubectl.ma_commande_minikube(*args)
    await ctx.send(retour)

# Fontions réservées aux dev


@bot.command(name='dev', help='[DEV] une commande pour les dev', pass_context=True)
@commands.has_role("dev")
async def dev(ctx):
    await ctx.send(f'Hey, tu as le droit de lancer la commande dev')


# Fonctions réservées aux ops


@bot.command(name="k", help='Les commandes kubectl')
@commands.has_role("ops")
async def k(ctx, *args):
    """Les commandes kubectl"""
    retour = kubectl.ma_commande_kubectl(*args)
    await ctx.send(retour)


# Gestion des erreurs


@bot.event
async def on_command_error(ctx, error):
    """Gestion des erreurs"""
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("Tu n'as pas le rôle nécessaire pour effectuer cette commande")


# Fonctions asynchrones


async def verif(salon, entree, sortie):
    """
    Fonction qui vérifie le contenu du fichier LOG
    """
    await bot.wait_until_ready()
    mon_salon = bot.get_channel(salon)
    while True:
        tableau = surveillance.verifie_logs(entree, sortie)
        if tableau:
            for message in tableau:
                await mon_salon.send(message)
        await asyncio.sleep(5)


# Programme


if __name__ == "__main__":
    bot.run(TOKEN)
    bot.loop.create_task(
        verif(salon_alertes, fichier_surveillance, fichier_logs))
