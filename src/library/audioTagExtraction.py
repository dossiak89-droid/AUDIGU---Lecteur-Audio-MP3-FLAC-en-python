#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
@file audioTagExtraction.py
@brief Module pour extraire et afficher les métadonnées des fichiers audio.

Fonctionnalités principales :
- Lecture des tags ID3 pour MP3
- Lecture des métadonnées FLAC
- Affichage de titre, artiste, album, genre, date et durée
- Conversion automatique de la durée en minutes et secondes

Utilisé par le GUI et le CLI pour analyser les fichiers audio.
"""

import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC


class Extraction:
    """
    Classe pour extraire et afficher les métadonnées
    des fichiers audio MP3 et FLAC.
    """

    def convertir_seconds_en_minutes_secondes(self, duree) -> tuple[int, int]:
        """
        Convertit une durée en secondes en minutes et secondes.
        """
        minutes = int(duree // 60)
        secondes = int(duree % 60)
        return minutes, secondes

    def extraction_et_afficher_tag(self, file_aud: str) -> dict:
        """
        Extrait les métadonnées d'un fichier audio (MP3 ou FLAC)
        et les retourne sous forme de dictionnaire.
        Compatible avec le CLI et le GUI.
        """
        try:
            fichier_audio = os.path.abspath(os.path.join("music", file_aud))

            if not os.path.isfile(fichier_audio):
                return {"Erreur": f"Le fichier {file_aud} n'existe pas dans 'music'."}

            # Détection du format audio
            audio = None
            if fichier_audio.lower().endswith('.mp3'):
                audio = MP3(fichier_audio, ID3=EasyID3)
            elif fichier_audio.lower().endswith('.flac'):
                audio = FLAC(fichier_audio)

            if audio is None:
                return {"Erreur": "Le fichier n'est ni au format MP3 ni FLAC."}

            # Extraction des métadonnées principales
            metadata = {
                'Titre': audio.get('title', ['Titre inconnu'])[0],
                'Artiste': audio.get('artist', ['Artiste inconnu'])[0],
                'Album': audio.get('album', ['Album inconnu'])[0],
                'Genre': audio.get('genre', ['Genre inconnu'])[0],
                'Date': audio.get('date', ['Date inconnue'])[0],
                'Organisation': audio.get('organization', ['Organisation inconnue'])[0],
            }

            # Calcul de la durée
            minutes, secondes = self.convertir_seconds_en_minutes_secondes(audio.info.length)
            metadata['Durée'] = f"{minutes}:{int(secondes):02d}"

            return metadata

        except Exception as e:
            return {"Erreur": f"Une erreur s'est produite lors de l'extraction des tags : {e}"}

    def afficher_tags_console(self, file_aud: str) -> None:
        """
        Affiche proprement les métadonnées dans la console.
        """
        tags = self.extraction_et_afficher_tag(file_aud)
        print(f"\n{'-'*50}")
        print(f"Métadonnées pour : {file_aud}")
        print(f"{'-'*50}")
        for k, v in tags.items():
            print(f"{k}: {v}")
        print(f"{'-'*50}\n")
