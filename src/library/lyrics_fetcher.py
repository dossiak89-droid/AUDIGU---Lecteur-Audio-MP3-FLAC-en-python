#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
@file lyrics_fetcher.py
@brief Module pour récupérer les paroles avec LRCLIB API (sans cache)

Fonctionnalités :
- Recherche via LRCLIB API
- Pas de cache local
- Affichage complet des paroles

@version 2.2
"""

import requests


class LyricsFetcher:
    """
    Classe pour récupérer les paroles avec LRCLIB API (sans cache)
    """

    def __init__(self):
        """Initialise le fetcher"""
        # Configuration du timeout
        self.timeout = 10  # secondes

    def _fetch_from_lrclib(self, artist, title):
        """Récupère les paroles depuis LRCLIB API"""
        try:
            url = "https://lrclib.net/api/search"
            params = {
                'artist_name': artist,
                'track_name': title
            }

            print(f"🔍 Recherche sur LRCLIB : {artist} - {title}")
            response = requests.get(url, params=params, timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    # Prendre le premier résultat
                    first_result = data[0]
                    plain_lyrics = first_result.get('plainLyrics')
                    synced_lyrics = first_result.get('syncedLyrics')

                    # Préférer les paroles plain text
                    if plain_lyrics:
                        return plain_lyrics
                    elif synced_lyrics:
                        # Nettoyer les timestamps LRC [00:00.00]
                        lines = synced_lyrics.split('\n')
                        clean_lines = []
                        for line in lines:
                            if ']' in line:
                                clean_line = line.split(']', 1)[-1].strip()
                                if clean_line:
                                    clean_lines.append(clean_line)
                        return '\n'.join(clean_lines)

            return None

        except Exception as e:
            print(f"❌ Erreur LRCLIB : {e}")
            return None

    def get_lyrics(self, artist, title):
        """
        Récupère les paroles complètes

        Args:
            artist: Nom de l'artiste
            title: Titre de la chanson

        Returns:
            str: Paroles complètes de la chanson ou message d'erreur
        """
        # Nettoyer les entrées
        artist = artist.strip()
        title = title.strip()

        # Récupérer depuis l'API
        lyrics = self._fetch_from_lrclib(artist, title)

        if lyrics:
            print("✅ Paroles trouvées !")
            return lyrics
        else:
            error_msg = (
                "❌ Paroles non trouvées\n\n"
                f"Artiste : {artist}\n"
                f"Titre : {title}\n\n"
                "💡 Suggestions :\n"
                "• Vérifiez l'orthographe\n"
                "• Essayez avec le nom exact de l'artiste\n"
                "• Vérifiez votre connexion internet"
            )
            return error_msg


# Test
if __name__ == "__main__":
    fetcher = LyricsFetcher()

    # Test 1
    print("=" * 60)
    print("Test 1 : Adele - Hello")
    print("=" * 60)
    lyrics = fetcher.get_lyrics("Adele", "Hello")
    print(lyrics)
    print()

    # Test 2
    print("=" * 60)
    print("Test 2 : Ed Sheeran - Shape of You")
    print("=" * 60)
    lyrics = fetcher.get_lyrics("Ed Sheeran", "Shape of You")
    print(lyrics)
    print()

    # Test 3 : Chanson inexistante
    print("=" * 60)
    print("Test 3 : Chanson inexistante")
    print("=" * 60)
    lyrics = fetcher.get_lyrics("ArtisteFaux12345", "TitreInexistant98765")
    print(lyrics)