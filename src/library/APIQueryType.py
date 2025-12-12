#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
@file APIQueryType.py
@brief Enumération pour les types de requêtes possibles à l'API MusicBrainz.

Ce module définit les différents types de recherche utilisables par le Fetcher :
- ARTIST : recherche d'artistes
- ALBUM : recherche d'albums
- TRACK : recherche de titres

Ces types sont utilisés pour formater les requêtes vers l'API MusicBrainz.

@author
@version 1.0
@date 
"""

from enum import Enum

class APIQueryType(Enum):
    """
    Enumération des types de requêtes API possibles pour la recherche musicale.
    Utilisé dans la classe Fetcher pour indiquer le type de recherche MusicBrainz.
    """
    ARTIST = 'artist'   # Requête sur un artiste
    ALBUM = 'album'     # Requête sur un album
    TRACK = 'track'     # Requête sur une piste musicale
