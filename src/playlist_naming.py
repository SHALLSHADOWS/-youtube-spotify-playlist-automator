#!/usr/bin/env python3
"""
Algorithme sophistiqué de génération automatique de noms et descriptions de playlists.
Analyse les titres pour créer des noms contextuels et des descriptions engageantes.
"""

import re
from typing import List, Dict, Tuple, Optional
from collections import Counter
import random

class PlaylistNamingEngine:
    """
    Moteur intelligent de nommage de playlists basé sur l'analyse des contenus.
    """
    
    def __init__(self):
        # Base de données des genres musicaux
        self.genre_keywords = {
            'afrobeat': ['afrobeat', 'afrobeats', 'naija', 'lagos', 'nigeria', 'ghana', 'benin'],
            'hip_hop': ['hip hop', 'rap', 'trap', 'drill', 'freestyle'],
            'rnb': ['r&b', 'rnb', 'soul', 'smooth', 'love', 'romance'],
            'dancehall': ['dancehall', 'reggae', 'jamaica', 'caribbean'],
            'pop': ['pop', 'mainstream', 'radio', 'chart'],
            'electronic': ['electronic', 'edm', 'house', 'techno', 'remix'],
            'french': ['french', 'français', 'clip officiel', 'feat tayc'],
            'amapiano': ['amapiano', 'piano', 'south africa', 'sa'],
        }
        
        # Mots-clés contextuels
        self.context_keywords = {
            'mix': ['mix', 'mixed', 'compilation'],
            'hits': ['hit', 'hits', 'best', 'top', 'greatest'],
            'new': ['new', 'latest', 'recent', '2024', '2025'],
            'official': ['official', 'music video', 'video'],
            'remix': ['remix', 'remaster', 'version'],
            'live': ['live', 'performance', 'concert'],
            'energy': ['fire', 'hot', 'banger', 'vibe', 'energy']
        }
        
        # Templates de noms créatifs
        self.name_templates = {
            'artist_focused': [
                "{main_artist} Essentials",
                "Best of {main_artist}",
                "{main_artist} Vibes",
                "The {main_artist} Collection",
                "{main_artist} Hits & More"
            ],
            'genre_focused': [
                "{genre} Bangers",
                "Pure {genre}",
                "{genre} Vibes",
                "Ultimate {genre} Mix",
                "{genre} Sessions",
                "Fresh {genre} Sounds"
            ],
            'mood_focused': [
                "Midnight Vibes",
                "Feel Good Playlist",
                "Energy Boost",
                "Chill Mode",
                "Party Starters",
                "Late Night Moods"
            ],
            'regional': [
                "African Heat",
                "Naija Mix",
                "French Touch",
                "Global Sounds",
                "World Vibes"
            ]
        }
        
        # Templates de descriptions
        self.description_templates = [
            "🎵 Une sélection soigneusement choisie de {genre} avec {main_artist} et plus. {track_count} titres pour {mood}.",
            "🔥 Les meilleurs sons {genre} du moment ! Featuring {top_artists} et d'autres talents. Perfect pour {context}.",
            "✨ Découvrez le meilleur du {genre} avec cette playlist de {track_count} titres. De {main_artist} aux nouveaux talents.",
            "🎯 Collection premium de {genre} - {track_count} tracks sélectionnées pour leur qualité et leur vibe unique.",
            "🌟 Votre dose quotidienne de {genre} ! {main_artist}, {second_artist} et plus dans une playlist de {track_count} titres."
        ]
    
    def analyze_tracks(self, track_titles: List[str]) -> Dict:
        """
        Analyse la liste des titres pour extraire les informations clés.
        
        Args:
            track_titles: Liste des titres de la playlist
            
        Returns:
            Dict avec les analyses (artistes, genres, contexte, etc.)
        """
        analysis = {
            'artists': [],
            'genres': [],
            'contexts': [],
            'keywords': [],
            'track_count': len(track_titles),
            'languages': []
        }
        
        all_text = ' '.join(track_titles).lower()
        
        # Extraire les artistes (premiers mots avant - ou feat)
        for title in track_titles:
            # Pattern: "Artiste - Titre" ou "Artiste feat. Autre"
            artist_match = re.match(r'^([^-]+?)(?:\s*[-–]|\s+feat\.|\s+ft\.)', title.strip())
            if artist_match:
                artist = artist_match.group(1).strip()
                # Nettoyer l'artiste
                artist = re.sub(r'\([^)]*\)|\[[^\]]*\]', '', artist).strip()
                if artist and len(artist) > 1:
                    analysis['artists'].append(artist)
        
        # Détecter les genres
        for genre, keywords in self.genre_keywords.items():
            score = sum(1 for keyword in keywords if keyword in all_text)
            if score > 0:
                analysis['genres'].append((genre, score))
        
        # Détecter le contexte
        for context, keywords in self.context_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                analysis['contexts'].append(context)
        
        # Compter les artistes les plus fréquents
        artist_counts = Counter(analysis['artists'])
        analysis['top_artists'] = artist_counts.most_common(5)
        
        # Trier les genres par score
        analysis['genres'].sort(key=lambda x: x[1], reverse=True)
        
        return analysis
    
    def generate_name(self, analysis: Dict) -> str:
        """
        Génère un nom de playlist basé sur l'analyse.
        
        Args:
            analysis: Résultats de l'analyse des titres
            
        Returns:
            Nom de playlist généré
        """
        top_artists = analysis['top_artists']
        genres = analysis['genres']
        contexts = analysis['contexts']
        
        # Déterminer la stratégie de nommage
        if top_artists and top_artists[0][1] >= 3:  # Artiste dominant
            main_artist = top_artists[0][0]
            template = random.choice(self.name_templates['artist_focused'])
            return template.format(main_artist=main_artist)
        
        elif genres and genres[0][1] >= 2:  # Genre dominant
            genre = genres[0][0]
            genre_name = self._get_genre_display_name(genre)
            template = random.choice(self.name_templates['genre_focused'])
            return template.format(genre=genre_name)
        
        elif 'french' in [g[0] for g in genres]:  # Contenu français
            return random.choice([
                "French Touch Mix",
                "Afrobeat Français",
                "Sons Francophones"
            ])
        
        elif 'afrobeat' in [g[0] for g in genres[:2]]:  # Afrobeat dominant
            return random.choice([
                "African Heat",
                "Naija Vibes",
                "Afrobeat Sessions",
                "Lagos Sounds"
            ])
        
        else:  # Fallback vers mood
            return random.choice(self.name_templates['mood_focused'])
    
    def generate_description(self, analysis: Dict, playlist_name: str) -> str:
        """
        Génère une description engageante pour la playlist.
        
        Args:
            analysis: Résultats de l'analyse
            playlist_name: Nom généré de la playlist
            
        Returns:
            Description de la playlist
        """
        track_count = analysis['track_count']
        top_artists = analysis['top_artists']
        genres = analysis['genres']
        
        # Préparer les variables pour le template
        main_artist = top_artists[0][0] if top_artists else "divers artistes"
        second_artist = top_artists[1][0] if len(top_artists) > 1 else "d'autres talents"
        
        genre = self._get_genre_display_name(genres[0][0]) if genres else "musique"
        
        # Top artistes pour la description
        if len(top_artists) >= 3:
            top_artists_str = f"{top_artists[0][0]}, {top_artists[1][0]}, {top_artists[2][0]}"
        elif len(top_artists) == 2:
            top_artists_str = f"{top_artists[0][0]} et {top_artists[1][0]}"
        elif len(top_artists) == 1:
            top_artists_str = top_artists[0][0]
        else:
            top_artists_str = "divers artistes"
        
        # Contexte et mood
        mood = self._determine_mood(analysis)
        context = self._determine_context(analysis)
        
        # Choisir un template et le remplir
        template = random.choice(self.description_templates)
        
        description = template.format(
            genre=genre,
            main_artist=main_artist,
            second_artist=second_artist,
            top_artists=top_artists_str,
            track_count=track_count,
            mood=mood,
            context=context,
            playlist_name=playlist_name
        )
        
        # Ajouter des émojis contextuels
        description += self._add_contextual_emojis(analysis)
        
        return description
    
    def _get_genre_display_name(self, genre: str) -> str:
        """Convertit le nom de genre interne en nom d'affichage."""
        display_names = {
            'afrobeat': 'Afrobeat',
            'hip_hop': 'Hip-Hop',
            'rnb': 'R&B',
            'dancehall': 'Dancehall',
            'pop': 'Pop',
            'electronic': 'Électronique',
            'french': 'Français',
            'amapiano': 'Amapiano'
        }
        return display_names.get(genre, genre.title())
    
    def _determine_mood(self, analysis: Dict) -> str:
        """Détermine le mood de la playlist."""
        contexts = analysis['contexts']
        
        if 'energy' in contexts or 'hits' in contexts:
            return "booster votre énergie"
        elif 'new' in contexts:
            return "découvrir les nouveautés"
        elif 'mix' in contexts:
            return "une ambiance parfaite"
        else:
            return "tous les moments"
    
    def _determine_context(self, analysis: Dict) -> str:
        """Détermine le contexte d'usage."""
        contexts = analysis['contexts']
        
        if 'mix' in contexts:
            return "un mix parfait"
        elif 'hits' in contexts:
            return "les plus grands hits"
        elif 'live' in contexts:
            return "des performances live"
        else:
            return "votre playlist idéale"
    
    def _add_contextual_emojis(self, analysis: Dict) -> str:
        """Ajoute des émojis contextuels à la description."""
        emojis = []
        
        genres = [g[0] for g in analysis['genres']]
        
        if 'afrobeat' in genres:
            emojis.extend(['🌍', '🔥', '🥁'])
        if 'french' in genres:
            emojis.extend(['🇫🇷', '✨'])
        if 'hip_hop' in genres:
            emojis.extend(['🎤', '💥'])
        if 'rnb' in genres:
            emojis.extend(['💖', '🌙'])
        
        if emojis:
            return f"\n\n{' '.join(emojis[:3])}"
        return ""
    
    def create_playlist_identity(self, track_titles: List[str]) -> Tuple[str, str]:
        """
        Crée une identité complète (nom + description) pour une playlist.
        
        Args:
            track_titles: Liste des titres de la playlist
            
        Returns:
            Tuple (nom, description)
        """
        if not track_titles:
            return "Mix Playlist", "Une playlist personnalisée 🎵"
        
        # Analyser les titres
        analysis = self.analyze_tracks(track_titles)
        
        # Générer nom et description
        name = self.generate_name(analysis)
        description = self.generate_description(analysis, name)
        
        return name, description


def main():
    """Test du moteur de nommage."""
    print("🧠 Test du moteur de nommage automatique")
    print("=" * 50)
    
    # Exemples de titres
    test_titles = [
        "Rema - DND (Official Music Video)",
        "Omah Lay - Understand (Official Music Video)",
        "Fireboy DML, Asake - Bandana (Official Video)",
        "Burna Boy - Common Person [Official Music Video]",
        "Asake - Joha (Official Video)",
        "Wizkid - Ghetto Love (Official Video)",
        "Tayc - Forévà (Visualizer)",
        "Asake & Tiakola - BADMAN GANGSTA"
    ]
    
    engine = PlaylistNamingEngine()
    
    name, description = engine.create_playlist_identity(test_titles)
    
    print(f"📝 Titres analysés: {len(test_titles)}")
    print(f"🎵 Nom généré: {name}")
    print(f"📄 Description:")
    print(f"   {description}")

if __name__ == "__main__":
    main()
