#!/usr/bin/python3
# -*- coding: UTF-8 -*-


"""
@file explorationDossier.py
@brief Exploration des dossiers et extraction des fichiers audio.

Fonctionnalités principales :
- Parcours récursif des dossiers
- Filtrage des fichiers MP3 et FLAC
- Extraction des chemins absolus des fichiers audio
- Lecture des playlists XSPF et extraction des pistes
- Interface console ou GUI pour lister les fichiers

Utilisé par le CLI et le GUI pour gérer et préparer les fichiers audio.

@author 
@version 1.0
@date 
"""

import os
import mimetypes
import xml.etree.ElementTree as ET

class Explorer:
    """
    Classe pour explorer des dossiers, lister les fichiers audio et gérer les playlists temporaires.
    """

    def __init__(self):
        os.makedirs("music", exist_ok=True)
        os.makedirs("FichierTemp", exist_ok=True)
        self.fichier_temp = os.path.abspath("FichierTemp/TempFile.txt")
        self.chemin_python_project = os.getcwd()

    # -----------------------------
    # Exploration des dossiers
    # -----------------------------
    def _explorer_dossier_audio(self, chemin: str, fichier_sortie: str) -> str:
        """
        Parcourt un dossier et enregistre tous les fichiers audio (.mp3, .flac) dans un fichier temporaire.
        """
        try:
            with open(fichier_sortie, 'w', encoding='utf-8') as f:
                for racine, _, fichiers in os.walk(chemin):
                    for fichier in fichiers:
                        chemin_complet = os.path.join(racine, fichier).replace("\\", "/")
                        if fichier.endswith(".mp3") or fichier.endswith(".flac"):
                            type_mime, _ = mimetypes.guess_type(chemin_complet)
                            if type_mime in ['audio/mpeg', 'audio/x-flac', 'audio/flac']:
                                f.write(f"{chemin_complet}\n")
            return fichier_sortie
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier temporaire : {e}")
            return None

    def explorer_dossier_console(self, chemin_name: str) -> None:
        """
        Parcourt un dossier et affiche tous les fichiers audio trouvés dans la console.
        """
        chemin = os.getcwd() if chemin_name == "." else os.path.abspath(chemin_name)
        for racine, _, fichiers in os.walk(chemin):
            for fichier in fichiers:
                if fichier.endswith(".mp3") or fichier.endswith(".flac"):
                    type_mime, _ = mimetypes.guess_type(os.path.join(racine, fichier))
                    if type_mime in ['audio/mpeg', 'audio/x-flac', 'audio/flac']:
                        print(os.path.join(racine, fichier))

    def explorer_dossier_gui(self, chemin: str) -> str:
        """
        Parcourt un dossier et retourne le chemin vers le fichier temporaire contenant la liste des fichiers audio.
        """
        os.makedirs(os.path.join(self.chemin_python_project, "FichierTemp"), exist_ok=True)
        return self._explorer_dossier_audio(chemin, self.fichier_temp)

    def explorer_Playlist(self) -> list:
        """
        Retourne une liste de toutes les playlists (.xspf) dans le projet.
        """
        playlists = []
        for racine, _, fichiers in os.walk(os.getcwd()):
            for fichier in fichiers:
                if fichier.endswith(".xspf"):
                    playlists.append(os.path.join(racine, fichier))
        return playlists

    def extraire_pistes_de_playlist(self, chemin_complet: str) -> list:
        """
        Extrait les chemins des pistes d'une playlist XSPF.
        """
        try:
            tree = ET.parse(chemin_complet)
            root = tree.getroot()
            namespaces = {'xspf': 'http://xspf.org/ns/0/'}
            pistes = []
            for track in root.findall(".//xspf:trackList/xspf:track", namespaces):
                loc = track.find("xspf:location", namespaces)
                if loc is not None and loc.text:
                    chemin_abs = loc.text.strip()
                    if chemin_abs.startswith("file:///"):
                        chemin_abs = chemin_abs[8:]
                    if os.path.exists(chemin_abs):
                        pistes.append(chemin_abs)
            return pistes
        except Exception as e:
            print(f"Erreur extraction playlist {chemin_complet} : {e}")
            return []

    def explorer_dossier_interface(self, chemin: str) -> str:
        """
        Parcourt un dossier pour l’interface GUI et retourne le fichier temporaire contenant les chemins audio.
        """
        fichier_sortie = os.path.abspath("FichierTemp/TempFile.txt")
        return self._explorer_dossier_audio(chemin, fichier_sortie)
