#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
@file audioMetaEdite.py
@brief Module pour modifier les métadonnées des fichiers audio (MP3 / FLAC).

Fonctionnalités principales :
- Modifier titre, artiste, album, genre et date
- Sauvegarder les changements dans le fichier audio
- Gérer les fichiers MP3 via EasyID3 et les FLAC via mutagen.FLAC

Ce module est utilisé par le GUI et le CLI pour éditer les tags audio.

@author
@version 1.0
@date 
"""

import mimetypes
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, ID3NoHeaderError, APIC

class Editer:
    """
    Classe pour créer, afficher et modifier les métadonnées des fichiers audio MP3 et FLAC.
    """

    def creation_meta_donnees(self, titre: str, artiste: str, album: str, genre: str,
                              ladate: str, organisation: str) -> dict:
        """
        Crée un dictionnaire de métadonnées pour un fichier audio.
        """
        return {
            "title": titre,
            "artist": artiste,
            "album": album,
            "genre": genre,
            "date": ladate,
            "organization": organisation
        }

    def afficher_et_modifier_metadata(self, chemin_audio: str, chemin_image: str, titre: str,
                                      artiste: str, album: str, genre: str, ladate: str,
                                      organisation: str) -> None:
        """
        Détecte le format du fichier audio et modifie les métadonnées.
        """
        meta_donnees = self.creation_meta_donnees(titre, artiste, album, genre, ladate, organisation)

        if chemin_audio.endswith(".mp3"):
            if meta_donnees:
                self._afficher_et_modifier_meta_mp3(chemin_audio, meta_donnees)
            if chemin_image:
                self.modify_mp3_cover(chemin_audio, chemin_image)

        elif chemin_audio.endswith(".flac"):
            self._afficher_et_modifier_meta_flac(chemin_audio, meta_donnees, chemin_image)
        else:
            print("Format audio non pris en charge.")

    def _afficher_et_modifier_meta_mp3(self, chemin_audio: str, meta_donnees: dict) -> None:
        """Affiche et modifie les métadonnées d'un fichier MP3."""
        try:
            audio = MP3(chemin_audio, ID3=EasyID3)
        except ID3NoHeaderError:
            audio = MP3(chemin_audio)
            audio.add_tags()

        audio["title"] = meta_donnees["title"]
        audio["artist"] = meta_donnees["artist"]
        audio["album"] = meta_donnees["album"]
        audio["genre"] = meta_donnees["genre"]
        audio["date"] = meta_donnees["date"]
        audio["organization"] = meta_donnees["organization"]
        audio.save()
        print("\nNouvelles métadonnées MP3 mises à jour avec succès !\n")

    def modify_mp3_cover(self, chemin_audio: str, cover_image_path: str) -> None:
        """Modifie la couverture d'un fichier MP3."""
        audio_cover = MP3(chemin_audio, ID3=ID3)
        with open(cover_image_path, "rb") as cover_file:
            cover_data = cover_file.read()

        cover = APIC(
            encoding=3,
            mime=mimetypes.guess_type(cover_image_path)[0] or "image/jpeg",
            type=3,
            desc="Front cover",
            data=cover_data
        )
        audio_cover.tags.add(cover)
        audio_cover.save()

    def _afficher_et_modifier_meta_flac(self, chemin_audio: str, meta_donnees: dict, chemin_image: str) -> None:
        """Affiche et modifie les métadonnées d'un fichier FLAC."""
        audio = FLAC(chemin_audio)
        audio["title"] = meta_donnees["title"]
        audio["artist"] = meta_donnees["artist"]
        audio["album"] = meta_donnees["album"]
        audio["genre"] = meta_donnees["genre"]
        audio["date"] = meta_donnees["date"]
        audio["organization"] = meta_donnees["organization"]

        if chemin_image:
            with open(chemin_image, "rb") as img:
                picture = Picture()
                picture.data = img.read()
                picture.type = 3
                picture.mime = mimetypes.guess_type(chemin_image)[0] or "image/jpeg"
                audio.clear_pictures()
                audio.add_picture(picture)

        audio.save()
        print("\nNouvelles métadonnées FLAC mises à jour avec succès !\n")
