#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
@file ecouterPlaylist.py
@brief Lecture simple d'une playlist XSPF (version étudiante, POO).

Cette classe permet :
- de charger une playlist .xspf
- de mémoriser la liste des pistes
- de savoir quelle piste est en cours
- de jouer la piste courante, la suivante, la précédente

Elle s'appuie sur :
- Explorer : pour lire le fichier XSPF
- Ecouter  : pour jouer les fichiers audio
"""

import os
from library.explorationDossier import Explorer
from library.ecouterAudio import Ecouter


class EcouterPlaylist:
    """
    Classe simple pour gérer une playlist audio.
    """

    def __init__(self, explorer: Explorer, ecouter: Ecouter):
        """
        Constructeur.
        """
        self.explorer = explorer      # pour lire le .xspf
        self.ecouter = ecouter        # pour lire les fichiers audio
        self.pistes = []              # liste des chemins des fichiers audio
        self.index_courant = 0        # index (0, 1, 2, ...) de la piste en cours


    # Chargement de la playlist
    
    def charger_playlist(self, chemin_xspf: str) -> bool:
        """
        Charge une playlist XSPF et remplit la liste des pistes.

        param chemin_xspf: chemin vers le fichier .xspf
        return: True si succès, False sinon
        """
        chemin_xspf = os.path.abspath(chemin_xspf)

        if not os.path.isfile(chemin_xspf):
            print(f"Erreur : le fichier de playlist '{chemin_xspf}' n'existe pas.")
            return False

        # Utilisation d'Explorer pour extraire les pistes
        self.pistes = self.explorer.extraire_pistes_de_playlist(chemin_xspf)

        if not self.pistes:
            print("Aucune piste trouvée dans la playlist.")
            return False

        # On commence par la premiere piste
        self.index_courant = 0

        print(f"Playlist chargée : {len(self.pistes)} pistes.")
        self.afficher_pistes()
        return True

 
    # Affichage
   
    def afficher_pistes(self) -> None:
        """
        Affiche la liste des pistes avec une flèche sur la piste courante.
        """
        print("\n--- Playlist ---")
        for i, chemin in enumerate(self.pistes):
            nom = os.path.basename(chemin)
            if i == self.index_courant:
                print(f"-> {i + 1}. {nom}")
            else:
                print(f"   {i + 1}. {nom}")
        print("---------------\n")

    # Lecture
    
    def jouer_courante(self) -> None:
        """
        Joue la piste courante.
        """
        if not self.pistes:
            print("Aucune piste à jouer.")
            return

        chemin = self.pistes[self.index_courant]
        nom = os.path.basename(chemin)
        print(f"Lecture de : {self.index_courant + 1}. {nom}")
        self.ecouter.lire_tout_audio(chemin)

    def jouer_numero(self, numero: int) -> None:
        """
        Joue la piste numéro 'numero' (1, 2, 3, ...).

        param numero: numéro de piste (1-based)
        """
        if not self.pistes:
            print("Aucune piste chargée.")
            return

        index = numero - 1  # conversion en index de liste

        if index < 0 or index >= len(self.pistes):
            print("Numéro de piste invalide.")
            return

        self.index_courant = index
        self.jouer_courante()

    def piste_suivante(self) -> None:
        """
        Passe à la piste suivante et la joue.
        """
        if not self.pistes:
            print("Aucune piste chargée.")
            return

        if self.index_courant < len(self.pistes) - 1:
            self.index_courant += 1
            self.jouer_courante()
        else:
            print("Déjà sur la dernière piste.")

    def piste_precedente(self) -> None:
        """
        Passe à la piste précédente et la joue.
        """
        if not self.pistes:
            print("Aucune piste chargée.")
            return

        if self.index_courant > 0:
            self.index_courant -= 1
            self.jouer_courante()
        else:
            print("Déjà sur la première piste.")
