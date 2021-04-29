#!/usr/bin/env python3
# coding:utf8

"""
Programme : Bot discord pour démo ISI2020
Auteurs : Sébastien Barbier, Rémi Sombrun
Date : 20/03/2021
"""

import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import kubectl

# Variables


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

salon_test = 822810525892476939
salon_alertes = 823184852429307966
salon_general = 822807737762316321

bleu = 0x496DDB
rouge = 0xC95D63
lavande = 0xAE8799
glauque = 0x717EC3
orange = 0xEE8434

# Fonctions pour un embed


def qui_lance_quoi(ctx):
    chaine = ctx.message.author.name + " a lancé la commande: " + ctx.message.content
    return chaine


def mon_embed(titre, contenu, couleur):
    embed = discord.Embed(title=titre, description=contenu, color=couleur)
    return embed


# Fonctions du robot


@bot.event
async def on_ready():
    """Le robot dit bonjour à la connexion"""
    mon_salon = bot.get_channel(salon_general)
    un_embed = mon_embed(
        "Bonjour", "je suis R. Daneel Olivaw, et je suis de retour en ligne", glauque)
    await mon_salon.send(embed=un_embed)


@bot.command(name='bonjour', help='le robot dit bonjour')
async def bonjour(ctx, nom="Giskard"):
    """Fonction de Test"""
    mon_salon = bot.get_channel(salon_general)
    un_embed = mon_embed(
        "Bonjour", "Bonjour "+nom+", je suis Daneel pour te servir", glauque)
    await mon_salon.send(embed=un_embed)


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
    contenu = ""
    for element in args:
        try:
            element = int(element)
        except:
            element = 4
        if element in range(5):
            contenu += les_lois[element]+"\n"
    un_embed = mon_embed("Les lois de la robotique", contenu, glauque)
    await ctx.send(embed=un_embed)

# Fonctions réservées aux admins


@bot.command(name='repos', help='arrête le robot', pass_context=True)
@commands.has_role("admin")
async def repos(ctx):
    """Fonction d'arrêt du script"""
    un_embed = mon_embed("Fonction d'arrêt du robot",
                         "Je vais me fermer pour maintenance, n'oublie pas de me relancer", orange)
    await ctx.send(embed=un_embed)
    await bot.logout()
    quit()


@bot.command(name="minikube", help='Les commandes minikube')
@commands.has_role("admin")
async def minikube(ctx, *args):
    """Les commandes minikube, commandes reservées aux admins"""
    retour = kubectl.ma_commande_minikube(*args)
    titre = qui_lance_quoi(ctx)
    if retour:
        contenu = retour
        couleur = lavande
    else:
        contenu = "erreur avec la commande"
        couleur = orange
    un_embed = mon_embed(titre, contenu, couleur)
    await ctx.send(embed=un_embed)

# Fontions réservées aux dev


@bot.command(name='dev', help='[DEV] une commande pour les dev', pass_context=True)
@commands.has_role("dev")
async def dev(ctx):
    await ctx.send(f'Hey, tu as le droit de lancer la commande dev')


# Fonctions réservées aux ops


@bot.command(name="k", help='Les commandes kubectl')
@commands.has_role("ops")
async def k(ctx, *args):
    """Les commandes kubectl, commande réservée aux ops"""
    retour = kubectl.ma_commande_kubectl(*args)
    titre = qui_lance_quoi(ctx)
    if retour:
        contenu = retour
        couleur = lavande
    else:
        contenu = "erreur avec la commande"
        couleur = orange
    un_embed = mon_embed(titre, contenu, couleur)
    await ctx.send(embed=un_embed)


@bot.command(name="apply", help='passer un yaml en PJ pour appliquer une configuration')
@commands.has_role("ops")
async def apply(ctx): 
    if ctx.message.attachments:
        for fic in ctx.message.attachments:
            fichier_cree = "fichiers_yaml/"+fic.filename
            await fic.save(fichier_cree)
            retour = kubectl.ma_commande_kubectl("apply -f ", fichier_cree)
            titre = qui_lance_quoi(ctx)
            titre += ", avec le fichier: "+fic.filename
            if retour:
                contenu = retour
                couleur = lavande
            else:
                contenu = "erreur avec la commande"
                couleur = orange
            un_embed = mon_embed(titre, contenu, couleur)
            await ctx.send(embed=un_embed)


# Gestion des erreurs


@bot.event
async def on_command_error(ctx, error):
    """Gestion des erreurs"""
    if isinstance(error, commands.errors.CheckFailure):
        titre = qui_lance_quoi(ctx)
        contenu = "Tu n'as pas le rôle nécessaire pour effectuer cette commande"
        un_embed = mon_embed(titre, contenu, rouge)
        await ctx.send(embed=un_embed)


# Programme


if __name__ == "__main__":
    bot.run(TOKEN)
