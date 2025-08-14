"""
Spotify Manager Module
Gère l'authentification, la recherche et la création de playlists sur Spotify
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
import time


class SpotifyManager:
    def __init__(self):
        """Initialise le gestionnaire Spotify avec les credentials."""
        load_dotenv()
        
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')
        
        if not self.client_id or not self.client_secret:
            raise ValueError(
                "❌ Variables d'environnement manquantes!\n"
                "Assurez-vous d'avoir SPOTIFY_CLIENT_ID et SPOTIFY_CLIENT_SECRET dans votre fichier .env"
            )
        
        # Scopes nécessaires pour créer et modifier des playlists
        self.scope = "playlist-modify-public playlist-modify-private user-library-read"
        
        # Initialiser l'authentification
        self.auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_path=".spotify_cache",
            open_browser=True,
            show_dialog=True
        )
        
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)
        self.user_id = None
        
    def authenticate(self) -> bool:
        """
        Authentifie l'utilisateur Spotify.
        
        Returns:
            True si l'authentification réussit, False sinon
        """
        try:
            # Obtenir les infos de l'utilisateur
            user_info = self.sp.current_user()
            if user_info:
                self.user_id = user_info['id']
                print(f"✅ Authentifié en tant que: {user_info['display_name']} ({self.user_id})")
                return True
            else:
                print("❌ Impossible d'obtenir les informations utilisateur")
                return False
        except Exception as e:
            print(f"❌ Erreur d'authentification Spotify: {e}")
            return False
    
    def search_track(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Recherche des pistes sur Spotify.
        
        Args:
            query: Requête de recherche
            limit: Nombre maximum de résultats
            
        Returns:
            Liste des pistes trouvées
        """
        try:
            results = self.sp.search(q=query, type='track', limit=limit)
            tracks = []
            
            if results and 'tracks' in results and results['tracks']:
                for track in results['tracks']['items']:
                    track_info = {
                        'id': track['id'],
                        'name': track['name'],
                        'artists': [artist['name'] for artist in track['artists']],
                        'album': track['album']['name'],
                        'uri': track['uri'],
                        'popularity': track['popularity'],
                        'duration_ms': track['duration_ms'],
                        'preview_url': track['preview_url']
                    }
                    tracks.append(track_info)
            
            return tracks
        except Exception as e:
            print(f"❌ Erreur lors de la recherche: {e}")
            return []
    
    def find_best_match(self, search_queries: List[str], original_title: str) -> Optional[Dict]:
        """
        Trouve la meilleure correspondance pour une liste de requêtes.
        
        Args:
            search_queries: Liste des requêtes de recherche
            original_title: Titre original pour comparaison
            
        Returns:
            Meilleure piste trouvée ou None
        """
        all_results = []
        
        for query in search_queries:
            tracks = self.search_track(query, limit=5)
            for track in tracks:
                # Calculer un score de pertinence
                score = self._calculate_relevance_score(track, original_title, query)
                track['relevance_score'] = score
                all_results.append(track)
        
        if not all_results:
            return None
        
        # Trier par score de pertinence (descendant)
        all_results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Retourner le meilleur résultat si le score est suffisant
        best_match = all_results[0]
        if best_match['relevance_score'] > 0.3:  # Seuil de confiance
            return best_match
        
        return None
    
    def _calculate_relevance_score(self, track: Dict, original_title: str, query: str) -> float:
        """
        Calcule un score de pertinence pour une piste.
        
        Args:
            track: Informations de la piste Spotify
            original_title: Titre original YouTube
            query: Requête de recherche utilisée
            
        Returns:
            Score de pertinence entre 0 et 1
        """
        score = 0.0
        
        # Score basé sur la popularité (20% du score)
        score += (track['popularity'] / 100) * 0.2
        
        # Score basé sur la correspondance du titre (40% du score)
        title_similarity = self._calculate_similarity(
            track['name'].lower(), 
            original_title.lower()
        )
        score += title_similarity * 0.4
        
        # Score basé sur la correspondance des artistes (40% du score)
        artists_text = ' '.join(track['artists']).lower()
        artist_similarity = self._calculate_similarity(
            artists_text, 
            original_title.lower()
        )
        score += artist_similarity * 0.4
        
        return min(score, 1.0)
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calcule la similarité entre deux textes (simple).
        
        Args:
            text1: Premier texte
            text2: Deuxième texte
            
        Returns:
            Score de similarité entre 0 et 1
        """
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def create_playlist(self, name: str, description: str = "", public: bool = True) -> Optional[str]:
        """
        Crée une nouvelle playlist Spotify.
        
        Args:
            name: Nom de la playlist
            description: Description de la playlist
            public: Si la playlist doit être publique
            
        Returns:
            ID de la playlist créée ou None
        """
        try:
            if not self.user_id:
                if not self.authenticate():
                    return None
            
            playlist = self.sp.user_playlist_create(
                user=self.user_id,
                name=name,
                public=public,
                description=description
            )
            
            if playlist:
                print(f"✅ Playlist créée: {name}")
                return playlist['id']
            else:
                print(f"❌ Erreur lors de la création de la playlist")
                return None
        except Exception as e:
            print(f"❌ Erreur lors de la création de la playlist: {e}")
            return None
    
    def add_tracks_to_playlist(self, playlist_id: str, track_uris: List[str]) -> bool:
        """
        Ajoute des pistes à une playlist.
        
        Args:
            playlist_id: ID de la playlist
            track_uris: Liste des URIs des pistes
            
        Returns:
            True si succès, False sinon
        """
        try:
            # Spotify limite à 100 pistes par requête
            batch_size = 100
            
            for i in range(0, len(track_uris), batch_size):
                batch = track_uris[i:i + batch_size]
                self.sp.playlist_add_items(playlist_id, batch)
                
                # Petite pause pour éviter les rate limits
                if len(track_uris) > batch_size:
                    time.sleep(0.1)
            
            print(f"✅ {len(track_uris)} pistes ajoutées à la playlist")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout des pistes: {e}")
            return False
    
    def get_playlist_url(self, playlist_id: str) -> str:
        """
        Génère l'URL publique d'une playlist.
        
        Args:
            playlist_id: ID de la playlist
            
        Returns:
            URL de la playlist
        """
        return f"https://open.spotify.com/playlist/{playlist_id}"
    
    def playlist_exists(self, name: str) -> Optional[str]:
        """
        Vérifie si une playlist avec ce nom existe déjà.
        
        Args:
            name: Nom de la playlist
            
        Returns:
            ID de la playlist si elle existe, None sinon
        """
        try:
            if not self.user_id:
                if not self.authenticate():
                    return None
            
            playlists = self.sp.user_playlists(self.user_id, limit=50)
            
            if playlists and 'items' in playlists:
                for playlist in playlists['items']:
                    if playlist['name'].lower() == name.lower():
                        return playlist['id']
            
            return None
        except Exception as e:
            print(f"❌ Erreur lors de la vérification des playlists: {e}")
            return None


def main():
    """Test du module Spotify."""
    try:
        # Initialiser le gestionnaire
        spotify = SpotifyManager()
        
        # Test d'authentification
        if not spotify.authenticate():
            print("❌ Échec de l'authentification")
            return
        
        # Test de recherche
        print("\n🔍 Test de recherche:")
        queries = ["Rema Calm Down", "Burna Boy Last Last"]
        
        for query in queries:
            print(f"\nRecherche: {query}")
            tracks = spotify.search_track(query, limit=3)
            
            for i, track in enumerate(tracks, 1):
                artists = ', '.join(track['artists'])
                print(f"  {i}. {track['name']} - {artists}")
        
        print("\n✅ Test terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    main()
