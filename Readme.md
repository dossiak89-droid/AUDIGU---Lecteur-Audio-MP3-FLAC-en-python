# AUDIGU - Lecteur Audio MP3/FLAC en python

## Membres du projet

| Nom       | Prénom    | Groupe |
|-----------|-----------|--------|
| DOSSO     | Siaka     | B3     |
| HAMITOUCHE| Dania     | B3     |
| OLEVIER   | Mathéo    | B3     |

---

## Description

Ce projet est un script Python permettant d'explorer des dossiers à la recherche de fichiers audio (MP3 et FLAC), d'en extraire les métadonnées (titre, artiste, album, etc.) et d'afficher la couverture (cover art) si elle est présente. C'est un outil utile pour analyser et organiser des fichiers audio, notamment dans des collections musicales ou des bibliothèques audio.

[Dépot github](https://github.com/dossiak89-droid/AUDIGU---Lecteur-Audio-MP3-FLAC-en-python)

## Sommaire

1. [Classes du projet](#classes-du-projet)
2. [Éditeur de Métadonnées Audio : Classe Editer()](#1-éditeur-de-métadonnées-audio--classe-editer)
3. [Extraction des Métadonnées Audio : Classe Extraction()](#2-extraction-des-métadonnées-audio--classe-extraction)
4. [Documentation : Chargement du client_id Jamendo](#3-documentation--chargement-du-client_id-jamendo)
5. [Gestion des Playlists en Python : Classe Playlist()](#4-gestion-des-playlists-en-python--classe-playlist)
6. [Lecteur Audio : Classe Ecouter()](#5-lecteur-audio--classe-ecouter)
7. [Lecteur Audio : Classe EcouterPlaylist()](#6-lecteur-audio--classe-ecouterplaylist)
8. [Explorateur de Fichiers Audio : Classe Explorer()](#7-explorateur-de-fichiers-audio--classe-explorer)
9. [Jamendo et MusicBrainz API Fetcher : Classe Fetcher()](#8-jamendo-et-musicbrainz-api-fetcher--classe-fetcher)
10. [Console : Classe Console()](#9-console--classe-console)
11. [Interface de gestion des fichiers audio : Classe AudioApp()](#10-interface-de-gestion-des-fichiers-audio--classe-audioapp)
12. [Conclusion](#conclusion)
13. [Prérequis](#prérequis)

---


## Classes du projet

## 1. Éditeur de Métadonnées Audio : Classe Editer()

Cette bibliothèque Python permet de créer, afficher, et modifier les métadonnées des fichiers audio au format **MP3** et **FLAC**. Elle offre également la possibilité d'ajouter ou de remplacer une image de couverture pour ces fichiers.

## 1.a Principales fonctionnalités

1. **Création de métadonnées** :
   - Génération d'un dictionnaire contenant des métadonnées comme le titre, l'artiste, l'album, etc.

2. **Modification des métadonnées** :
   - Ajout ou modification des métadonnées existantes dans les fichiers MP3 et FLAC.

3. **Gestion des images de couverture** :
   - Ajout ou remplacement de l'image de couverture des fichiers MP3 et FLAC.

4. **Affichage des métadonnées existantes** :
   - Lecture et affichage des métadonnées présentes dans les fichiers audio.

---

## 2. Extraction des Métadonnées Audio : Classe Extraction()

Cette classe Python permet d'extraire, d'afficher et de formater les métadonnées des fichiers audio au format **MP3** et **FLAC**. Elle gère également l'extraction des couvertures d'album.

## 2.1 Principales fonctionnalités

a. **Extraction des métadonnées** :
   - Titre, Artiste, Album, Genre, Date, Organisation.
   - Format MP3 et FLAC pris en charge.

b. **Durée audio** :
   - Conversion et affichage de la durée en minutes et secondes.

c. **Gestion des fichiers audio** :
   - Validation des chemins des fichiers audio.
   - Gestion des erreurs pour les fichiers manquants ou les formats non pris en charge.

---

## 3. Documentation : Chargement du `client_id` Jamendo

Cet identifiant est chargé automatiquement depuis le fichier .env lors de l’initialisation du Fetcher.Il permet d’effectuer des requêtes authentifiées auprès de Jamendo.

## 3.1 Fonctionnalité

- **Objectif** : Permettre à Jamendo de reconnaître l'application, de contrôler l’accès à l’API et d’autoriser l’utilisation des endpoints pour rechercher titres, albums, liens audio, métadonnées et images de cover.
- **Durée de validité** : Le `client_id` n’expire pas, reste valide tant que le compte développeur Jamendo est actif et, contrairement à un token OAuth, n’a pas besoin d’être régénéré régulièrement.

---

## 4. Gestion des Playlists en Python : Classe Playlist()

Ce projet Python fournit une classe `Playlist` pour créer et gérer des fichiers de playlists au format XSPF. Il offre des fonctionnalités permettant :

- De créer des fichiers de playlists par défaut ou personnalisés.
- D'ajouter des pistes à partir d'un dossier ou d'une sélection de fichiers.


Le script utilise des bibliothèques standard et tierces pour manipuler les fichiers XML et interagir avec le système de fichiers.

## 4.1 Principales fonctionnalités

a. **Créer un fichier par défaut** :
   - Crée un fichier `ma_playlist.xspf` dans le répertoire `Python/src/Playlist`.
   - Inclut une structure XML minimale.

b. **Créer un fichier spécifique** :
   - Permet de définir un nom personnalisé pour le fichier XSPF.
   - Le fichier est enregistré dans le répertoire 'Python/src/Playlist'.

c. **Ajouter des pistes à une playlist** :
   - Ajoute une liste de pistes provenant d'un dossier ou d'une sélection manuelle.
   - Les pistes sont ajoutées avec leurs emplacements respectifs au format `file:///`.

## 2.2 Manipulation de fichiers XML

- Utilise `lxml` pour créer et mettre à jour la structure XML des playlists.
- Ajoute des éléments comme`<date>` et `<trackList>` au fichier XSPF.

---

## 5. Lecteur Audio  : Classe Ecouter()

Cette classe Python permettant de lire divers formats de fichiers audio tels que **MP3**, **FLAC**, et **WAV**. Elle utilise la bibliothèque **Pygame** pour la lecture audio et **Pydub** pour la conversion des fichiers FLAC en WAV afin de les rendre compatibles avec Pygame.

## 5.1 Principales fonctionnalités  

a. **Lecture de fichiers MP3** :
   - Chargement et lecture directe des fichiers MP3.

b. **Lecture de fichiers FLAC** :
   - Conversion des fichiers FLAC en WAV temporaire pour permettre leur lecture.

c. **Lecture de fichiers WAV** :
   - Lecture directe des fichiers WAV.

d. **Contrôle de la lecture audio** :
   - pause() : met la lecture en pause.
   - resume() : reprend la lecture là où elle avait été mise en pause ou relance le fichier depuis le début si nécessaire.
   - stop() : arrête complètement la lecture audio.

e. **Gestion intelligente des fichiers audio** :
   - Identifie automatiquement le type de fichier audio basé sur son extension et appelle la méthode correspondante.

---
## 5. Lecteur Audio  : Classe EcouterPlaylist()

Cette classe permet de charger, afficher et lire une playlist audio au format XSPF.

## 6 Principales fonctionnalités  

a. **Chargement d’une playlist XSPF** :
   - Elle valide le fichier .xspf, extrait automatiquement les chemins audio grâce à Explorer, initialise la lecture sur la première piste et affiche l’ensemble des pistes trouvées..

b. **Lecture de la piste courante** :
   - Elle joue la piste courante en affichant son nom et son index dans la playlist.

c. **Lecture d’une piste spécifique** :
   - Elle permet de jouer une piste choisie par son numéro dans la playlist, en mettant à jour la piste courante.

d. **Navigation vers la piste suivante** :
   - Elle passe à la piste suivante et la joue, ou indique si la dernière piste est déjà atteinte.

e. **Navigation vers la piste précédente** :
   - Elle revient à la piste précédente et la joue, ou indique si la première piste est déjà atteinte.

---

## 7. Explorateur de Fichiers Audio : Classe Explorer()

Ce projet fournit une classe Python pour explorer des dossiers, identifier les fichiers audio au format **MP3**, **FLAC**, et gérer des playlists au format **XSPF**. Il offre des fonctionnalités permettant de lister les fichiers dans la console, de créer des fichiers de sortie avec les chemins audio et d'extraire les pistes des playlists.

## 7.1 Principales fonctionnalités  

a. **Exploration de dossiers audio** :
   - Identifie les fichiers MP3 et FLAC dans un répertoire donné.
   - Stocke les chemins des fichiers trouvés dans un fichier texte ou les affiche dans la console.

b. **Support des playlists XSPF** :
   - Recherche les fichiers de playlist **.xspf**.
   - Extrait les chemins des pistes des playlists.

c. **Gestion des fichiers temporaires** :
   - Génère des fichiers temporaires contenant les résultats d'exploration.

---

## 8. Jamendo et MusicBrainz API Fetcher : Classe Fetcher()

Ce script permet de récupérer des informations sur des titres, albums et artistes à partir des API Jamendo et MusicBrainz, en utilisant un client sécurisé pour Jamendo via un fichier .env. Le script interagit avec ces API pour effectuer des recherches musicales et renvoie les résultats sous forme de listes de dictionnaires contenant les métadonnées et, pour Jamendo, les liens audio. Il inclut également des fonctionnalités pour normaliser les textes et récupérer les couvertures via CoverArtArchive.
## 8.1 Principales fonctionnalités  

a. **Vérification de la connexion Internet**

   - Avant d’interroger Jamendo, le script charge le JAMENDO_CLIENT_ID depuis le fichier .env. Si la clé est absente, une erreur est levée pour prévenir l’utilisateur.

b. **Recherche de titres, artisteet albums via l'API Jamendo et MusicBrainz **

   - Le script permet de rechercher des titres et albums sur Jamendo. Les résultats incluent le titre, l’artiste, l’album, les genres, moods, instruments, l’année, la couverture et le lien audio MP3.
   - Le script permet de rechercher des artistes et leurs enregistrements via MusicBrainz. Les résultats incluent le titre, l’artiste, l’album, les genres, l’année et la couverture via CoverArtArchive. Aucun lien audio n’est fourni.

b. **Normalisation des textes**

   - Les chaînes de caractères sont normalisées en supprimant les accents et en les convertissant en minuscules pour faciliter la comparaison des noms d’artistes et des titres.

c. **Méthode unifiée de recherche**

   - search_recordings permet de rechercher titres, albums ou artistes en utilisant Jamendo ou MusicBrainz et renvoie une liste de résultats normalisés.
---

## 9. **Console** : Classe Console()

La classe `Console` sert d'interface utilisateur pour interagir avec le programme via la ligne de commande. Elle gère les options fournies par l'utilisateur et coordonne l'utilisation des autres classes :

- **`afficher_aide(self)`** : Affiche un message d'aide sur l'utilisation du programme.
- **`main(self)`** : Analyse les arguments de ligne de commande et appelle les méthodes appropriées des classes `Explorer`, `Extraction`, et `Playlist`.

## Importations

Le fichier `__init__.py` initialise le package `Python_project`. Il importe les classes suivantes pour un accès facile :

- **`Extraction`** : Importée depuis le module `audioTagExtraction`, elle permet d'extraire et d'afficher les métadonnées des fichiers audio.
- **`Playlist`** : Importée depuis le module `constitutionPlaylist`, elle gère la création et la modification des playlists au format XSPF.
- **`Explorer`** : Importée depuis le module `explorationDossier`, elle permet d'explorer les dossiers à la recherche de fichiers audio.

Les variables et constantes définies dans le fichier peuvent inclure la version du package, facilitant la gestion des mises à jour.

## Utilisation de la Console

Pour utiliser le script depuis la ligne de commande, assurez-vous d'abord d'être dans le dossier contenant le fichier `cli.py`. Ensuite, vous pouvez suivre les exemples ci-dessous :

- **Exécuter le script** :

    ```bash
    python3 cli.py
    ```

- **Afficher l'aide** :
  
    ```bash
    python3 cli.py -h
    ```

    ou

    ```bash
    python3 cli.py --help
    ```

- **Explorer le dossier courant** :
  
    ```bash
    python3 cli.py -d .
    ```

    ou

    ```bash
    python3 cli.py --directory .
    ```

- **Explorer un dossier spécifique** :
  
    ```bash
    python3 cli.py -d "chemin\vers\un\dossier"
    ```

    ou

    ```bash
    python3 cli.py --directory "chemin\vers\un\dossier"
    ```

- **Extraire les métadonnées d'un fichier audio dans le dossier music éxistant** :
  
    ```bash
    python3 cli.py -f music.mp3
    ```

    ou

    ```bash
    python3 cli.py --file music.mp3
    ```

- **Extraire les métadonnées d'un fichier audio en donnant un chemin spécifique** :
  
    ```bash
    python3 cli.py -f "chemin\vers\la\musique\music.mp3"
    ```

    ou

    ```bash
    python3 cli.py --file "chemin\vers\la\musique\music.mp3"
    ```

- **Générer une playlist à partir d'un dossier music éxistant et en spécifiant le nom de la playlist** :
  
    ```bash
    python3 cli.py -d ./music/ -o nom_de_votre_playlist.xspf
    ```

    ou
  
    ```bash
    python3 cli.py --directory ./music/ --output nom_de_votre_playlist.xspf
    ```

- **Générer une playlist à partir d'un dossier spécifique et en spécifiant le nom de la playlist** :
  
    ```bash
    python3 cli.py -d "chemin\vers\un\dossier" -o nom_de_votre_playlist.xspf
    ```

    ou

    ```bash
    python3 cli.py --directory "chemin\vers\un\dossier" --output nom_de_votre_playlist.xspf
    ```

- **Lancer l'interface graphique ** :
  
    ```bash
    python3 gui.py
    ```

- **Ecouter un fichier audio donné** :
  
    ```bash
    python3 cli.py -p music.mp3
    ```

    ou

    ```bash
    python3 cli.py --play music.mp3
    ```

- **Ecouter un playlist existant** :
  
    ```bash
    python3 cli.py --playlist "nom_de_votre_playlist.xspf"
   
---

## 10. **Interface de gestion des fichiers audio** : Classe AudioApp()

Ce projet est une interface graphique qui permet d'explorer des fichiers audio sur votre ordinateur, d'en extraire les métadonnées, d'afficher la couverture d'album (cover art), et de créer des playlists. Il est conçu pour être simple d'utilisation grâce à des boutons et des fenêtres interactives.

## Introduction

Cette application de gestion musicale vous permet de rechercher, lire, et organiser vos fichiers audio de manière efficace. Ce document explique les différentes fenêtres et boutons de l'interface utilisateur.
## 1. Choix du dossier à explorer

- **But** : Sélectionner un dossier contenant des fichiers audio (MP3 et FLAC) sur votre ordinateur pour les analyser.
- **Fonctionnement** : Un explorateur de fichiers s'ouvre pour naviguer et choisir le dossier. Les fichiers audio trouvés sont ensuite listés dans l'interface.
- **Code associé** : La méthode `explore_folder()` est utilisée pour parcourir le système de fichiers et charger les fichiers audio dans une Listbox.

## 2. Affichage des fichiers audio détectés

- **But** : Après avoir sélectionné un dossier, une liste de fichiers audio détectés (formats MP3 et FLAC) est affichée.
- **Fonctionnalité additionnelle** : L'utilisateur peut sélectionner un fichier audio pour afficher ses métadonnées.
- **Code associé** : La méthode `explore_folder()` peuple la Listbox avec les fichiers audio. La fonction `return_full_list()` extrait les informations du fichier sélectionné.

## 3. Extraction et affichage des métadonnées

- **But** : Afficher les métadonnées (titre, artiste, album, genre, etc.) des fichiers audio sélectionnés.
- **Fonctionnement** : Lorsqu'un fichier est cliqué dans la liste, ses métadonnées sont extraites et affichées dans l'interface.
- **Code associé** : La méthode `show_audio_details()` appelle `extract_metadata()` pour extraire les métadonnées du fichier audio sélectionné.

## 4. Affichage de la couverture (Cover Art)

- **But** : Afficher l'image de couverture d'un fichier audio s'il en contient une.
- **Fonctionnement** : Si une image de couverture est détectée dans le fichier audio, elle est affichée dans une zone dédiée. Sinon, une image par défaut est utilisée.
- **Code associé** : La méthode `cover_image()` gère l'extraction et l'affichage de la couverture d'album.

## 5. Fenêtre Principale

À l'ouverture de l'application, vous verrez la fenêtre principale qui contient plusieurs sections et boutons. Voici les boutons disponibles :

- **Jouer** :
  - Bouton pour lire l'audio **▶**
  - Cliquez sur ce bouton pour lire l'audio sélectionné.

- **Pause / Reprendre /suivant /paroles** :
  - Bouton pour faire pause l'audio **⏸**
  - Bouton pour reprendre la lecture l'audio **▶**
  - Bouton pour passer la lecture precedante l'audio **◀◀**
  - Bouton pour passer la lecture suivante l'audio **▶▶*
  - Boutton pour recherche les paroles liées a l'audio **🎤**
  - Utilisez ces boutons pour mettre en pause la lecture de l'audio ou reprendre la lecture après une pause.

- **Playlist** :
  - Bouton pour créer ou gérer vos playlists **Nouvelle Playlist**
  - Ce bouton ouvre une nouvelle fenêtre pour créer ou gérer vos playlists.

- **Exploration** :
  - Bouton pour parcourir un dossier et ses sous-dossiers.
  - Permet de parcourir un dossier et ses sous-dossiers pour sélectionner des fichiers audio.

- **Ecouter** :
  - Bouton pour écouter une playlist sélectionée **Ecouter**
  - Permet la lecture des fichiers audio dans une playlist sélectionée.
  
- **Next** :
  - Bouton pour l'audio suivant **▶▶**
  - Passe à l'audio suivant dans la liste.

- **Prev** :
  - Bouton pour l'audio précédent **◀◀**
  - Revient à l'audio précédent dans la liste.

- **Modifier Métadonnées (:::)** :
  - Bouton pour modifier les métadonnées **:::**
  - Ouvre une fenêtre pour modifier les métadonnées d'un fichier audio.
  
- **Rechercher** :
  - Bouton pour utilise une API **Recherche**
  - Utilisez ce bouton pour rechercher un artiste, un album,un titre en utilisant une API.
  - Entrez votre recherche dans le champ de saisie (Entry).

### Fonctionnalité de Recherche de Musique

L'application utilise deux API  pour effectuer des recherches de musique. Voici comment cela fonctionne :

#### 1. Chosise d'abord par titre, artiste ou album

#### 2. Saisie de la Recherche

L'utilisateur entre une commande dans le champ de recherche. Les commandes acceptées incluent :

- **artiste** : `artiste: Nom de l'artiste`
	ou
- **album** : `album: Nom de l'album`
	ou
- **titre** : `titre: Nom de la musique`

Ces commandes permettent à l'utilisateur de spécifier exactement ce qu'il recherche, facilitant ainsi l'accès aux résultats souhaités.

#### 2. Envoi de la Requête

Lorsque l'utilisateur clique sur le bouton **Recherche**, l'application envoie une requête à l'API avec les paramètres spécifiés. Cette requête est généralement formulée en utilisant une méthode HTTP (comme GET ou POST) pour récupérer des données. Cela permet à l'application d'interroger efficacement l'API et de récupérer des informations pertinentes sur la musique.

#### 3. Réception des Résultats

L'API renvoie les résultats de la recherche sous forme de données structurées, en format JSON. L'application traite ces données pour extraire les informations pertinentes, telles que les titres des morceaux, les noms des artistes et les albums associés.

#### 4. Affichage des Résultats

Les résultats de la recherche (artistes, albums, titre) sont ensuite affichés dans l'interface utilisateur.

## 5. Fenêtre de Playlist

En cliquant sur le bouton **Nouvelle Playlist**, une nouvelle fenêtre s'ouvrira avec les options suivantes :

- **Annuler** :
  - Bouton pour annuler toutes les opérations **Annuler**
  - Annule toutes les opérations en cours et ferme la fenêtre de playlist sans sauvegarder les modifications.

- **Créer Playlist** :
  - Bouton pour créer la playlist par défaut **par défaut**
  - Crée la playlist par défaut qui contient une liste d'audio préétablie dans la Listbox affichée sur l'interface. Cette playlist peut être utilisée pour une lecture rapide sans nécessiter de configuration supplémentaire.

## 6. Fenêtre de Modification des Métadonnées

En cliquant sur le bouton **Modifier Métadonnées (:::)**, une nouvelle fenêtre apparaîtra, permettant à l'utilisateur de modifier les informations d'un fichier audio et changer la cover. Cette fenêtre est équipée de plusieurs champs et boutons pour faciliter la gestion des métadonnées.

### Labels et Zones de Saisie

La fenêtre de modification contient les champs suivants, chacun associé à un label explicite :

- **Titre** : Champ pour saisir ou modifier le titre de la piste audio.
- **Artiste** : Champ pour saisir ou modifier le nom de l'artiste.
- **Album** : Champ pour saisir ou modifier le nom de l'album.
- **Genre** : Champ pour saisir ou modifier le genre musical.
- **Année** : Champ pour saisir ou modifier la date de sortie.
- **Commentaire** : Champ pour saisir ou modifier le commentaire.

Chaque champ contient par défaut les valeurs actuelles des métadonnées, facilitant ainsi la modification. Cela permet à l'utilisateur de garder les informations existantes tout en offrant la possibilité de les mettre à jour rapidement.

### Bouton Changer la cover

Ce bouton ouvre un explorateur de fichiers pour choisir une nouvelle image de couverture pour l'audio. La couverture sélectionnée sera associée au fichier audio et affichée dans l'interface.

### Boutons d'Action

- **Annuler** :
  - Bouton pour annuler toutes les opérations **Annuler**
  - Ferme la fenêtre sans effectuer d'opérations sur les métadonnées.

- **Sélectionner une cover** :
  - Bouton pour sélectionner une couverture **Sélectionner une couverture**
  - Ouvre un explorateur de fichiers pour choisir une image de couverture pour l'audio.

- **Enregistrer** :
  - Bouton pour sauvegarde les métadonnées **Enregistrer**
  - Sauvegarde les métadonnées saisies dans les champs de texte et la couverture si elle a été modifiée.

## 7. Contrôle de lecture (Play/Pause/Next/Previous/Paroles)

- **But** : Contrôler la lecture des fichiers audio depuis l'interface.
- **Fonctionnalité** :
  - **Play/Pause** : Lire ou mettre en pause la chanson sélectionnée.
  - **Next/Prev** : Passer à la piste suivante ou précédente.
- **Code associé** :
  - `play_audio()` pour la lecture.
  - `pause_audio()` pour basculer entre pause et lecture.
  - `next_audio()` et `prev_audio()` pour changer de piste.
  - `show_lyrics_popup`  pour rechercher les paroles. 

## 8. Navigation et interaction améliorée

- **But** : Permettre une navigation fluide entre les fichiers audio.
- **Fonctionnement** :Lorsqu'une nouvelle piste est sélectionnée, les informations affichées (métadonnées et cover) sont mises à jour, et les boutons "suivant" et "précédent" permettent de naviguer rapidement dans la liste des fichiers audio.
- **Code associé** : Les méthodes next_audio() et prev_audio() gèrent les changements de sélection dans la Listbox et la lecture automatique de la piste correspondante.

## Utilisation Générale

- **Lancer une recherche** :
  - Saisissez un texte dans le champ de recherche en haut de l'interface et cliquez sur le bouton "Rechercher".
  - Les résultats locaux et ceux provenant de l’API sont affichés dans la Listbox principale ou dans une fenêtre popup pour les résultats API.
  

- **Lire de la musique** :
  - Sélectionnez un morceau dans la liste et cliquez sur "Jouer" pour commencer la lecture.
  - Utilisez "Pause" pour mettre la musique en pause et "Reprendre" pour continuer la lecture.
  - Les boutons ◀◀ et ▶▶ permettent de passer à l’audio précédent ou suivant.

- **Gérer les playlists** :
  - Cliquez sur le bouton "Playlist" pour ouvrir la fenêtre de gestion des playlists.
  - Vous pouvez créer une playlist personnalisée avec cases à cocher pour sélectionner les fichiers audio.
  - Le bouton Annuler ferme la fenêtre sans sauvegarder les modifications.

- **Modifier les métadonnées** :
  - Cliquez sur "Modifier Méta" pour ouvrir la fenêtre de modification.
  - Vous pouvez modifier le Titre, l’Artiste, l’Album, le Genre, l’Année et le Commentaire, et changer la couverture (cover) si nécessaire.
  - Les boutons Enregistrer permettent de sauvegarder les modifications.
## Conclusion

Cette application fournit une interface intuitive pour explorer, lire, rechercher et organiser vos fichiers audio. Elle permet de gérer les métadonnées, d’afficher la cover, de créer et lire des playlists, tout en intégrant une navigation fluide et un accès aux résultats d’API musicales.

## Prérequis

Avant d'exécuter ce script, vous devez installer les bibliothèques suivantes :

- [mutagen](https://mutagen.readthedocs.io/en/latest/installation.html) : Bibliothèque utilisée pour extraire les métadonnées des fichiers MP3 et FLAC.
- [Pillow](https://python-pillow.org/) : Bibliothèque Python pour manipuler et afficher des images.
- [Pygame](https://www.pygame.org/) : Bibliothèque pour créer des jeux en Python et jouer des fichiers audio.
- [Pydub](https://github.com/jiaaro/pydub) : Bibliothèque pour manipuler les fichiers audio.
- [lxml](https://lxml.de/) : Bibliothèque pour le traitement des documents XML et HTML.
- [requests](https://docs.python-requests.org/en/latest/): Bibliothèque pour envoyer des requêtes HTTP en Python..

Pour installer les dépendances, exécutez la commande suivante dans votre terminal :

```bash
pip install mutagen 
pip install Pillow 
pip install pygame
pip install pydub
pip install lxml
pip install requests
