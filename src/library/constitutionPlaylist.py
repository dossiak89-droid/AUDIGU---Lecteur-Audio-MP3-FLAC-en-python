#!/usr/bin/python3
# -*- coding: UTF-8 -*-


"""
@file constitutionPlaylist.py
@brief Création et gestion des playlists XSPF.

Fonctionnalités principales :
- Création de fichiers XSPF par défaut ou avec nom personnalisé
- Ajout de pistes à la playlist
- Lecture de fichiers audio à partir de la playlist
- Compatibilité avec MP3 et FLAC
- Fonctionnalités GUI et CLI pour générer la playlist automatiquement

Utilisé par le GUI et le CLI pour gérer les playlists.

@author 
@version 1.0
@date 
"""

import os
import datetime
from lxml import etree
from library.explorationDossier import Explorer

class Playlist:
    """
    Classe pour créer et écrire des fichiers de playlists au format XSPF.
    """

    def __init__(self):
        """Initialisation des dossiers nécessaires pour les playlists et fichiers temporaires."""
        self.dossier = 'Playlist'
        os.makedirs("music", exist_ok=True)
        os.makedirs("Playlist", exist_ok=True)
        os.makedirs("FichierTemp", exist_ok=True)
        self.path_temp = os.path.abspath(os.path.join("FichierTemp", "TempFile.txt"))

    def creer_un_fichier_xspf(self) -> str:
        """Crée un fichier XSPF par défaut et retourne son chemin."""
        try:
            nom = os.path.join(self.dossier, 'maPlaylist.xspf')
            with open(nom, 'w', encoding='utf-8') as f:
                f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
                f.write("<playlist version=\"1\" xmlns=\"http://xspf.org/ns/0/\"></playlist>\n")
            return os.path.abspath(nom).replace("\\", "/")
        except OSError as e:
            print(f"Erreur lors de la création du fichier : {e}")
            return None

    def creer_fichier_xspf_nom(self, fichier_name: str) -> str:
        """Crée un fichier XSPF avec un nom spécifié et retourne son chemin."""
        try:
            fichier_name = f"{fichier_name}.xspf" if not fichier_name.endswith('.xspf') else fichier_name
            nom = os.path.join(self.dossier, fichier_name)
            with open(nom, 'w', encoding='utf-8') as f:
                f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
                f.write("<playlist version=\"1\" xmlns=\"http://xspf.org/ns/0/\"></playlist>\n")
            return os.path.abspath(nom).replace("\\", "/")
        except OSError as e:
            print(f"Erreur lors de la création du fichier spécifique : {e}")
            return None

    def ecriture_fichier_xspf(self, dossier_music: str, out_fichier_nom: str = None):
        """
        Écrit les informations d'une playlist dans un fichier XSPF.

        Paramètres:
            dossier_music : str : chemin du dossier contenant les fichiers musicaux
            out_fichier_nom : str : nom du fichier de sortie XSPF (optionnel)
        """
        try:
            chemin_file = self.creer_un_fichier_xspf() if out_fichier_nom is None else self.creer_fichier_xspf_nom(out_fichier_nom)
            if not chemin_file:
                return

            # Charger le fichier XSPF
            tree = etree.parse(chemin_file)
            root = tree.getroot()

            # Ajouter la date de création
            date_elem = etree.Element("date")
            date_elem.text = datetime.datetime.today().strftime('%d-%m-%y %H:%M:%S')
            root.append(date_elem)

            # Créer la liste de pistes
            tracklist = etree.Element("trackList")
            explorer = Explorer()
            # Explorer le dossier pour générer la liste des fichiers audio
            fichier_temp = explorer.explorer_dossier_interface(dossier_music)

            with open(fichier_temp, 'r', encoding='utf-8') as f:
                for ligne in f:
                    chemin_audio = os.path.abspath(ligne.strip()).replace("\\", "/")
                    track = etree.Element("track")
                    location = etree.Element("location")
                    location.text = f"file:///{chemin_audio}"
                    track.append(location)
                    tracklist.append(track)

            root.append(tracklist)

            with open(chemin_file, 'wb') as f:
                f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

            print(f"Playlist créée avec succès : {chemin_file}")

        except Exception as e:
            print(f"Erreur lors de la création de la playlist : {e}")
