#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
AudioApp audio complète avec lecture, gestion de métadonnées et playlists.

    AudioApp est une application qui permet :
        - La lecture de fichiers audio MP3 et FLAC via pygame.
        - L'affichage et la modification des métadonnées (titre, artiste, album, genre, année, commentaire, cover).
        - L'affichage de la couverture associée à la musique.
        - La création et l'ouverture de playlists au format XSPF.
        - La recherche locale dans les fichiers audio et la recherche via API externe (Fetcher).
        - La navigation audio (précédent/suivant) et contrôle lecture/pause.
lecture audio, métadonnées, playlists, recherche locale et API.
"""



import os   # Gestion des fichiers et chemins
import io   # Gestion des flux d'entrée/sortie
import tkinter as tk  # Interface graphique
from tkinter import filedialog, messagebox, Toplevel, Scrollbar  # Boîtes de dialogue et widgets GUI
from tkinterdnd2 import DND_FILES,TkinterDnD  # Support du glisser-déposer de fichiers
import mimetypes  # Détection du type de fichier
from PIL import Image, ImageTk # Manipulation et affichage d’images
import pygame # Lecture de sons et musiques
from mutagen.mp3 import MP3  # Gestion des métadonnées MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TDRC, COMM, APIC # Balises ID3 (titre, artiste, album, etc.)
from mutagen.flac import FLAC, Picture # Métadonnées et images pour fichiers FLAC
from library.lyrics_fetcher import LyricsFetcher
import requests
import re


# Import direct depuis library
try:
    from library.fetcher import Fetcher

except ModuleNotFoundError as e:
    messagebox.showerror("Erreur import", f"Impossible d'importer library.fetcher : {e}")
    raise

#  Styles utilitaires
def style_button(self, btn, bg_color="#3498DB", fg_color="white"):
    btn.configure(bg=bg_color, fg=fg_color, activebackground="#2980B9",
                  relief=tk.FLAT, bd=0, padx=8, pady=5, font=("Segoe UI", 10, "bold"))
    btn.bind("<Enter>", lambda e: btn.configure(bg="#2980B9"))
    btn.bind("<Leave>", lambda e: btn.configure(bg=bg_color))
    if btn not in self.all_buttons:
        self.all_buttons.append(btn)


def style_listbox(listbox):
    listbox.configure(bg="#FFFFFF", fg="#333333", font=("Segoe UI", 12), selectbackground="#3498DB", selectforeground="white", activestyle="none")

#  Application 
class AudioApp:
    def __init__(self, master):
        """
    Initialise l'application AUDIGU avec son interface, ses états audio, et ses configurations (polices, couleurs, chemins, icônes). 
    Prépare la fenêtre Tkinter principale, le lecteur audio, et les composants de l'interface utilisateur.
    """
        self.master = master
        self.master.title("AUDIGU")
        pygame.mixer.init()
        
        #  --- POLICES pour panel2 ---
        self.FONT_PANEL2_SMALL = ("Segoe UI", 13)
        self.FONT_PANEL2_MEDIUM = ("Segoe UI", 10, "bold")
        self.FONT_PANEL2_LARGE = ("Segoe UI", 16, "bold")
        
        # États / données
        self.max_length = 78
        self.max_length_milieu = 38
        self.audio_list = []           # noms affichés
        self.audio_paths = {}          # { "0": "/abs/path/file.mp3", ... }
        self.filtered_audio_list = []
        self.current_index = 0
        self.is_paused = False
        self.audio_playing = False
        self.fetcher = Fetcher()
        self.lyrics_fetcher = LyricsFetcher()
        self.current_playlist = []
        self.dark_mode = False # Mode sombre activé ou non

        self.current_lyrics = ""
        self.current_artist = ""
        self.current_title = ""

        #  Couleurs 
        self.light_colors = {
            "bg": "#F5F5F5",
            "fg": "#333333",
            "button_bg": "#3498DB",
            "button_fg": "white",
            "select_bg": "#3498DB",
            "select_fg": "white",
            "entry_bg": "white"
        }
        self.dark_colors = {
            "bg": "#2E0249",
            "fg": "white",
            "button_bg": "#8E44AD",
            "button_fg": "white",
            "select_bg": "#9D00FF",
            "select_fg": "white",
            "entry_bg": "#5D275D"
        }

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.chem_im = os.path.abspath(os.path.join(base_dir, "img", "nn.webp"))
        self.image_path_default = os.path.abspath(os.path.join(base_dir, "img", "images.jpeg"))
        self.default_music_dir = os.path.abspath(os.path.join(base_dir, "music"))

        self.api_music_dir = os.path.join(base_dir, "music_api")
        os.makedirs(self.api_music_dir, exist_ok=True)
        self.icons = {}
        self.load_icons()
        self.all_buttons = []
        self.build_interface_structure()
       

    #  icônes 
    def load_icons(self):
        icon_files = {
            "play":"icons/play.png",
            "pause":"icons/pause.png",
            "next":"icons/next.png",
            "explorer":"icons/folder.png",
            "new_playlist":"icons/new_playlist.png",
            "open_playlist":"icons/open_playlist.png",
            "play_playlist":"icons/play_playlist.png",
            "dark_mode":"icons/dark_mode.png"
        }
        for key, path in icon_files.items():
            if os.path.exists(path):
                try:
                    img = Image.open(path).resize((24,24))
                    self.icons[key] = ImageTk.PhotoImage(img)
                except:
                    self.icons[key] = None
            else:
                self.icons[key] = None
    # --- Style boutons & listbox 
    def style_button(self, btn, bg_color="#3498DB", fg_color="white"):
        btn.configure(bg=bg_color, fg=fg_color, activebackground="#2980B9",
                      relief=tk.FLAT, bd=0, padx=8, pady=5, font=("Segoe UI", 10, "bold"))
        btn.bind("<Enter>", lambda e: btn.configure(bg="#2980B9"))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg_color))
        if btn not in self.all_buttons:
            self.all_buttons.append(btn)


    def style_listbox(self, listbox):
        listbox.configure(bg="#FFFFFF", fg="#333333", font=("Segoe UI", 12),
                          selectbackground="#3498DB", selectforeground="white", activestyle="none")

    def show_lyrics_popup(self):
        """Affiche les paroles dans une fenêtre popup"""
        if not self.current_artist or not self.current_title:
            messagebox.showwarning("Paroles", "Aucune musique sélectionnée.")
            return

        cleaned_artist = self.current_artist.split(';')[0].strip()
        cleaned_artist = cleaned_artist.split('&')[0].strip()
        cleaned_artist = cleaned_artist.split(' feat.')[0].strip()
        cleaned_artist = cleaned_artist.split(' ft.')[0].strip()

        cleaned_title = re.sub(r'\s*[\(\[].*?[\)\]]', '', self.current_title).strip()

        popup = Toplevel(self.master)
        popup.title(f"Paroles - {self.current_title}")
        popup.geometry("600x500")

        # Frame pour le titre
        title_frame = tk.Frame(popup, bg="#3498DB", pady=10)
        title_frame.pack(fill=tk.X)

        tk.Label(
            title_frame,
            text=f"{self.current_artist} - {self.current_title}",
            font=("Segoe UI", 14, "bold"),
            bg="#3498DB",
            fg="white"
        ).pack()

        # Zone de texte avec scrollbar
        text_frame = tk.Frame(popup)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        lyrics_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            yscrollcommand=scrollbar.set,
            bg="white",
            fg="#333333",
            padx=10,
            pady=10
        )
        lyrics_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=lyrics_text.yview)

        # Afficher message de chargement
        lyrics_text.insert("1.0", "🔄 Recherche des paroles en cours...")
        lyrics_text.config(state=tk.DISABLED)
        popup.update()

        # Récupérer les paroles
        lyrics = self.lyrics_fetcher.get_lyrics(cleaned_artist, cleaned_title)

        # Afficher les paroles
        lyrics_text.config(state=tk.NORMAL)
        lyrics_text.delete("1.0", tk.END)
        lyrics_text.insert("1.0", lyrics)
        lyrics_text.config(state=tk.DISABLED)

        # Bouton fermer
        tk.Button(
            popup,
            text="Fermer",
            command=popup.destroy,
            bg="#E74C3C",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=5
        ).pack(pady=10)

    #  structure GUI 
    def build_interface_structure(self):
        #  Panel 1 : écran d’accueil  
        self.panel1 = tk.Frame(self.master, bg="#2E0249")
        self.panel1.pack(fill="both", expand=True)

        # Logo principal
        title_label = tk.Label(
            self.panel1,
            text="🎵 AUDIOGU 🎵",
            font=("Segoe UI", 32, "bold"),
            fg="white",
            bg="#2E0249"
        )
        title_label.pack(pady=100)

        # Texte "Chargement..." animé
        loading_label = tk.Label(
            self.panel1,
            text="Chargement",
            font=("Segoe UI", 14),
            fg="#E0AAFF",
            bg="#2E0249"
        )
        loading_label.pack(pady=10)

        def animate_dots():
            current = loading_label.cget("text")
            if current.endswith("..."):
                loading_label.config(text="Chargement")
            else:
                loading_label.config(text=current + ".")
            self.master.after(500, animate_dots)

        animate_dots()

        # Bouton Démarrer stylé
        start_button = tk.Button(
            self.panel1,
            text="Démarrer",
            command=self.direct_Goto,
            font=("Segoe UI", 12, "bold"),
            bg="#7A0BC0",
            fg="white",
            activebackground="#9D00FF",
            relief=tk.FLAT,
            padx=20,
            pady=10,
        )
        start_button.pack(pady=40)

        # Hover effet
        start_button.bind("<Enter>", lambda e: start_button.config(bg="#9D00FF"))
        start_button.bind("<Leave>", lambda e: start_button.config(bg="#7A0BC0"))

        #  Panel 2 : interface principale 
        self.panel2 = tk.Frame(self.master, bg="#F5F5F5")

        # Frames haut / centre / bas
        self.frame1_haut = tk.Frame(self.panel2, bg="#F5F5F5")
        self.frame2_centre = tk.Frame(self.panel2, bg="#F5F5F5")
        self.frame3_bas = tk.Frame(self.panel2, bg="#F5F5F5")

        self.frame1_haut.pack(fill=tk.X, padx=5, pady=5)
        self.frame2_centre.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.frame2_centre.grid_columnconfigure(1, weight=1, minsize=240) # ← ajoute une largeur minimale contrôlée
        self.frame3_bas.pack(fill=tk.X, padx=5, pady=5)

        # --- Frame haut : recherche + boutons ---
        self.search_type_var = tk.StringVar(value="titre")
        
        # Frame radio (Titre / Artiste / Album)
        radio_frame = tk.Frame(self.frame1_haut, bg="#F5F5F5")
        radio_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Radiobutton(radio_frame, text="Titre", variable=self.search_type_var, value="titre", bg="#F5F5F5", font=self.FONT_PANEL2_SMALL).pack(side=tk.LEFT)
        tk.Radiobutton(radio_frame, text="Artiste", variable=self.search_type_var, value="artiste", bg="#F5F5F5", font=self.FONT_PANEL2_SMALL).pack(side=tk.LEFT)
        tk.Radiobutton(radio_frame, text="Album", variable=self.search_type_var, value="album", bg="#F5F5F5", font=self.FONT_PANEL2_SMALL).pack(side=tk.LEFT)
        
        # Frame pour les éléments à gauche (label + entry)
        left_frame = tk.Frame(self.frame1_haut, bg="#F5F5F5")
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Label
        self.label_Check = tk.Label(left_frame, text="Entrez votre recherche :", bg="#F5F5F5", font=self.FONT_PANEL2_SMALL)
        self.label_Check.pack(side=tk.LEFT, padx=5)
        
        # Entry
        self.entry_ecriture_haut = tk.Entry(left_frame, width=60, font=self.FONT_PANEL2_SMALL)
        self.entry_ecriture_haut.pack(side=tk.LEFT, padx=5)
        
        # Frame pour les boutons à droite
        buttons_frame = tk.Frame(self.frame1_haut, bg="#F5F5F5")
        buttons_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Bouton Rechercher
        self.butt_check_api = tk.Button(buttons_frame, text="Rechercher", width=12, command=self.check_search_from_top, font=self.FONT_PANEL2_SMALL)
        self.style_button(self.butt_check_api, bg_color="#2ECC71")
        self.butt_check_api.pack(side=tk.LEFT, padx=5)
        
        # Bouton Retour
        self.butt_retour_api = tk.Button(buttons_frame, text="Retour", width=12, command=self.return_full_list, font=self.FONT_PANEL2_SMALL)
        self.style_button(self.butt_retour_api, bg_color="#5D6D7E")
        self.butt_retour_api.pack(side=tk.LEFT, padx=5)

        #  Frame centre : trois colonnes 
        self.frame2_centre.grid_columnconfigure(0, weight=1)
        self.frame2_centre.grid_columnconfigure(1, weight=1)
        self.frame2_centre.grid_columnconfigure(2, weight=1)
        self.frame2_centre.grid_rowconfigure(0, weight=1)

        # gauche : listbox
        self.section1_gauche_liste = tk.Frame(self.frame2_centre, bg="#F5F5F5")
        self.section1_gauche_liste.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        self.audio_listbox = tk.Listbox(self.section1_gauche_liste, width=80, height=20, bg="#FFFFFF", selectbackground="#4E9F3D", font=self.FONT_PANEL2_SMALL)
        style_listbox(self.audio_listbox)
        self.audio_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        self.audio_listbox.bind("<Double-Button-1>", self.on_listbox_double)

        self.scrollbarlistbox = Scrollbar(self.section1_gauche_liste, orient="vertical", command=self.audio_listbox.yview)
        self.scrollbarlistbox.pack(side=tk.RIGHT, fill=tk.Y)
        self.audio_listbox.config(yscrollcommand=self.scrollbarlistbox.set)

        self.audio_listbox.drop_target_register(DND_FILES)
        self.audio_listbox.dnd_bind('<<Drop>>', self.on_drop)

        # centre : cover + boutons
        self.section2_centre_cover = tk.Frame(self.frame2_centre, bg="#F5F5F5")
        self.section2_centre_cover.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        self.centrale_label = tk.Frame(self.section2_centre_cover, bg="#F5F5F5")
        self.centrale_label.pack(fill='both', expand=True, padx=10, pady=10)

        self.A_label_cover = tk.Label(self.centrale_label, text="Aucune sélection", width=40, height=12, bg="#F5F5F5", relief=tk.RAISED, font=self.FONT_PANEL2_MEDIUM)
        self.A_label_cover.pack(pady=10, fill='both', expand=True)

        self.B_label_fichier_boutton = tk.Frame(self.centrale_label, bg="#F5F5F5")
        self.B_label_fichier_boutton.pack(fill='x', pady=5)

        self.B1_label_fichier_nom = tk.Label(self.B_label_fichier_boutton, text="", bg="#F5F5F5", anchor="w", font=self.FONT_PANEL2_MEDIUM)
        self.B1_label_fichier_nom.pack(side=tk.LEFT, padx=4)
        self.B1_label_fichier_nom.config(width=10, anchor="w")
        self.B1_label_fichier_nom.pack_propagate(False)


        self.B2_label_bouton_manip = tk.Frame(self.B_label_fichier_boutton, bg="#F5F5F5")
        self.B2_label_bouton_manip.pack(side=tk.RIGHT)

        # Boutons lecture
      
        self.panel_controls = tk.Frame(self.B2_label_bouton_manip, bg="#F5F5F5")
        self.panel_controls.pack(side=tk.LEFT)
        
        
        def add_btn(text, color, cmd):
            btn = tk.Button(
                self.panel_controls,
                text=text,
                width=2,
                height=1,
                font=("Segoe UI", 8, "bold"),
                padx=1, pady=1,
                command=cmd
            )
            self.style_button(btn, bg_color=color)
            btn.pack(side=tk.LEFT, padx=2)
        
        
        # Boutons lecture ULTRA COMPACTS + ALIGNEMENT FIXE
        add_btn("◀◀", "#5D6D7E", self.prev_audio)
        add_btn("▶", "#2ECC71", self.play_audio)
        add_btn("⏸", "#F1C40F", self.pause_resume)
        add_btn("▶▶", "#5D6D7E", self.next_audio)
        add_btn("🎤", "#E67E22", self.show_lyrics_popup)
        
        
        # droite : métadonnées
        self.section3_metaData = tk.Frame(self.frame2_centre, bg="#F5F5F5")
        self.section3_metaData.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)

        self.metaData_label = tk.Label(self.section3_metaData, text="", bg="#F5F5F5", justify="left", anchor="nw", font=self.FONT_PANEL2_SMALL)
        self.metaData_label.pack(fill='both', expand=True, padx=10, pady=10)

        #  Frame bas : exploration / playlist / logo 
        self.explo_playlist_boutton = tk.Frame(self.frame3_bas, bg="#F5F5F5")
        self.explo_playlist_boutton.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)

        self.zone_petit_logo = tk.Frame(self.frame3_bas, bg="#F5F5F5")
        self.zone_petit_logo.grid(row=0, column=2, sticky='nsew', padx=2, pady=2)

        try:
            if os.path.isfile(self.chem_im):
                im = Image.open(self.chem_im).resize((24,24))
                self.im_tk = ImageTk.PhotoImage(im)
            else:
                self.im_tk = None
        except Exception:
            self.im_tk = None

        if self.im_tk:
            self.label_img_petit_logo = tk.Label(self.zone_petit_logo, image=self.im_tk, bg="#F5F5F5")
        else:
            self.label_img_petit_logo = tk.Label(self.zone_petit_logo, text="", bg="#F5F5F5", fg="white")
        self.label_img_petit_logo.pack(side=tk.RIGHT, padx=10, pady=10)

        # boutons bas
        for text, cmd, color in [("Exploration",self.explore_folder,"#3498DB"),("Nouvelle Playlist",self.create_playlist,"#8E44AD"),
                                 ("Modifier Méta",self.edit_metadata,"#2ECC71"),("Ecouter Playlist",self.play_playlist,"#8E44AD")]:
            btn = tk.Button(self.explo_playlist_boutton, text=text, command=cmd, font=self.FONT_PANEL2_SMALL)
            self.style_button(btn, bg_color=color)
            btn.pack(side=tk.LEFT if text=="Exploration" else tk.RIGHT, padx=8, pady=8)

        # Frame pour le bouton Jour/Nuit
        frame_dark_mode = tk.Frame(self.frame3_bas, bg="#F5F5F5")
        frame_dark_mode.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        btn_dark_mode = tk.Button(frame_dark_mode, text="Jour/Nuit", command=self.toggle_dark_mode, font=self.FONT_PANEL2_SMALL)
        self.style_button(btn_dark_mode, bg_color="#8E44AD")
        btn_dark_mode.pack(expand=True)
        self.btn_dark_mode = btn_dark_mode


        # liaisons clavier
        self.master.bind("<Return>", lambda e: self.check_search_from_top())
        self.master.bind("<Left>", lambda e: self.prev_audio())
        self.master.bind("<Right>", lambda e: self.next_audio())


        # Par défaut on commence sur panel1
        self.tailleListbox = 0

        #  Mode sombre / clair 
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        colors = self.dark_colors if self.dark_mode else self.light_colors
    
        def recolor_widget(widget):
            # Frame
            if isinstance(widget, tk.Frame):
                widget.config(bg=colors["bg"])
            # Label
            elif isinstance(widget, tk.Label):
                widget.config(bg=colors["bg"], fg=colors["fg"])
            # Entry
            elif isinstance(widget, tk.Entry):
                widget.config(bg=colors["entry_bg"], fg=colors["fg"])
            # Listbox
            elif isinstance(widget, tk.Listbox):
                widget.config(
                    bg=colors["entry_bg"] if not self.dark_mode else "#4B0082",
                    fg=colors["fg"],
                    selectbackground=colors["select_bg"],
                    selectforeground=colors["select_fg"]
                )
            # Button
            elif isinstance(widget, tk.Button):
                # Si c'est le bouton Jour/Nuit, couleurs spéciales
                if widget == getattr(self, "btn_dark_mode", None):
                    widget.config(
                        bg=self.dark_colors["button_bg"] if self.dark_mode else self.light_colors["button_bg"],
                        fg=self.dark_colors["button_fg"] if self.dark_mode else self.light_colors["button_fg"]
                    )
                else:
                    widget.config(bg=colors["button_bg"], fg=colors["button_fg"])
            # Radiobutton
            elif isinstance(widget, tk.Radiobutton):
                widget.config(bg=colors["bg"], fg=colors["fg"], selectcolor=colors["bg"])
    
            # Appliquer récursivement aux enfants
            for child in widget.winfo_children():
                recolor_widget(child)
    
        # Appliquer sur la fenêtre principale
        recolor_widget(self.master)        
           
    #  Transition accueil -> panel2 
    def direct_Goto(self, event=None):
        self.panel1.pack_forget()
        self.panel2.pack(fill="both", expand=True)
        if os.path.isdir(self.default_music_dir):
            self.explore_folder(path=self.default_music_dir)
        if self.audio_listbox.size() > 0:
            self.audio_listbox.selection_set(0)
            self.audio_listbox.activate(0)
            path = self.audio_paths.get("0")
            if path:
                self.show_audio_details(path=path)

    #  Exploration dossier 
    def explore_folder(self, path=None):
        folder = path if path else filedialog.askdirectory()
        if not folder:
            return
        self.audio_list.clear()
        self.audio_paths.clear()
        i = 0
        for root_dir, dirs, files in os.walk(folder):
            for file in files:
                if file.lower().endswith((".mp3", ".flac")):
                    p = os.path.join(root_dir, file)
                    self.audio_list.append(file)
                    self.audio_paths[str(i)] = p
                    i += 1
        self.return_full_list()

    #  Lecture audio 
    def on_listbox_double(self, event=None):
        sel = self.audio_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
    
        # Si filtered_audio_list est vide, on prend la liste complète
        if self.filtered_audio_list:
            if idx >= len(self.filtered_audio_list):
                return
            item = self.filtered_audio_list[idx]
            if isinstance(item, dict) and item.get("type") == "local":
                path = item.get("path")
            elif isinstance(item, dict) and item.get("type") == "api":
                # Si API, on peut juste afficher les métadonnées
                rec = item.get("data", {})
                meta_text = (
                    f"Titre : {rec.get('Titre','Inconnu')}\n"
                    f"Artiste : {rec.get('Artiste','Inconnu')}\n"
                    f"Album : {rec.get('Album','Inconnu')}\n"
                    f"Genre : {rec.get('Genre','Inconnu')}\n"
                    f"Année : {rec.get('Année','Inconnu')}\n"
                    f"Commentaire : {rec.get('Commentaire','')}\n"
                )
                self.metaData_label.config(text=meta_text)
                return
            else:
                return
        else:
            # fallback : on prend la listbox complète
            path = self.audio_paths.get(str(idx))
    
        if path:
            self.current_index = idx
            self.show_audio_details(path=path)
            self.play_audio()


    def play_audio(self):
        path = self.audio_paths.get(str(self.current_index))
        if not path:
            sel = self.audio_listbox.curselection()
            if sel:
                path = self.audio_paths.get(str(sel[0]))
                self.current_index = sel[0]
        if not path or not os.path.exists(path):
            messagebox.showwarning("Lecture", "Fichier introuvable.")
            return
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            self.audio_playing = True
            self.is_paused = False
        except Exception as e:
            messagebox.showerror("Lecture", f"Impossible de lire le fichier : {e}")

    def pause_resume(self):
        if self.audio_playing:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.pause()
                self.is_paused = True

    def next_audio(self, event=None):
        if not self.audio_paths:
            return
        total = len(self.audio_paths)
        self.current_index = (self.current_index + 1) % total
        self.audio_listbox.selection_clear(0, tk.END)
        self.audio_listbox.selection_set(self.current_index)
        self.audio_listbox.activate(self.current_index)
        path = self.audio_paths.get(str(self.current_index))
        if path:
            self.show_audio_details(path=path)
            self.play_audio()

    def prev_audio(self, event=None):
        if not self.audio_paths:
            return
        total = len(self.audio_paths)
        self.current_index = (self.current_index - 1 + total) % total
        self.audio_listbox.selection_clear(0, tk.END)
        self.audio_listbox.selection_set(self.current_index)
        self.audio_listbox.activate(self.current_index)
        path = self.audio_paths.get(str(self.current_index))
        if path:
            self.show_audio_details(path=path)
            self.play_audio()

    #  Métadonnées & Cover 
    def show_audio_details(self, event=None, path=None):
        if path is None:
            sel = self.audio_listbox.curselection()
            if not sel:
                return
            idx = sel[0]
            if self.filtered_audio_list:
                name = self.filtered_audio_list[idx]
                path = next((p for p in self.audio_paths.values() if os.path.basename(p) == name), None)
            else:
                path = self.audio_paths.get(str(idx))
            self.current_index = idx
        if not path:
            return
        self.extract_metadata(path)
        self.show_cover(path)
        nom = os.path.basename(path)
        nom_aff = self.verifier_et_couper_nom_Milieu(nom)
        self.B1_label_fichier_nom.config(text=nom_aff)
        
    #  Modifier métadonnées 
    def edit_metadata(self):
        if not self.audio_paths:
            return
        path = self.audio_paths.get(str(self.current_index))
        if not path:
            return
    
        # STOP audio pour éviter conflit d'accès
        if pygame.mixer.get_init():
            pygame.mixer.quit()
    
        popup = Toplevel(self.master)
        popup.title("Modifier Métadonnées")
        popup.geometry("420x520")
    
        # Champs texte pour les métadonnées
        labels = ["Titre", "Artiste", "Album", "Genre", "Année", "Commentaire"]
        entries = {}
        for lbl in labels:
            tk.Label(popup, text=f"{lbl} :").pack(anchor="w", padx=10)
            entry = tk.Entry(popup, width=50)
            entry.pack(padx=10)
            entries[lbl.lower()] = entry
    
        # Charger valeurs actuelles
        try:
            if path.lower().endswith(".mp3"):
                audio = MP3(path, ID3=ID3)
                if audio.tags is None:
                    audio.add_tags()
                tags = audio.tags
                entries["titre"].insert(0, tags.get("TIT2").text[0] if tags.get("TIT2") else os.path.basename(path))
                entries["artiste"].insert(0, tags.get("TPE1").text[0] if tags.get("TPE1") else "Inconnu")
                entries["album"].insert(0, tags.get("TALB").text[0] if tags.get("TALB") else "Inconnu")
                entries["genre"].insert(0, tags.get("TCON").text[0] if tags.get("TCON") else "")
                entries["année"].insert(0, str(tags.get("TDRC").text[0]) if tags.get("TDRC") else "")
                # Commentaire
                comment = ""
                for f in tags.values():
                    if getattr(f, "FrameID", "") == "COMM" and hasattr(f, "text"):
                        comment = f.text[0]
                        break
                entries["commentaire"].insert(0, comment)
    
            elif path.lower().endswith(".flac"):
                audio = FLAC(path)
                entries["titre"].insert(0, audio.get("title", [""])[0])
                entries["artiste"].insert(0, audio.get("artist", [""])[0])
                entries["album"].insert(0, audio.get("album", [""])[0])
                entries["genre"].insert(0, audio.get("genre", [""])[0])
                entries["année"].insert(0, audio.get("date", [""])[0])
                entries["commentaire"].insert(0, audio.get("comment", [""])[0])
        except Exception as e:
            print("Erreur chargement meta popup :", e)
    
        # Bouton choisir cover
        def choose_cover():
            file = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
            if file:
                popup.selected_cover = file
    
        tk.Button(popup, text="Changer Cover", command=choose_cover).pack(pady=5)
        popup.selected_cover = None
    
        # Sauvegarde des modifications
        def save_changes():
            title = entries["titre"].get().strip()
            artist = entries["artiste"].get().strip()
            album = entries["album"].get().strip()
            genre = entries["genre"].get().strip()
            year = entries["année"].get().strip()
            comment = entries["commentaire"].get().strip()
            cover_file = getattr(popup, 'selected_cover', None)
    
            try:
                if path.lower().endswith(".mp3"):
                    audio = MP3(path, ID3=ID3)
                    if audio.tags is None:
                        audio.add_tags()
                    tags = audio.tags
    
                    # Texte
                    tags["TIT2"] = TIT2(encoding=3, text=title)
                    tags["TPE1"] = TPE1(encoding=3, text=artist)
                    tags["TALB"] = TALB(encoding=3, text=album)
                    tags["TCON"] = TCON(encoding=3, text=genre)
                    tags["TDRC"] = TDRC(encoding=3, text=year)
    
                    # Commentaire
                    tags.delall("COMM")
                    tags.add(COMM(encoding=3, lang="eng", desc="", text=comment))
    
                    # Cover
                    if cover_file:
                        tags.delall("APIC")
                        with open(cover_file, "rb") as img:
                            mime = "image/png" if cover_file.lower().endswith(".png") else "image/jpeg"
                            tags.add(APIC(
                                encoding=3,
                                mime=mime,
                                type=3,
                                desc="Cover",
                                data=img.read()
                            ))
    
                    audio.save(v2_version=3)
    
                elif path.lower().endswith(".flac"):
                    audio = FLAC(path)
                    audio["title"] = title
                    audio["artist"] = artist
                    audio["album"] = album
                    audio["genre"] = genre
                    audio["date"] = year
                    audio["comment"] = comment
    
                    if cover_file:
                        audio.clear_pictures()
                        pic = Picture()
                        with open(cover_file, "rb") as f:
                            pic.data = f.read()
                        pic.type = 3
                        pic.mime = "image/png" if cover_file.lower().endswith(".png") else "image/jpeg"
                        audio.add_picture(pic)
    
                    audio.save()
    
                popup.destroy()
                # Affichage immédiat de la nouvelle cover
                self.master.after(300, lambda: self.show_audio_details(path=path))
    
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder : {e}")
    
            finally:
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
    
        tk.Button(popup, text="Enregistrer", command=save_changes, bg="#27AE60", fg="white").pack(pady=10)          

    #  Métadonnées 
    def extract_metadata(self, path):
        try:

            duration = 0
            bitrate = sample_rate = channels = "Inconnu"
            title = artist = album = genre = year = comment = "Inconnu"
    
            if path.lower().endswith(".mp3"):
                audio = MP3(path, ID3=ID3)
                if audio.info:
                    duration = int(audio.info.length)
                    bitrate = f"{int(audio.info.bitrate/1000)} kbps"
                    sample_rate = f"{audio.info.sample_rate} Hz"
                    channels = audio.info.channels
    
                tags = audio.tags or {}
                title = tags.get("TIT2").text[0] if tags.get("TIT2") else os.path.basename(path)
                artist = tags.get("TPE1").text[0] if tags.get("TPE1") else "Inconnu"
                album = tags.get("TALB").text[0] if tags.get("TALB") else "Inconnu"
                genre = tags.get("TCON").text[0] if tags.get("TCON") else "Inconnu"
                year = str(tags.get("TDRC").text[0]) if tags.get("TDRC") else "Inconnu"

                self.current_artist = artist
                self.current_title = title

                # lire le premier commentaire existant, toutes langues
                comment = ""
                try:
                    for frame in tags.values():
                        if getattr(frame, "FrameID", "") == "COMM" and hasattr(frame, "text"):
                            comment = frame.text[0]
                            break
                except Exception as e:
                    comment = ""
                    print("Erreur lecture commentaire :", e)
    
            elif path.lower().endswith(".flac"):
                audio = FLAC(path)
                if audio.info:
                    duration = int(audio.info.length)
                    bitrate = f"{int(audio.info.bitrate/1000)} kbps" if hasattr(audio.info,"bitrate") else "Inconnu"
                    sample_rate = f"{audio.info.sample_rate} Hz" if hasattr(audio.info,"sample_rate") else "Inconnu"
                    channels = audio.info.channels if hasattr(audio.info,"channels") else "Inconnu"
                title = audio.get("title", ["Inconnu"])[0]
                artist = audio.get("artist", ["Inconnu"])[0]
                album = audio.get("album", ["Inconnu"])[0]
                genre = audio.get("genre", ["Inconnu"])[0]
                year = audio.get("date", ["Inconnu"])[0]
                comment = audio.get("comment", [""])[0]
    
            mins = duration // 60
            secs = duration % 60
            dur_str = f"{mins}m {secs}s" if duration else "0m 0s"
    
            meta_text = (
                f"Titre : {title}\n"
                f"Artiste : {artist}\n"
                f"Album : {album}\n"
                f"Genre : {genre}\n"
                f"Année : {year}\n"
                f"Commentaire : {comment}\n"
                f"Durée : {dur_str}\n"
                f"Bitrate : {bitrate}\n"
                f"Sample rate : {sample_rate}\n"
                f"Channels : {channels}"
            )
            self.metaData_label.config(text=meta_text)
    
        except Exception as e:
            self.metaData_label.config(text="Métadonnées : Inconnues")
            print("Erreur extraction metadata :", e)         
      
    def show_cover(self, path):
        try:
            img = None
            if path.lower().endswith(".mp3"):
                audio = MP3(path, ID3=ID3)
                # Chercher le premier APIC disponible
                apics = [tag for tag in audio.tags.values() if getattr(tag, "FrameID", "") == "APIC"]
                if apics:
                    img = Image.open(io.BytesIO(apics[0].data))
            elif path.lower().endswith(".flac"):
                audio = FLAC(path)
                if audio.pictures:
                    img = Image.open(io.BytesIO(audio.pictures[0].data))
            if img:
                img = img.resize((200, 200))
                self.cover_tk = ImageTk.PhotoImage(img, master=self.master)
                self.A_label_cover.config(image=self.cover_tk, text="")
            else:
                self.A_label_cover.config(image="", text="Pas de couverture")
        except Exception as e:
            print("Erreur show_cover :", e)
            self.A_label_cover.config(image="", text="Erreur couverture")

         
    #  Recherche  API 
    def check_search_from_top(self):
           query = self.entry_ecriture_haut.get().strip()
           if not query:
               messagebox.showwarning("Recherche", "Veuillez entrer un texte pour rechercher.")
               return
           search_type = self.search_type_var.get()   #  Récupère le type choisi
           self.check_search(query=query, search_type=search_type)

    def check_search(self, query=None, search_type="titre"):
        if query is None:
            messagebox.showwarning("Recherche", "Aucun texte fourni.")
            return
        q = query.strip().lower()
    
        #   Recherche locale 
        self.audio_listbox.delete(0, tk.END)
        self.filtered_audio_list.clear()
    
        results_local = []
        local_paths = []
        for idx, name in enumerate(self.audio_list):
            path = self.audio_paths.get(str(idx))
            try:
                if path.lower().endswith(".mp3"):
                    audio = MP3(path, ID3=ID3)
                    title = audio.tags.get("TIT2").text[0].lower() if audio.tags.get("TIT2") else ""
                    artist = audio.tags.get("TPE1").text[0].lower() if audio.tags.get("TPE1") else ""
                    album = audio.tags.get("TALB").text[0].lower() if audio.tags.get("TALB") else ""
                elif path.lower().endswith(".flac"):
                    audio = FLAC(path)
                    title = audio.get("title", [""])[0].lower()
                    artist = audio.get("artist", [""])[0].lower()
                    album = audio.get("album", [""])[0].lower()
                else:
                    continue
            except Exception:
                title = artist = album = ""
    
            match = False
            if search_type == "titre" and q in title:
                match = True
            elif search_type == "artiste" and q in artist:
                match = True
            elif search_type == "album" and q in album:
                match = True
    
            if match:
                results_local.append(name)
                local_paths.append(path)
    
        # Afficher les résultats locaux dans la listbox principale
        for i, name in enumerate(results_local):
            self.audio_listbox.insert(tk.END, self.truncate_name(name))
            self.filtered_audio_list.append({"type": "local", "path": local_paths[i]})
    
        if not results_local:
            self.audio_listbox.insert(tk.END, "Aucun résultat local trouvé.")
    
        #   Recherche API dans popup 
        self.search_api_popup(query, search_type)

    
        #  Double-clic géré pour local et API 
        def on_double_click(self, event=None):
            sel = self.audio_listbox.curselection()
            if not sel:
                return
        
            idx = sel[0]
        
            # Vérifie que l'index est valide
            if idx >= len(self.filtered_audio_list):
                return
        
            item = self.filtered_audio_list[idx]
        
            if isinstance(item, dict) and item.get("type") == "local":
                path = item.get("path")
                if path and os.path.exists(path):
                    self.current_index = next(
                        (i for i, p in self.audio_paths.items() if p == path), 0
                    )
                    self.show_audio_details(path=path)
                    self.play_audio()
            elif isinstance(item, dict) and item.get("type") == "api":
                rec = item.get("data", {})
                meta_text = (
                    f"Titre : {rec.get('Titre','Inconnu')}\n"
                    f"Artiste : {rec.get('Artiste','Inconnu')}\n"
                    f"Album : {rec.get('Album','Inconnu')}\n"
                    f"Genre : {rec.get('Genre','Inconnu')}\n"
                    f"Année : {rec.get('Année','Inconnu')}\n"
                    f"Commentaire : {rec.get('Commentaire','')}\n"
                )
                self.metaData_label.config(text=meta_text)


    def search_api_popup(self, query, search_type):
        try:
            results = self.fetcher.search_recordings(query, search_type, limit=10)

            if not results:
                messagebox.showinfo("API", "Aucun résultat trouvé via l'API.")
                return
    
            popup = Toplevel(self.master)
            popup.title(f"Résultats API pour '{query}'")
            popup.geometry("600x400")
    
            listbox_api = tk.Listbox(popup, font=("Segoe UI", 12))
            listbox_api.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
            # Afficher chaque résultat API
            for rec in results:
                display_text = f"[{rec.get('API')}] {rec.get('Titre','?')} - {rec.get('Artiste','?')} ({rec.get('Album','?')})"

                listbox_api.insert(tk.END, display_text)

            # Double-clic : afficher métadonnées
            def choose_api(event=None):
                sel = listbox_api.curselection()
                if not sel:
                    return
                rec = results[sel[0]]
                meta_text = (
                    f"Titre : {rec.get('Titre','Inconnu')}\n"
                    f"Artiste : {rec.get('Artiste','Inconnu')}\n"
                    f"Album : {rec.get('Album','Inconnu')}\n"
                    f"Genres : {', '.join(rec.get('Genres', []))}\n"
                    f"Moods : {', '.join(rec.get('Moods', []))}\n"
                    f"Instruments : {', '.join(rec.get('Instruments', []))}\n"
                    f"Année : {rec.get('Année','Inconnu')}\n"
                    
                )


                self.metaData_label.config(text=meta_text)
                # afficher cover API
                cover_url = rec.get("Cover")
                if cover_url:
                    try:
                        img_data = requests.get(cover_url).content
                        img = Image.open(io.BytesIO(img_data)).resize((200, 200))
                        self.cover_tk = ImageTk.PhotoImage(img)
                        self.A_label_cover.config(image=self.cover_tk, text="")
                    except:
                        self.A_label_cover.config(text="Cover non disponible", image="")

    
            # Ajouter à la bibliothèque
            def add_to_library():
                sel = listbox_api.curselection()
                if not sel:
                    messagebox.showwarning("Sélection", "Veuillez sélectionner une piste.")
                    return
            
                rec = results[sel[0]]
                url = rec.get("Audio")
                titre = rec.get("Titre")
                artiste = rec.get("Artiste")
            
                if not url:
                        messagebox.showwarning("Audio indisponible",
                           "Cette piste vient de MusicBrainz.\nElle n'a pas de fichier audio téléchargeable.")
                        return

            
                filename = f"{artiste} - {titre}.mp3"
                path = os.path.join(self.api_music_dir, filename)
            
                try:
                    # Téléchargement réel du MP3
                    r = requests.get(url, stream=True)
                    with open(path, "wb") as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
            
                    # Ajout à la bibliothèque locale
                    idx = str(len(self.audio_paths))
                    self.audio_paths[idx] = path
                    self.audio_list.append(filename + " (API)")  # ← Ici on ajoute la mention (API)
                    self.audio_listbox.insert(tk.END, self.truncate_name(filename + " (API)"))
            
                    messagebox.showinfo("Ajout", f"Fichier téléchargé et ajouté : {filename} (API)")
            
                    popup.destroy()
            
                    # Lecture immédiate
                    self.current_index = int(idx)
                    self.show_audio_details(path=path)
                    self.play_audio()
            
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de télécharger : {e}")

            # Lier le double-clic à choose_api
            listbox_api.bind("<Double-1>", choose_api)
    
            # Bouton pour ajouter la piste sélectionnée
            add_button = tk.Button(popup, text="Ajouter à la bibliothèque", command=add_to_library)
            add_button.pack(pady=5)

        except Exception as e:
            messagebox.showerror("Erreur API", f"Erreur lors de la recherche : {e}")

    #  Playlists 
    def create_playlist(self):
        if not self.audio_list:
            messagebox.showwarning("Playlist", "Aucune musique disponible pour créer une playlist.")
            return
    
        popup = Toplevel(self.master)
        popup.title("Nouvelle Playlist")
        popup.geometry("450x500")
        tk.Label(popup, text="Sélectionner les musiques à ajouter :").pack(pady=5)
    
        # Frame pour contenir les checkboxes avec scrollbar
        frame = tk.Frame(popup)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)
    
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
    
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        # Création dynamique des checkboxes
        self.playlist_vars = []
        for name in self.audio_list:
            var = tk.IntVar(value=0)
            cb = tk.Checkbutton(scroll_frame, text=name, variable=var, anchor="w", justify="left")
            cb.pack(fill="x", anchor="w")
            self.playlist_vars.append((var, name))

        # Sauvegarde de la playlist
        def save_playlist():
            selected_paths = []
            for var, name in self.playlist_vars:
                if var.get() == 1:  # cochée
                    for idx, fname in enumerate(self.audio_list):
                        if fname == name:
                            path = self.audio_paths.get(str(idx))
                            if path and os.path.exists(path):
                                selected_paths.append(path)
                            break
    
            if not selected_paths:
                messagebox.showwarning("Playlist", "Veuillez sélectionner au moins une musique.")
                return
    
            self.current_playlist = selected_paths
            popup.destroy()
            save_path = filedialog.asksaveasfilename(defaultextension=".xspf", filetypes=[("XSPF Playlist","*.xspf")])
            if save_path:
                try:
                    import xml.etree.ElementTree as ET
                    playlist = ET.Element("playlist", version="1", xmlns="http://xspf.org/ns/0/")
                    trackList = ET.SubElement(playlist, "trackList")
                    for path in self.current_playlist:
                        track = ET.SubElement(trackList, "track")
                        ET.SubElement(track, "location").text = f"file:///{path}"
                        ET.SubElement(track, "title").text = os.path.basename(path)
                    tree = ET.ElementTree(playlist)
                    tree.write(save_path, encoding="utf-8", xml_declaration=True)
                    messagebox.showinfo("Playlist", f"Playlist sauvegardée : {save_path}")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de sauvegarder la playlist : {e}")
        
        # Bouton Annuler : ferme simplement le popup
        def cancel_playlist():
            popup.destroy()
    
        # Boutons en bas
        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Créer Playlist", command=save_playlist, bg="#27AE60", fg="white").pack(side="left", padx=5)
        tk.Button(button_frame, text="Annuler", command=cancel_playlist, bg="#E74C3C", fg="white").pack(side="left", padx=5)
    
    #  play_playlist 
    def play_playlist(self):
        if not self.current_playlist:
            messagebox.showwarning("Playlist", "Aucune playlist chargée ou créée.")
            return

        self.audio_list.clear()
        self.audio_paths.clear()
        for i, path in enumerate(self.current_playlist):
            if os.path.exists(path):
                self.audio_paths[str(i)] = path
                name = os.path.basename(path)
                if path.startswith(self.api_music_dir):
                    name += " (API)"
                self.audio_list.append(name)

        self.return_full_list()
        self.current_index = 0
        self.show_audio_details(path=self.audio_paths.get(str(self.current_index)))
        self.play_audio()

    # open_playlist
    def open_playlist(self):
        path = filedialog.askopenfilename(filetypes=[("XSPF Playlist", "*.xspf")])
        if not path:
            return
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(path)
            root = tree.getroot()
            playlist_paths = []
            for track in root.findall(".//{http://xspf.org/ns/0/}track"):
                loc = track.find("{http://xspf.org/ns/0/}location")
                if loc is not None:
                    file_path = loc.text.replace("file:///", "")
                    if os.path.exists(file_path):
                        playlist_paths.append(file_path)

            if not playlist_paths:
                messagebox.showinfo("Playlist", "Aucune piste valide trouvée dans la playlist.")
                return

            self.audio_list.clear()
            self.audio_paths.clear()
            for i, p in enumerate(playlist_paths):
                self.audio_paths[str(i)] = p
                name = os.path.basename(p)
                if p.startswith(self.api_music_dir):
                    name += " (API)"
                self.audio_list.append(name)

            self.return_full_list()
            self.current_playlist = playlist_paths
            messagebox.showinfo("Playlist", f"{len(self.current_playlist)} musiques chargées depuis la playlist.")
        except Exception as e:
            messagebox.showerror("Playlist", f"Erreur lors de l'ouverture : {e}")


    #  Utilitaires 
    def return_full_list(self):
        self.audio_listbox.delete(0, tk.END)
        self.filtered_audio_list.clear()
        self.audio_list = [os.path.basename(p) for p in self.audio_paths.values()]
        for idx, name in enumerate(self.audio_list):
            self.audio_listbox.insert(tk.END, self.truncate_name(name))
        self.tailleListbox = self.audio_listbox.size()

    def truncate_name(self, name, max_len=None):
        if max_len is None:
            max_len = self.max_length
        return name if len(name) <= max_len else name[:max_len]+"..."

    def verifier_et_couper_nom_Milieu(self, nom_fichier: str) -> str:
        max_length = self.max_length_milieu
        if len(nom_fichier) > max_length:
            return nom_fichier[:max_length] + "..."
        
        return nom_fichier

    #dépôt de fichiers via drag & drop
    # dépôt de fichiers via drag & drop (sans supprimer l'original)
    def on_drop(self, event):
        # Récupération des fichiers déposés
        files = self.master.tk.splitlist(event.data)
        dest_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "music")
        os.makedirs(dest_dir, exist_ok=True)
    
        valid_files = []
        invalid_files = []
    
        for file_path in files:
            file_path = file_path.strip('{}').strip()
    
            if not os.path.isfile(file_path):
                invalid_files.append(file_path)
                continue
    
            if self.is_audio_file(file_path):
                try:
                    new_path = os.path.join(dest_dir, os.path.basename(file_path))
                    # Copier le fichier au lieu de le déplacer
                    import shutil
                    if not os.path.exists(new_path):
                        shutil.copy2(file_path, new_path)
                    valid_files.append(new_path)
                except Exception as e:
                    print(f"Erreur lors de la copie de {file_path} : {e}")
                    invalid_files.append(file_path)
            else:
                invalid_files.append(file_path)
    
        if valid_files:
            messagebox.showinfo("Fichiers copiés", f"{len(valid_files)} fichier(s) copiés dans {dest_dir}")
            self.explore_folder(path=dest_dir)
    
        if invalid_files:
            messagebox.showwarning("Fichiers invalides", f"{len(invalid_files)} fichier(s) non valides:\n" + "\n".join(invalid_files))

        return event.action
    #Vérifie si un fichier est au format MP3 ou FLAC
    def is_audio_file(self, file_path):
        ext = file_path.lower()
        if not (ext.endswith('.mp3') or ext.endswith('.flac')):
            return False

        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type in ['audio/mpeg', 'audio/x-flac', 'audio/flac']


#  Lancement
if __name__ == "__main__":
    root =TkinterDnD.Tk()
    app = AudioApp(root)
    root.mainloop()
