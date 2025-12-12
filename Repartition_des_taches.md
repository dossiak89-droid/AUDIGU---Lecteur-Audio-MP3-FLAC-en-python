# AUDIGU - Lecteur Audio MP3/FLAC en Python

Ce projet est un script Python permettant d'explorer des dossiers à la recherche de fichiers audio (MP3 et FLAC), d'en extraire les métadonnées (titre, artiste, album, etc.) et d'afficher la couverture (cover art) si elle est présente.  
Il est conçu pour analyser, organiser et visualiser des collections musicales, et peut être utilisé pour gérer efficacement une bibliothèque audio personnelle ou professionnelle.

---

## Sommaire

1. [Tâches effectuées par Dania HAMITOUCHE](#tâches-effectuées-par-dania-hamitouche)  
2. [Tâches effectuées par Siaka DOSSO](#tâches-effectuées-par-siaka-dosso)  
3. [Tâches effectuées par Mathéo OLEVIER](#tâches-effectuées-par-mathéo-olivier)  
4. [Tâches communes](#tâches-communes)  

---

## Tâches effectuées par Dania HAMITOUCHE
- **Développement du mode CLI (Command Line Interface)**  
  - Navigation dans les dossiers depuis la console.  
  - Commandes pour lire, mettre en pause et arrêter la lecture audio.  
- **Développement du module `lecture_playlist`**  
  - Gestion des playlists en console.  
  - Ajout, suppression et lecture séquentielle ou aléatoire des fichiers audio.  
- **Contrôles de lecture et gestion des playlists en console**  
  - Commandes `next`, `previous`, `repeat`.  
  - Gestion des erreurs pour fichiers audio manquants ou corrompus.

---

## Tâches effectuées par Siaka DOSSO
- **Développement complet de l’interface graphique (Tkinter)**  
  - Création des fenêtres principales et secondaires.  
  - Affichage des listes de lecture et des métadonnées.  
- **Intégration du mode sombre**  
  - Personnalisation des couleurs et thèmes pour un confort visuel.  
- **Développement des modules dans `library`**  
  - Extraction des métadonnées (titre, artiste, album, etc.).  
  - Gestion des playlists.  
  - Connexion et récupération via des APIs musicales (Jamendo, MusicBrainz).  

---

## Tâches effectuées par Mathéo OLEVIER
- **Extraction et édition des tags MP3/FLAC**  
  - Lecture et modification des informations des fichiers audio.  
  - Vérification de la cohérence des métadonnées.  
- **Intégration du drag and drop**  
  - Ajout de fichiers audio par glisser-déposer.  
  - Gestion des dossiers et fichiers multiples.  
- **Intégration des APIs Jamendo (musique) et LRCLIB (paroles)**  
  - Recherche et récupération automatique des musiques et paroles correspondantes.  
  - Affichage dans l’interface graphique pour une expérience complète.

---

## Tâches communes
- **Analyse des tâches à réaliser**  
  - Répartition et planification des fonctionnalités du projet.  
  - Identification des dépendances entre modules.  
- **Rédaction du rapport**  
  - Documentation détaillée du projet et des fonctionnalités.  
  - Explication des choix techniques et méthodologiques. 
- **Réalisation de la vidéo de démonstration**  
  - Présentation du fonctionnement complet de l’application.  
  - Démonstration des fonctionnalités principales et avancées.
- **Test global**  
  - Vérification de l’ensemble des fonctionnalités du projet.  
  - Identification et correction des bugs.  
  - Assurer la compatibilité entre les différents modules et la stabilité de l’application.
