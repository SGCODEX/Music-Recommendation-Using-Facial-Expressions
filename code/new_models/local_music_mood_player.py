"""
Music Recommendation Using Facial Expressions - Local Library Edition
======================================================================

This single-file GUI integrates facial expression detection with a local
music library cache. The script can compute your music library recursively
and then play music from your local library based on detected emotions.

Requirements:
- tensorflow==2.15.0
- keras==2.15.0
- opencv-python
- numpy
- tkinter (built-in with Python)
- mood_detector (pip install git+https://github.com/wedsmoker/Mood-Detector.git)

Usage:
    python local_music_mood_player.py --compute --music-folder "path/to/music"
    python local_music_mood_player.py

Cache and model files are located relative to the script location.
The cache file is created in the same directory as this script.
"""

import cv2
import numpy as np
import json
import os
import random
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import threading
import subprocess
import sys
import time
from collections import deque
from statistics import mode, StatisticsError
from io import BytesIO
from pathlib import Path
import argparse

# Try to import keras/tensorflow
try:
    from keras.models import load_model
except ImportError:
    print("ERROR: Keras not found. Install with: pip install tensorflow==2.15.0 keras==2.15.0")
    sys.exit(1)

# Try to import pygame for music playback
try:
    import pygame
    pygame.mixer.init()
except ImportError:
    print("ERROR: Pygame not found. Install with: pip install pygame")
    sys.exit(1)

# Try to import mutagen for album art extraction (optional)
try:
    from mutagen import File as MutagenFile
    from mutagen.id3 import ID3, APIC
    from mutagen.mp3 import MP3
    from mutagen.flac import FLAC
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False
    print("Note: mutagen not found. Album art will not be displayed. Install with: pip install mutagen")

# Try to import mood_detector for music analysis
try:
    from mood_detector import analyze_audio
    MOOD_DETECTOR_AVAILABLE = True
except ImportError:
    MOOD_DETECTOR_AVAILABLE = False
    print("Note: mood_detector not found. Cache computation disabled. Install with: pip install git+https://github.com/wedsmoker/Mood-Detector.git")


