"""
YouTube Extractor Module
Extrait les vidéos et métadonnées depuis YouTube en utilisant yt-dlp
"""

import yt_dlp
import re
from typing import List, Dict, Optional
from urllib.parse import urlparse, parse_qs


class YouTubeExtractor:
    def __init__(self):
        """Initialise l'extracteur YouTube avec les options yt-dlp."""
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,  # Ne télécharge pas, juste les métadonnées
            'ignoreerrors': True,
        }
    
    def extract_playlist_info(self, url: str) -> Optional[Dict]:
        """
        Extrait les informations de base d'une playlist/mix YouTube.
        
        Args:
            url: URL de la playlist ou mix YouTube
            
        Returns:
            Dict avec les infos de la playlist ou None si erreur
        """
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if info is None:
                    print(f"❌ Impossible d'extraire les informations depuis {url}")
                    return None
                
                return {
                    'title': info.get('title', 'Playlist sans nom'),
                    'id': info.get('id'),
                    'uploader': info.get('uploader'),
                    'description': info.get('description', ''),
                    'entries': info.get('entries', [])
                }
        except Exception as e:
            print(f"❌ Erreur lors de l'extraction de la playlist: {e}")
            return None
    
    def extract_videos(self, url: str) -> List[Dict]:
        """
        Extrait toutes les vidéos d'une playlist/mix YouTube.
        
        Args:
            url: URL de la playlist ou mix YouTube
            
        Returns:
            Liste de dictionnaires contenant les infos des vidéos
        """
        playlist_info = self.extract_playlist_info(url)
        if not playlist_info:
            return []
        
        videos = []
        entries = playlist_info.get('entries', [])
        
        print(f"🎵 {len(entries)} vidéos trouvées dans la playlist")
        
        for entry in entries:
            if entry is None:  # Vidéo indisponible
                continue
                
            video_info = {
                'title': entry.get('title', 'Titre inconnu'),
                'id': entry.get('id'),
                'duration': entry.get('duration'),
                'uploader': entry.get('uploader'),
                'url': f"https://www.youtube.com/watch?v={entry.get('id')}" if entry.get('id') else None
            }
            
            # Filtrer les vidéos trop courtes (probablement des intros/outros)
            if video_info['duration'] and video_info['duration'] < 30:
                continue
                
            videos.append(video_info)
        
        return videos
    
    def is_valid_youtube_url(self, url: str) -> bool:
        """
        Vérifie si l'URL est une URL YouTube valide.
        
        Args:
            url: URL à vérifier
            
        Returns:
            True si l'URL est valide, False sinon
        """
        youtube_patterns = [
            r'youtube\.com/playlist',
            r'youtube\.com/watch.*list=',
            r'youtu\.be/.*list=',
            r'music\.youtube\.com/playlist',
            r'music\.youtube\.com/watch.*list='
        ]
        
        return any(re.search(pattern, url) for pattern in youtube_patterns)
    
    def extract_playlist_id(self, url: str) -> Optional[str]:
        """
        Extrait l'ID de la playlist depuis l'URL.
        
        Args:
            url: URL YouTube
            
        Returns:
            ID de la playlist ou None
        """
        try:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            return query_params.get('list', [None])[0]
        except:
            return None


def main():
    """Test du module d'extraction YouTube."""
    extractor = YouTubeExtractor()
    
    # URL de test (remplacez par une vraie URL pour tester)
    test_url = "https://www.youtube.com/playlist?list=PLrAUdmqUc2leFVt7hqRXfCqaZQGUbWjKK"
    
    if extractor.is_valid_youtube_url(test_url):
        videos = extractor.extract_videos(test_url)
        print(f"Trouvé {len(videos)} vidéos:")
        for i, video in enumerate(videos[:5], 1):  # Affiche les 5 premières
            print(f"{i}. {video['title']} ({video['duration']}s)")
    else:
        print("URL YouTube invalide")


if __name__ == "__main__":
    main()
