
""" @file fetcher.py
 @brief Fournit une classe Fetcher permettant d’interroger Jamendo,
       MusicBrainz et CoverArtArchive pour récupérer des métadonnées
      musicales et des liens audio externes.
      """

import os
import requests
import unicodedata
from dotenv import load_dotenv

# Charger variables .env
load_dotenv()

class Fetcher:
    """
    @class Fetcher
    @brief Classe centralisant les appels API (Jamendo + MusicBrainz)
           et fournissant une interface unifiée de recherche musicale.

    La classe permet :
    - Recherche titre / album via Jamendo (avec audio MP3).
    - Recherche artiste via MusicBrainz (métadonnées + cover).
    - Chargement sécurisé du client_id Jamendo depuis .env.
    """
    def __init__(self):
        """
        @brief Constructeur : initialise l’objet Fetcher.
        
        - Charge JAMENDO_CLIENT_ID depuis .env pour sécuriser la clé.
        - Configure les URL des trois API :
            * Jamendo
            * MusicBrainz
            * CoverArtArchive
        - Initialise l'en-tête HTTP obligatoire pour MusicBrainz.
        """
        # Récupère client_id depuis .env
        client_id = os.getenv("JAMENDO_CLIENT_ID")

        if not client_id:
            raise ValueError(
                "⚠️ ERREUR : JAMENDO_CLIENT_ID est absent du fichier .env"
            )

        self.client_id = client_id

        # Jamendo
        self.jamendo_url = "https://api.jamendo.com/v3.0/tracks"

        # MusicBrainz
        self.mb_url = "https://musicbrainz.org/ws/2/"
        self.headers = {
            "User-Agent": "AudiguApp/1.0 (contact: dossiak89@gmail.com)"
        }

        # CoverArtArchive
        self.cover_url = "https://coverartarchive.org/release/"

    
    # JAMENDO → Recherche titre/album
    
    def _search_jamendo(self, query, limit):
        """
        @brief Recherche musicale via Jamendo selon un titre ou album.

        @param query Texte recherché (titre ou album)
        @param limit Nombre maximum de résultats

        @return Liste de dictionnaires contenant :
            - Titre, Artiste, Album
            - Genres, Moods, Instruments
            - Année, URL cover
            - Lien MP3 (Audio)
            - API = "Jamendo"
        
        Utilise l'endpoint : /v3.0/tracks
        """
        # Paramètres envoyés à Jamendo
        params = {
            "client_id": self.client_id,
            "format": "json",
            "limit": limit,
            "namesearch": query,
            "audioformat": "mp32",
            "include": "musicinfo+stats+licenses"
        }

        r = requests.get(self.jamendo_url, params=params)
        data = r.json()

        results = []
        for track in data.get("results", []):
            musicinfo = track.get("musicinfo", {})
            tags = musicinfo.get("tags", {})

            results.append({
                "Titre": track.get("name"),
                "Artiste": track.get("artist_name"),
                "Album": track.get("album_name"),
                "Cover": (
                    track.get("album_image_hires")
                    or track.get("album_image")
                    or track.get("image")
                ),
                "Genres": tags.get("genres", []),
                "Moods": tags.get("moods", []),
                "Instruments": tags.get("instruments", []),
                "Année": track.get("releasedate", ""),
                "Audio": track.get("audio"),
                "ID": track.get("id"),
                "API": "Jamendo"
            })
        return results

    
    # NORMALISATION (MusicBrainz)
    
    def _normalize(self, text):
        """
        @brief Normalise une chaîne de texte :
               - supprime les accents
               - convertit en minuscules

        @param text Chaîne à normaliser
        @return texte normalisé

        Utilisée pour améliorer la comparaison des artistes.
        """
        if not text:
            return ""
        text = unicodedata.normalize('NFD', text)
        return "".join(c for c in text if unicodedata.category(c) != 'Mn').lower()

    
    # MUSICBRAINZ → Recherche artiste
    
    def _search_artist_mb(self, artist_name, limit):
        """
        @brief Recherche d’enregistrements MusicBrainz selon un nom d’artiste.

        @param artist_name Nom de l’artiste recherché
        @param limit Nombre de résultats maximum

        @return Liste de métadonnées :
            - Titre
            - Artiste
            - Album
            - Genres (tags MB)
            - Année
            - Image (via CoverArtArchive)
            - Audio = None (car MusicBrainz n’héberge pas d’audio)
            - API = "MusicBrainz"
        """
        params = {
            "query": f'artist:"{artist_name}"',
            "fmt": "json",
            "limit": limit,
            "inc": "releases+tags+genres"
        }
        r = requests.get(self.mb_url + "recording", params=params, headers=self.headers)
        rec_data = r.json()
        recordings = []

        for rec in rec_data.get("recordings", []):
            if not rec.get("title"):
                continue

            if rec.get("artist-credit"):
                artist_name_clean = rec["artist-credit"][0].get("name")
            else:
                artist_name_clean = artist_name

            releases = rec.get("releases") or []
            if releases:
                album = releases[0].get("title", "Single")
                release_id = releases[0].get("id")

                cover = None
                try:
                    cover_r = requests.get(self.cover_url + release_id, timeout=3)
                    if cover_r.status_code == 200:
                        cover_json = cover_r.json()
                        images = cover_json.get("images")
                        if images:
                            cover = images[0]["thumbnails"].get("large")
                except:
                    cover = None

                year = releases[0].get("date", "")[:4]
            else:
                album = "Single"
                cover = None
                year = rec.get("first-release-date", "")[:4]

            tags = rec.get("tags", [])
            genres = [t["name"] for t in tags if t.get("name")]

            recordings.append({
                "Titre": rec.get("title"),
                "Artiste": artist_name_clean,
                "Album": album,
                "Cover": cover,
                "Genres": genres,
                "Moods": [],
                "Instruments": [],
                "Année": year,
                "Audio": None,
                "API": "MusicBrainz"
            })

        return recordings


    # Méthode unifiée

    def search_recordings(self, query, search_type="titre", limit=10):
        """
        @brief Point d’entrée unifié pour effectuer une recherche musicale.

        @param query Texte recherché
        @param search_type Type de recherche :
                - "titre"   → Jamendo
                - "album"   → Jamendo
                - "artiste" → MusicBrainz
        @param limit Nombre maximum de résultats
        
        @return Liste normalisée de résultats provenant
                soit de Jamendo, soit de MusicBrainz
        """
        if search_type in ("titre", "album"):
            return self._search_jamendo(query, limit)
        if search_type == "artiste":
            return self._search_artist_mb(query, limit)
        return []
