#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
CLI pour lecteur audio et gestion de playlists


Description générale:
- Permet d’extraire et d’afficher les métadonnées des fichiers audio (MP3/FLAC).
- Permet d’explorer un dossier pour générer et sauvegarder une playlist au format XSPF.
- Offre la possibilité de jouer directement un fichier audio local.
- Fournit une interface en ligne de commande simple avec différentes options.

Modules et classes principales:
   - `Extraction` : extraction des tags audio (titre, artiste, album, genre, date, durée)
   - `Explorer` : exploration de dossier et identification des fichiers audio
   - `Playlist` : génération d’une playlist XSPF à partir des fichiers explorés
   - `Ecouter` : lecture audio via `pygame`


"""

import argparse
import os
import datetime
import pygame
from library.audioTagExtraction import Extraction
from library.constitutionPlaylist import Playlist
from library.explorationDossier import Explorer
from library.ecouterAudio import Ecouter
from library.fetcher import Fetcher
from library.ecouterPlaylist import EcouterPlaylist





class Console:
    def __init__(self):
        self.extraction = Extraction()
        self.explorer = Explorer()
        self.playlist = Playlist()
        self.ecouter = Ecouter()
        self.fetcher = Fetcher()
        self.lecteur_playlist = EcouterPlaylist(self.explorer, self.ecouter)
        pygame.mixer.init()

    def afficher_aide(self):
        print("""
Usage: python cli.py [OPTIONS]

Options:
    -h, --help            Afficher cette aide
    -f, --file FILE       Afficher les métadonnées d'un fichier audio (MP3/FLAC)
    -d, --directory DIR   Explorer un dossier pour générer une playlist
    -o, --output FILE     Fichier XSPF de sortie pour la playlist (à utiliser avec -d)
    -p, --play FILE       Jouer directement un fichier audio
""")

    def main(self):
        parser = argparse.ArgumentParser(description="Gestionnaire audio CLI")
        parser.add_argument('-f', '--file', type=str, help='Fichier audio pour extraire les métadonnées')
        parser.add_argument('-d', '--directory', type=str, help='Dossier à explorer pour créer playlist')
        parser.add_argument('-o', '--output', type=str, help='Fichier XSPF de sortie pour la playlist')
        parser.add_argument('-p', '--play', type=str, help='Lire un fichier audio')
        parser.add_argument('--playlist', type=str, help='Lire une playlist XSPF')
        args = parser.parse_args()

        if not any(vars(args).values()):
            print("Aucun paramètre fourni. Tapez '-h' ou '--help' pour obtenir de l’aide.")
            return

        if args.file and args.directory:
            print("Erreur : utilisez uniquement '-f' ou '-d', pas les deux.")
            return

        # Extraction métadonnées
        if args.file:
            chemin_file = os.path.abspath(args.file)
            if not os.path.isfile(chemin_file):
                print(f"Erreur : le fichier '{chemin_file}' n’existe pas.")
                return
            print(f"Métadonnées locales pour : {chemin_file}")
            tags = self.extraction.extraction_et_afficher_tag(chemin_file)
            for k, v in tags.items():
                print(f"{k}: {v}")

        # Exploration dossier et playlist
        if args.directory:
            chemin_dir = os.path.abspath(args.directory)
            if not os.path.isdir(chemin_dir):
                print(f"Erreur : le dossier '{chemin_dir}' n’existe pas.")
                return
            print(f"Exploration du dossier : {chemin_dir}")
            self.explorer.explorer_dossier_console(chemin_dir)
            if args.output:
                out_file = os.path.abspath(args.output)
                print(f"Génération de la playlist : {out_file}")
                self.playlist.ecriture_fichier_xspf(chemin_dir, out_file)
                print("Playlist générée avec succès.")

       # Lecture audio        
        if args.play:
            chemin_play = os.path.abspath(args.play)
            if not os.path.isfile(chemin_play):
                print(f"Erreur : le fichier '{chemin_play}' n’existe pas.")
                return

            print(f"Lecture du fichier : {chemin_play}")
            self.ecouter.lire_tout_audio(chemin_play)

            print("\n--- Commandes disponibles ---")
            print("pause   -> mettre en pause la musique")
            print("resume  -> reprendre la musique est mise en pause relire si elle a été stopé ")
            print("stop    -> arrêter la musique")
            print("quit    -> quitter le lecteur")
            print("--------------------------------")

            while True:
                cmd = input("> ").strip().lower()

                if cmd == "pause":
                    self.ecouter.pause()
                elif cmd == "resume":
                    self.ecouter.resume()
                elif cmd == "stop":
                    self.ecouter.stop()
                elif cmd == "quit":
                    self.ecouter.stop()
                    break
                else:
                    print("Commandes valides : pause, resume, stop, quit")
       
        if args.playlist:

            ok = self.lecteur_playlist.charger_playlist(args.playlist)
            if not ok:
                return

            self.lecteur_playlist.jouer_courante()

            print("\n--- Commandes playlist ---")
            print("pause          -> mettre en pause")
            print("resume         -> reprendre")
            print("stop           -> arrêter la musique")
            print("next           -> piste suivante")
            print("prev           -> piste précédente")
            print("play N         -> jouer la piste numéro N (ex: play 3)")
            print("list           -> afficher la playlist")
            print("quit           -> quitter")
            print("---------------------------")

            while True:
                cmd = input("> ").strip().lower()

                if cmd == "pause":
                    self.ecouter.pause()
                elif cmd == "resume":
                    self.ecouter.resume()
                elif cmd == "stop":
                    self.ecouter.stop()
                elif cmd == "next":
                    self.lecteur_playlist.piste_suivante()
                elif cmd == "prev":
                    self.lecteur_playlist.piste_precedente()
                elif cmd.startswith("play "):
                    parts = cmd.split()
                    if len(parts) == 2 and parts[1].isdigit():
                        num = int(parts[1])
                        self.lecteur_playlist.jouer_numero(num)
                    else:
                        print("Utilisation : play N (ex: play 2)")
                elif cmd == "list":
                    self.lecteur_playlist.afficher_pistes()
                elif cmd == "quit":
                    self.ecouter.stop()
                    break
                else:
                    print("Commandes valides : pause, resume, stop, next, prev, play N, list, quit")

        

if __name__ == "__main__":
    console = Console()
    console.main()