class LocalMusicMoodPlayer:
    """Main application class for facial expression detection and local music playback"""

    # Emotion to music mood mapping based on energy/tempo characteristics
    # Now includes all 22 available mood categories for better matching
    EMOTION_TO_MUSIC_MOOD = {
        'Happy': {
            'moods': [
                'Disco/Funk',           # Classic happy/dance vibes
                'Club/Groovy',          # Upbeat club music
                'House/Dance',          # Dance floor energy
                'Upbeat/Moderate',      # Positive moderate tempo
                'Moderate Groove',      # Feel-good grooves
                'Energetic/Rave',       # High energy happiness
                'Breakbeat/Fast',       # Energetic breakbeats
            ],
            'energy_range': (0.5, 1.0),
            'tempo_range': (100, 150)
        },
        'Sad': {
            'moods': [
                'Melancholic/Sad',      # Direct sad mood match
                'Ambient/Atmospheric',   # Introspective ambience
                'Ambient/Drone',        # Deep, contemplative
                'Atmospheric/Textural', # Emotional textures
                'Minimal/Sparse',       # Stripped down, lonely
                'Relaxed/Moderate',     # Slow, reflective
            ],
            'energy_range': (0.0, 0.4),
            'tempo_range': (60, 95)
        },
        'Angry': {
            'moods': [
                'Hard/Aggressive',      # Direct aggressive match
                'Techno/Industrial',    # Harsh industrial sounds
                'Harsh Noise/Experimental', # Chaotic, angry
                'Drum & Bass',          # Fast, aggressive beats
                'Energetic/Rave',       # Intense energy
                'Techno/Dark',          # Dark, pounding techno
                'Breakbeat/Fast',       # Aggressive breakbeats
            ],
            'energy_range': (0.7, 1.0),
            'tempo_range': (130, 220)
        },
        'Neutral': {
            'moods': [
                'Moderate Groove',      # Balanced, neutral groove
                'Midtempo Groove',      # Medium-paced neutral
                'Relaxed/Moderate',     # Calm, balanced
                'Atmospheric/Textural', # Neutral ambience
                'Upbeat/Moderate',      # Slightly positive neutral
                'Ambient/Atmospheric',  # Chill background
                'House/Dance',          # Neutral dance vibes
                'Club/Groovy',          # Easy grooves
            ],
            'energy_range': (0.3, 0.6),
            'tempo_range': (85, 120)
        },
        'Surprise': {
            'moods': [
                'Fast/Atmospheric',     # Unexpected, fast-paced
                'Glitch/Experimental',  # Surprising, unusual sounds
                'Breakbeat/Fast',       # Dynamic, surprising beats
                'Energetic/Rave',       # Sudden energy burst
                'Drum & Bass',          # Fast, complex rhythms
                'Upbeat/Moderate',      # Positive surprise
                'Club/Groovy',          # Exciting club energy
                'Techno/Industrial',    # Unexpected industrial elements
            ],
            'energy_range': (0.5, 0.9),
            'tempo_range': (115, 170)
        },
        'Fear': {
            'moods': [
                'Techno/Dark',          # Dark, ominous
                'Dark House',           # Mysterious, tense
                'Ambient/Drone',        # Eerie, unsettling
                'Atmospheric/Textural', # Tense atmosphere
                'Harsh Noise/Experimental', # Disturbing sounds
                'Minimal/Sparse',       # Sparse, isolating
                'Ambient/Atmospheric',  # Eerie ambience
                'Glitch/Experimental',  # Unpredictable, anxious
            ],
            'energy_range': (0.2, 0.6),
            'tempo_range': (70, 110)
        },
        'Disgust': {
            'moods': [
                'Harsh Noise/Experimental', # Abrasive, unpleasant
                'Techno/Industrial',    # Harsh industrial
                'Glitch/Experimental',  # Distorted, unsettling
                'Hard/Aggressive',      # Aggressive, confrontational
                'Techno/Dark',          # Dark, gritty
                'Dark House',           # Underground, gritty
                'Minimal/Sparse',       # Cold, detached
            ],
            'energy_range': (0.4, 0.8),
            'tempo_range': (85, 140)
        }
    }

    def __init__(self, cache_path=None, model_path=None, music_folder=None):
        """Initialize the application"""

        # Set default paths relative to script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.cache_path = cache_path or os.path.join(script_dir, ".mood_cache.json")
        
        # Adjust model path based on script location
        # If script is in code/new_models, adjust path accordingly
        if "code" in script_dir and "new_models" in script_dir:
            # Script is in code/new_models, so model is up one directory and into code/model
            default_model_path = os.path.join(script_dir, "..", "..", "code", "model", "fer2013_mini_XCEPTION.102-0.66.hdf5")
        else:
            # Script is in root or elsewhere
            default_model_path = os.path.join(script_dir, "code", "model", "fer2013_mini_XCEPTION.102-0.66.hdf5")
        
        self.model_path = model_path or os.path.normpath(default_model_path)
        self.music_folder = music_folder
        self.music_cache = {}
        self.emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        self.current_emotion = None
        self.video_running = True
        self.cap = None
        self.model = None
        self.face_cascade = None

        # Mood smoothing - track last N emotions to reduce flickering
        self.mood_history = deque(maxlen=15)  # Track last 15 detections (~1.5 seconds at 10fps)
        self.smoothed_emotion = None

        # Continuous playback state
        self.is_playing = False
        self.playback_thread = None
        self.current_track_process = None
        self.used_tracks = deque(maxlen=50)  # Remember last 50 tracks to avoid repetition
        self.skip_current_track = False  # Flag to skip current track

        # Playback history tracking
        self.playback_history = []
        self.current_track_info = None
        self.current_album_art = None

        # Load ML model first (needed for both cache and GUI)
        self.load_model()

        # Initialize GUI first so we can show progress
        self.init_gui()
        
        # Load music cache or compute it
        if not self.load_music_cache():
            # If no cache exists, prompt user to select music folder and compute cache
            self.prompt_and_compute_cache()

        # Initialize GUI
        # (GUI already initialized above)

    def load_music_cache(self):
        """Load the precomputed music cache from JSON file"""
        if not os.path.exists(self.cache_path):
            print(f"Cache file not found at: {self.cache_path}")
            return False

        print(f"Loading music cache from: {self.cache_path}")
        with open(self.cache_path, 'r', encoding='utf-8') as f:
            self.music_cache = json.load(f)

        print(f"Loaded {len(self.music_cache)} tracks from cache")

        # Extract unique moods for debugging
        moods = set()
        for track_info in self.music_cache.values():
            if 'mood' in track_info:
                moods.add(track_info['mood'])
        print(f"Found {len(moods)} unique moods in cache: {sorted(moods)}")
        
        return True

    def prompt_and_compute_cache(self):
        """Prompt user to select a music folder and compute the cache if mood_detector is available"""
        if not MOOD_DETECTOR_AVAILABLE:
            messagebox.showerror("Error", 
                "mood_detector library not found. Please install it with:\n\n"
                "pip install git+https://github.com/wedsmoker/Mood-Detector.git\n\n"
                "Without this library, the cache cannot be computed automatically.\n"
                "You can create a cache file manually with the expected format.")
            return

        # Ask user if they want to compute cache now
        response = messagebox.askyesno(
            "No Cache Found", 
            f"No music cache found at:\n{self.cache_path}\n\n"
            "Would you like to select a music folder and compute the cache now?\n"
            "(This may take several minutes depending on your library size)"
        )
        
        if response:
            # Let user select music folder
            if not self.music_folder:
                self.music_folder = filedialog.askdirectory(
                    title="Select Music Folder to Analyze",
                    initialdir=os.path.expanduser("~")
                )
            
            if self.music_folder and os.path.isdir(self.music_folder):
                self.compute_music_cache()
            else:
                messagebox.showinfo("Info", "No music folder selected. The application will continue without a cache.")
        else:
            messagebox.showinfo("Info", "No music folder selected. The application will continue without a cache.")

    def compute_music_cache(self):
        """Compute music cache by recursively analyzing audio files in the music folder"""
        if not MOOD_DETECTOR_AVAILABLE:
            print("ERROR: mood_detector library not available for cache computation.")
            return

        # Supported audio formats
        supported_formats = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma', '.m4p'}
        
        # Find all audio files recursively
        all_audio_files = []
        for root, dirs, files in os.walk(self.music_folder):
            for file in files:
                if Path(file).suffix.lower() in supported_formats:
                    all_audio_files.append(os.path.join(root, file))
        
        if not all_audio_files:
            messagebox.showwarning("No Audio Files", 
                f"No supported audio files found in {self.music_folder}")
            return

        print(f"Found {len(all_audio_files)} audio files to analyze")
        
        # Show progress window
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Computing Music Cache")
        progress_window.geometry("400x100")
        progress_window.transient(self.root)
        progress_window.grab_set()  # Make it modal
        
        # Progress label
        progress_label = tk.Label(progress_window, text="Analyzing 0 of 0 files...")
        progress_label.pack(pady=10)
        
        # Progress bar
        progress_bar = ttk.Progressbar(progress_window, mode='determinate', maximum=len(all_audio_files))
        progress_bar.pack(pady=10, padx=20, fill=tk.X)
        
        # Cancel button
        cancel_button = tk.Button(progress_window, text="Cancel", 
                                 command=lambda: setattr(self, '_cancel_cache_computation', True))
        cancel_button.pack(pady=5)
        
        self._cancel_cache_computation = False
        analyzed_count = 0
        cache = {}
        
        # Process each file
        for i, file_path in enumerate(all_audio_files):
            if self._cancel_cache_computation:
                print("Cache computation cancelled by user")
                break
                
            try:
                # Update progress
                progress_label.config(text=f"Analyzing {i+1} of {len(all_audio_files)}: {os.path.basename(file_path)}")
                progress_bar['value'] = i + 1
                progress_window.update()
                
                # Check if file has been modified since last cache
                mtime = os.path.getmtime(file_path)
                
                # Skip if already in cache and unchanged
                if file_path in self.music_cache:
                    cached = self.music_cache[file_path]
                    if cached.get("mtime", 0) == mtime and "mood" in cached:
                        cache[file_path] = cached
                        continue
                
                # Analyze the audio file
                result = analyze_audio(file_path)
                cache[file_path] = {
                    "mood": result.mood,
                    "tempo": result.tempo,
                    "energy": result.energy,
                    "key": result.key,
                    "mtime": mtime
                }
                analyzed_count += 1
                
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
                # Keep old cache entry if exists, else skip
                if file_path in self.music_cache:
                    cache[file_path] = self.music_cache[file_path]
        
        # Save the cache
        with open(self.cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2)
        
        self.music_cache = cache
        progress_window.destroy()
        
        print(f"Cache computation completed. Analyzed {analyzed_count} new files. Total: {len(cache)} tracks in cache.")
        messagebox.showinfo("Cache Created", 
            f"Music cache created successfully!\n{analyzed_count} new files analyzed.\nTotal: {len(cache)} tracks in cache.\nCache saved to: {self.cache_path}")

    def load_model(self):
        """Load the pre-trained emotion detection model"""
        if not os.path.exists(self.model_path):
            messagebox.showerror("Error", f"Model file not found at:\n{self.model_path}")
            sys.exit(1)

        print(f"Loading emotion detection model from: {self.model_path}")
        self.model = load_model(self.model_path)

        # Load Haar Cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        print("Model loaded successfully")

    def init_gui(self):
        """Initialize the tkinter GUI"""
        self.root = tk.Tk()
        self.root.title("Facial Expression → Local Music Player")
        self.root.geometry("1400x800")
        self.root.configure(bg='#2b2b2b')

        # Create main container with two panels
        main_container = tk.Frame(self.root, bg='#2b2b2b')
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left panel - main video/controls
        left_panel = tk.Frame(main_container, bg='#2b2b2b')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right panel - sidebar for now playing and history
        right_panel = tk.Frame(main_container, bg='#1a1a1a', width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH)
        right_panel.pack_propagate(False)

        # === LEFT PANEL - Main content ===
        # Title
        title_frame = tk.Frame(left_panel, bg='#2b2b2b')
        title_frame.pack(pady=10)

        title_label = tk.Label(
            title_frame,
            text="🎵 Facial Expression Music Player 🎵",
            font=('Arial', 20, 'bold'),
            bg='#2b2b2b',
            fg='white'
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text="Using precomputed local music library",
            font=('Arial', 10),
            bg='#2b2b2b',
            fg='#888888'
        )
        subtitle_label.pack()

        # Video frame
        video_frame = tk.Frame(left_panel, bg='#1a1a1a', relief=tk.SUNKEN, borderwidth=2)
        video_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.video_label = tk.Label(video_frame, bg='#1a1a1a')
        self.video_label.pack(pady=10)

        # Emotion display
        emotion_frame = tk.Frame(left_panel, bg='#2b2b2b')
        emotion_frame.pack(pady=5)

        tk.Label(
            emotion_frame,
            text="Detected Emotion:",
            font=('Arial', 12),
            bg='#2b2b2b',
            fg='white'
        ).pack(side=tk.LEFT, padx=5)

        self.emotion_label = tk.Label(
            emotion_frame,
            text="None",
            font=('Arial', 12, 'bold'),
            bg='#2b2b2b',
            fg='#00ff00',
            width=15
        )
        self.emotion_label.pack(side=tk.LEFT, padx=5)

        # Control buttons
        button_frame = tk.Frame(left_panel, bg='#2b2b2b')
        button_frame.pack(pady=10)

        self.start_button = tk.Button(
            button_frame,
            text="▶ Start Mood Player",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            command=self.start_continuous_playback,
            width=20,
            height=2
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(
            button_frame,
            text="⏹ Stop",
            font=('Arial', 12, 'bold'),
            bg='#FF9800',
            fg='white',
            command=self.stop_continuous_playback,
            width=15,
            height=2,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.skip_button = tk.Button(
            button_frame,
            text="⏭ Skip",
            font=('Arial', 12, 'bold'),
            bg='#2196F3',
            fg='white',
            command=self.skip_track,
            width=12,
            height=2,
            state=tk.DISABLED
        )
        self.skip_button.pack(side=tk.LEFT, padx=5)

        self.quit_button = tk.Button(
            button_frame,
            text="❌ Quit",
            font=('Arial', 12, 'bold'),
            bg='#f44336',
            fg='white',
            command=self.quit_app,
            width=10,
            height=2
        )
        self.quit_button.pack(side=tk.LEFT, padx=5)

        # Status text
        status_frame = tk.Frame(left_panel, bg='#2b2b2b')
        status_frame.pack(pady=5, padx=20, fill=tk.BOTH)

        self.status_text = tk.Text(
            status_frame,
            height=6,
            font=('Courier', 9),
            bg='#1a1a1a',
            fg='#00ff00',
            wrap=tk.WORD
        )
        self.status_text.pack(fill=tk.BOTH, expand=True)

        # Add scrollbar
        scrollbar = tk.Scrollbar(self.status_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.status_text.yview)

        # === RIGHT PANEL - Now Playing and History ===
        self.init_sidebar(right_panel)

        self.log_status(f"Loaded {len(self.music_cache)} tracks from cache")
        self.log_status("Starting webcam...")
        self.log_status("Mood smoothing enabled (tracks last 15 detections)")
        self.log_status("Click 'Start Mood Player' to begin continuous playback")

    def init_sidebar(self, parent):
        """Initialize the sidebar with now playing and history"""
        # Sidebar title
        sidebar_title = tk.Label(
            parent,
            text="NOW PLAYING",
            font=('Arial', 14, 'bold'),
            bg='#1a1a1a',
            fg='#00ff00',
            pady=10
        )
        sidebar_title.pack()

        # Album art display
        art_frame = tk.Frame(parent, bg='#1a1a1a')
        art_frame.pack(pady=10)

        self.album_art_label = tk.Label(
            art_frame,
            bg='#2b2b2b',
            width=250,
            height=250
        )
        self.album_art_label.pack()

        # Current track info
        info_frame = tk.Frame(parent, bg='#1a1a1a')
        info_frame.pack(pady=10, padx=10, fill=tk.X)

        self.now_playing_track = tk.Label(
            info_frame,
            text="No track playing",
            font=('Arial', 10, 'bold'),
            bg='#1a1a1a',
            fg='white',
            wraplength=350,
            justify=tk.LEFT
        )
        self.now_playing_track.pack(anchor=tk.W)

        self.now_playing_emotion = tk.Label(
            info_frame,
            text="",
            font=('Arial', 9),
            bg='#1a1a1a',
            fg='#00ff00'
        )
        self.now_playing_emotion.pack(anchor=tk.W)

        self.now_playing_mood = tk.Label(
            info_frame,
            text="",
            font=('Arial', 9),
            bg='#1a1a1a',
            fg='#888888',
            wraplength=350,
            justify=tk.LEFT
        )
        self.now_playing_mood.pack(anchor=tk.W)

        # History section
        tk.Label(
            parent,
            text="PLAYBACK HISTORY",
            font=('Arial', 12, 'bold'),
            bg='#1a1a1a',
            fg='#888888',
            pady=10
        ).pack()

        # History list with scrollbar
        history_frame = tk.Frame(parent, bg='#1a1a1a')
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        history_scrollbar = tk.Scrollbar(history_frame)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_listbox = tk.Listbox(
            history_frame,
            font=('Courier', 8),
            bg='#0a0a0a',
            fg='#888888',
            selectbackground='#2b2b2b',
            yscrollcommand=history_scrollbar.set,
            borderwidth=0,
            highlightthickness=0
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.config(command=self.history_listbox.yview)

    def log_status(self, message):
        """Log a message to the status text widget"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)

    def create_placeholder_album_art(self):
        """Create a placeholder album art image"""
        # Create a 250x250 image with gradient background
        img = Image.new('RGB', (250, 250), color='#2b2b2b')

        # Draw a simple music note icon using PIL
        draw = ImageDraw.Draw(img)

        # Draw a vinyl record style design
        # Outer circle
        draw.ellipse([25, 25, 225, 225], fill='#1a1a1a', outline='#444444', width=3)
        # Inner circle (label)
        draw.ellipse([75, 75, 175, 175], fill='#2b2b2b', outline='#555555', width=2)
        # Center hole
        draw.ellipse([110, 110, 140, 140], fill='#0a0a0a', outline='#666666', width=2)

        # Draw some grooves
        for i in range(30, 75, 8):
            draw.ellipse([i, i, 250-i, 250-i], outline='#333333', width=1)

        # Add music note symbol
        try:
            # Try to use a larger font
            font = ImageFont.truetype("arial.ttf", 48)
        except:
            # Fallback to default font
            font = ImageFont.load_default()

        text = "♪"
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Center the text
        x = (250 - text_width) // 2
        y = (250 - text_height) // 2 - 10

        draw.text((x, y), text, fill='#00ff00', font=font)

        return ImageTk.PhotoImage(img)

    def extract_album_art(self, file_path):
        """Extract album art from audio file"""
        if not MUTAGEN_AVAILABLE:
            return self.create_placeholder_album_art()

        try:
            audio = MutagenFile(file_path)

            if audio is None:
                return self.create_placeholder_album_art()

            # Try different methods depending on file type
            artwork_data = None

            # MP3 files with ID3 tags
            if hasattr(audio, 'tags') and audio.tags:
                for tag in audio.tags.values():
                    if isinstance(tag, APIC):
                        artwork_data = tag.data
                        break

            # FLAC files
            if artwork_data is None and hasattr(audio, 'pictures') and audio.pictures:
                artwork_data = audio.pictures[0].data

            if artwork_data:
                # Convert to PIL Image
                image = Image.open(BytesIO(artwork_data))
                # Resize to 250x250
                image = image.resize((250, 250), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(image)

        except Exception as e:
            print(f"Could not extract album art: {e}")

        # Return placeholder if no album art found
        return self.create_placeholder_album_art()

    def update_now_playing(self, track_info, emotion):
        """Update the now playing display"""
        filename = os.path.basename(track_info['path'])

        # Update labels
        self.now_playing_track.config(text=filename)
        self.now_playing_emotion.config(text=f"😊 Face Mood: {emotion}")
        self.now_playing_mood.config(text=f"🎵 Music Mood: {track_info['mood']}")

        # Extract and display album art (always returns an image, placeholder if needed)
        album_art = self.extract_album_art(track_info['path'])
        self.album_art_label.config(image=album_art, text='')
        self.album_art_label.image = album_art  # Keep a reference

    def add_to_history(self, track_info, emotion):
        """Add a track to the playback history"""
        filename = os.path.basename(track_info['path'])
        history_entry = f"{emotion:8} | {track_info['mood']:20} | {filename}"

        # Add to history list
        self.playback_history.append({
            'track': filename,
            'emotion': emotion,
            'mood': track_info['mood'],
            'timestamp': time.strftime('%H:%M:%S')
        })

        # Update history listbox
        self.history_listbox.insert(0, history_entry)

    def get_smoothed_emotion(self):
        """Get smoothed emotion using mode of recent detections to reduce flickering"""
        if len(self.mood_history) < 5:  # Need at least 5 samples
            return self.current_emotion

        try:
            # Use mode (most common) of recent emotions
            smoothed = mode(self.mood_history)
            return smoothed
        except StatisticsError:
            # If no clear mode (tie), use most recent
            return self.mood_history[-1] if self.mood_history else self.current_emotion

    def detect_emotion(self, frame):
        """Detect emotion from a video frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(64, 64)
        )

        emotion = None

        for (x, y, w, h) in faces:
            # Extract face ROI
            roi_gray = gray[y:y+h, x:x+w]

            # Resize to model input size (64x64)
            roi_gray = cv2.resize(roi_gray, (64, 64))

            # Normalize pixel values [0, 1]
            roi = roi_gray.astype("float") / 255.0

            # Add dimensions for model input: (batch, height, width, channels)
            roi = np.expand_dims(roi, axis=0)
            roi = np.expand_dims(roi, axis=-1)

            # Get predictions
            preds = self.model.predict(roi, verbose=0)[0]
            emotion = self.emotions[np.argmax(preds)]
            confidence = np.max(preds)

            # Draw rectangle and label on frame
            color = (0, 255, 0) if confidence > 0.5 else (0, 255, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

            label = f"{emotion} ({confidence:.2f})"
            cv2.putText(frame, label, (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # Only use the first detected face
            break

        return frame, emotion

    def find_matching_tracks(self, emotion, max_results=10, exclude_recent=True):
        """Find tracks matching the detected emotion"""
        if emotion not in self.EMOTION_TO_MUSIC_MOOD:
            return []

        mood_config = self.EMOTION_TO_MUSIC_MOOD[emotion]
        target_moods = mood_config['moods']
        energy_min, energy_max = mood_config['energy_range']
        tempo_min, tempo_max = mood_config['tempo_range']

        matching_tracks = []

        for file_path, track_info in self.music_cache.items():
            # Check if file exists
            if not os.path.exists(file_path):
                continue

            # Skip recently played tracks
            if exclude_recent and file_path in self.used_tracks:
                continue

            mood = track_info.get('mood', '')
            energy = track_info.get('energy', 0.5)
            tempo = track_info.get('tempo', 100)

            # Score the track based on multiple factors
            score = 0

            # Mood match (exact or partial)
            for target_mood in target_moods:
                if target_mood.lower() in mood.lower() or mood.lower() in target_mood.lower():
                    score += 10
                    break

            # Energy range match
            if energy_min <= energy <= energy_max:
                score += 5

            # Tempo range match
            if tempo_min <= tempo <= tempo_max:
                score += 5

            # Add some randomness to avoid always playing the same songs
            score += random.uniform(0, 3)

            if score > 5:  # Minimum threshold
                matching_tracks.append({
                    'path': file_path,
                    'mood': mood,
                    'tempo': tempo,
                    'energy': energy,
                    'key': track_info.get('key', 'Unknown'),
                    'score': score
                })

        # Sort by score and return top results
        matching_tracks.sort(key=lambda x: x['score'], reverse=True)
        return matching_tracks[:max_results]

    def start_continuous_playback(self):
        """Start continuous mood-based playback"""
        if not self.smoothed_emotion and not self.current_emotion:
            messagebox.showwarning("No Emotion", "No emotion detected yet. Please wait...")
            return

        if self.is_playing:
            return

        self.is_playing = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.skip_button.config(state=tk.NORMAL)
        self.log_status("\n▶ Starting continuous mood-based playback...")

        # Start playback thread
        self.playback_thread = threading.Thread(target=self.continuous_playback_loop, daemon=True)
        self.playback_thread.start()

    def stop_continuous_playback(self):
        """Stop continuous playback"""
        if not self.is_playing:
            return

        self.is_playing = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.skip_button.config(state=tk.DISABLED)
        self.log_status("⏹ Stopping playback...")

        # Stop pygame music
        try:
            pygame.mixer.music.stop()
        except:
            pass

        # Kill any currently playing track process (fallback)
        if self.current_track_process:
            try:
                self.current_track_process.terminate()
            except:
                pass

    def skip_track(self):
        """Skip the currently playing track"""
        if not self.is_playing:
            return

        self.skip_current_track = True
        self.log_status("⏭ Skipping track...")

        # Stop the current track immediately
        try:
            pygame.mixer.music.stop()
        except:
            pass

    def continuous_playback_loop(self):
        """Main loop for continuous playback"""
        while self.is_playing:
            # Get current smoothed emotion
            emotion = self.smoothed_emotion or self.current_emotion

            if not emotion:
                time.sleep(1)
                continue

            # Find matching tracks
            matching_tracks = self.find_matching_tracks(emotion, max_results=20)

            if not matching_tracks:
                self.log_status(f"No matching tracks for {emotion}, waiting...")
                time.sleep(5)
                continue

            # Pick a track from top matches
            track = random.choice(matching_tracks[:5])
            self.used_tracks.append(track['path'])

            # Update now playing display
            self.update_now_playing(track, emotion)

            # Add to history
            self.add_to_history(track, emotion)

            # Log track info
            self.log_status(f"\n🎵 Now Playing ({emotion}):")
            self.log_status(f"  {os.path.basename(track['path'])}")
            self.log_status(f"  Mood: {track['mood']} | Energy: {track['energy']:.2f} | Tempo: {track['tempo']:.0f} BPM")

            # Play the track and wait for it to finish
            self.play_and_wait(track['path'])

            # Small gap between tracks
            if self.is_playing:
                time.sleep(0.5)

    def play_and_wait(self, file_path):
        """Play an audio file using pygame and wait for it to complete"""
        try:
            # Reset skip flag
            self.skip_current_track = False

            # Load and play the music file with pygame
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

            # Wait until the music finishes playing or skip is requested
            while pygame.mixer.music.get_busy() and self.is_playing and not self.skip_current_track:
                time.sleep(0.1)  # Check every 100ms

            # If stopped manually or skipped, stop the music
            if not self.is_playing or self.skip_current_track:
                pygame.mixer.music.stop()

        except Exception as e:
            self.log_status(f"Error playing file: {e}")
            # If pygame fails, try fallback to system player
            try:
                if sys.platform == 'win32':
                    os.startfile(file_path)
                elif sys.platform == 'darwin':
                    subprocess.call(['open', file_path])
                else:
                    subprocess.call(['xdg-open', file_path])
            except:
                pass


    def update_video_feed(self):
        """Update the video feed with emotion detection"""
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)

            if not self.cap.isOpened():
                messagebox.showerror("Camera Error", "Could not open webcam")
                self.quit_app()
                return

        ret, frame = self.cap.read()

        if ret:
            # Detect emotion
            frame, emotion = self.detect_emotion(frame)

            if emotion:
                self.current_emotion = emotion
                # Add to mood history for smoothing
                self.mood_history.append(emotion)
                # Update smoothed emotion
                self.smoothed_emotion = self.get_smoothed_emotion()
                # Display smoothed emotion
                self.emotion_label.config(text=f"{self.smoothed_emotion} (raw: {emotion})")

            # Convert frame to PhotoImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        # Schedule next update
        if self.video_running:
            self.root.after(10, self.update_video_feed)

    def quit_app(self):
        """Clean up and quit the application"""
        # Stop playback first
        if self.is_playing:
            self.stop_continuous_playback()

        self.video_running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.quit()
        self.root.destroy()

    def run(self):
        """Run the application"""
        # Start video feed
        self.update_video_feed()

        # Start GUI main loop
        self.root.mainloop()


def main():
    """Main entry point"""
    print("=" * 70)
    print("Music Recommendation Using Facial Expressions - Local Library Edition")
    print("=" * 70)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Facial Expression Based Local Music Player')
    parser.add_argument('--cache-path', type=str, 
                        help='Path to the music cache file (default: .mood_cache.json in script directory)')
    parser.add_argument('--model-path', type=str,
                        help='Path to the emotion detection model (default: in code/model subdirectory)')
    parser.add_argument('--music-folder', type=str,
                        help='Path to music folder for cache computation (optional)')
    parser.add_argument('--compute', action='store_true',
                        help='Compute music cache from specified music folder')
    
    args = parser.parse_args()

    # Set up paths relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_cache_path = os.path.join(script_dir, ".mood_cache.json")
    
    # Adjust model path based on script location
    # If script is in code/new_models, adjust path accordingly
    if "code" in script_dir and "new_models" in script_dir:
        # Script is in code/new_models, so model is up one directory and into code/model
        default_model_path = os.path.join(script_dir, "..", "..", "code", "model", "fer2013_mini_XCEPTION.102-0.66.hdf5")
    else:
        # Script is in root or elsewhere
        default_model_path = os.path.join(script_dir, "code", "model", "fer2013_mini_XCEPTION.102-0.66.hdf5")
    
    # Normalize the path to resolve .. components
    default_model_path = os.path.normpath(default_model_path)
    
    # Use provided paths or defaults
    cache_path = args.cache_path or default_cache_path
    model_path = args.model_path or default_model_path

    # If --compute flag is used, compute the cache first
    if args.compute:
        if not args.music_folder:
            print("\nERROR: --music-folder is required when using --compute")
            sys.exit(1)
            
        if not os.path.exists(args.music_folder) or not os.path.isdir(args.music_folder):
            print(f"\nERROR: Music folder does not exist: {args.music_folder}")
            sys.exit(1)
            
        # Compute cache in a separate function call
        compute_cache_standalone(args.music_folder, cache_path)
        print(f"\nCache computed successfully at: {cache_path}")
        return

    # Check for model file
    if not os.path.exists(model_path):
        print(f"\nERROR: Model file not found at: {model_path}")
        print("Please ensure the emotion detection model exists at this location.")
        print("You can download it from the original repository.")
        sys.exit(1)

    # Create and run app
    app = LocalMusicMoodPlayer(cache_path=cache_path, model_path=model_path, music_folder=args.music_folder)
    app.run()


def compute_cache_standalone(music_folder, cache_path):
    """Standalone function to compute cache without GUI"""
    if not MOOD_DETECTOR_AVAILABLE:
        print("ERROR: mood_detector library not found.")
        print("Please install it with: pip install git+https://github.com/wedsmoker/Mood-Detector.git")
        sys.exit(1)

    # Supported audio formats
    supported_formats = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma', '.m4p'}
    
    # Find all audio files recursively
    all_audio_files = []
    for root, dirs, files in os.walk(music_folder):
        for file in files:
            if Path(file).suffix.lower() in supported_formats:
                all_audio_files.append(os.path.join(root, file))
    
    if not all_audio_files:
        print(f"No supported audio files found in {music_folder}")
        return

    print(f"Found {len(all_audio_files)} audio files to analyze")
    
    # Load existing cache if it exists
    existing_cache = {}
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            existing_cache = json.load(f)
    
    # Process each file
    cache = {}
    analyzed_count = 0
    
    for i, file_path in enumerate(all_audio_files):
        try:
            print(f"Analyzing {i+1}/{len(all_audio_files)}: {os.path.basename(file_path)}")
            
            # Check if file has been modified since last cache
            mtime = os.path.getmtime(file_path)
            
            # Skip if already in cache and unchanged
            if file_path in existing_cache:
                cached = existing_cache[file_path]
                if cached.get("mtime", 0) == mtime and "mood" in cached:
                    cache[file_path] = cached
                    continue
            
            # Analyze the audio file
            result = analyze_audio(file_path)
            cache[file_path] = {
                "mood": result.mood,
                "tempo": result.tempo,
                "energy": result.energy,
                "key": result.key,
                "mtime": mtime
            }
            analyzed_count += 1
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            # Keep old cache entry if exists, else skip
            if file_path in existing_cache:
                cache[file_path] = existing_cache[file_path]
    
    # Save the cache
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)  # Ensure directory exists
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2)
    
    print(f"\nCache computation completed!")
    print(f"Analyzed {analyzed_count} new files.")
    print(f"Total: {len(cache)} tracks in cache.")
    print(f"Cache saved to: {cache_path}")


if __name__ == "__main__":
    main()
