#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
Lecture des fichiers audio (MP3, FLAC) via Pygame et Pydub.
"""

import pygame
from pydub import AudioSegment
import os

class Ecouter:
    """
    Classe pour lire des fichiers audio (MP3, FLAC) via pygame.
    Compatible CLI.
    """
    def __init__(self):
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Erreur d'initialisation de pygame.mixer : {e}")
        self.current_file = None      # dernier fichier joué
        self.is_paused = False        # état de pause


    def lire_fichier_audio(self, chemin_fichier: str) -> None:
        """
        Charge et lit un fichier audio avec pygame (NON bloquant).
        """
        try:
            pygame.mixer.music.load(chemin_fichier)
            pygame.mixer.music.play()
            self.current_file = chemin_fichier  # on mémorise le fichier courant
            self.is_paused = False              # on n'est plus en pause
            print("Lecture démarrée.")
        except pygame.error as e:
            print(f"Erreur pygame: impossible de lire le fichier audio - {e}")
        except FileNotFoundError as e:
            print(f"Erreur: fichier introuvable - {e}")
        except Exception as e:
            print(f"Erreur inattendue : {e}")


    def lire_fichier_flac(self, chemin_fichier: str) -> None:
        """
        Lit un fichier FLAC en le convertissant temporairement en WAV (NON bloquant).
        """
        try:
            chemin_audio = os.path.abspath(os.path.join("music", chemin_fichier))
            if not os.path.isfile(chemin_audio):
                chemin_audio = chemin_fichier

            audio = AudioSegment.from_file(chemin_audio, format="flac")
            fichier_temp = "temp_audio.wav"
            audio.export(fichier_temp, format="wav")
            self.lire_fichier_audio(fichier_temp)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier FLAC : {e}")

    def lire_fichier_mp3(self, chemin_fichier: str) -> None:
        """
        Lit un fichier MP3 (NON bloquant).
        """
        try:
            chemin_audio = os.path.abspath(os.path.join("music", chemin_fichier))
            if not os.path.isfile(chemin_audio):
                chemin_audio = chemin_fichier
            self.lire_fichier_audio(chemin_audio)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier MP3 : {e}")

    def lire_tout_audio(self, chemin: str) -> None:
        """
        Détermine le type de fichier audio et le lit (NON bloquant).
        """
        try:
            if chemin.endswith('.mp3'):
                self.lire_fichier_mp3(chemin)
            elif chemin.endswith('.flac'):
                self.lire_fichier_flac(chemin)
            else:
                print("Format audio non supporté pour la lecture.")
        except Exception as e:
            print(f"Erreur lors de la tentative de lecture du fichier : {e}")

    def pause(self):
        """Met la musique en pause."""
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.is_paused = True
                print(" Lecture mise en pause.")
            else:
                print("Aucune lecture en cours à mettre en pause.")
        except Exception:
            print("Erreur : impossible de mettre en pause.")

    def resume(self):
        """
        Reprend la lecture :
        - si on était en pause -> reprend là où on s'est arrêté
        - sinon, si on avait fait stop -> relit le fichier depuis le début
        """
        try:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                print("  Lecture reprise.")
            else:
                # pas en pause : on relit depuis le début si on connaît le fichier
                if self.current_file:
                    print(" Relecture depuis le début.")
                    self.lire_fichier_audio(self.current_file)
                else:
                    print("Aucun fichier à reprendre.")
        except Exception:
            print("Erreur : impossible de reprendre.")

    def stop(self):
        """Arrête complètement la lecture."""
        try:
            pygame.mixer.music.stop()
            self.is_paused = False    # on n'est plus en pause
            # self.current_file reste mémorisé pour pouvoir relire avec resume()
            print(" Musique arrêtée.")
        except Exception:
            print("Erreur : impossible d'arrêter la musique.")
