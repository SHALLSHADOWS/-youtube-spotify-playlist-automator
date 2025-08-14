#!/usr/bin/env python3
"""
🎵 YouTube Mix → Spotify Playlist Automator

Script principal pour automatiser le transfert de playlists YouTube vers Spotify.

Usage:
    python yt2spotify.py --youtube "URL" --name "Playlist Name" [options]

Auteur: Votre nom
Date: 2025
"""

import argparse
import sys
import os
from datetime import datetime
from typing import List, Dict

# Ajouter le dossier src au path pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from youtube_extractor import YouTubeExtractor
from title_cleaner import TitleCleaner
from spotify_manager import SpotifyManager
from playlist_naming import PlaylistNamingEngine


class PlaylistTransferReport:
    """Gestionnaire de rapport de transfert."""
    
    def __init__(self):
        self.found_tracks: List[Dict] = []
        self.not_found_tracks: List[str] = []
        self.total_youtube_videos = 0
        self.processing_time = 0.0
        self.playlist_url = ""
        self.playlist_name = ""
    
    def add_found_track(self, youtube_title: str, spotify_track: Dict):
        """Ajoute une piste trouvée au rapport."""
        self.found_tracks.append({
            'youtube_title': youtube_title,
            'spotify_name': spotify_track['name'],
            'spotify_artists': ', '.join(spotify_track['artists']),
            'spotify_id': spotify_track['id'],
            'relevance_score': spotify_track.get('relevance_score', 0)
        })
    
    def add_not_found_track(self, youtube_title: str):
        """Ajoute une piste non trouvée au rapport."""
        self.not_found_tracks.append(youtube_title)
    
    def print_summary(self):
        """Affiche un résumé du transfert."""
        print("\n" + "="*60)
        print("📊 RÉSUMÉ DU TRANSFERT")
        print("="*60)
        print(f"🎵 Vidéos YouTube analysées: {self.total_youtube_videos}")
        print(f"✅ Pistes trouvées sur Spotify: {len(self.found_tracks)}")
        print(f"❌ Pistes non trouvées: {len(self.not_found_tracks)}")
        print(f"📈 Taux de réussite: {len(self.found_tracks)/max(self.total_youtube_videos, 1)*100:.1f}%")
        
        if self.playlist_url:
            print(f"🎯 Playlist créée: {self.playlist_url}")
        
        print(f"⏱️  Temps de traitement: {self.processing_time:.1f}s")
        print("="*60)
    
    def save_to_file(self, filename: str | None = None):
        """Sauvegarde le rapport détaillé dans un fichier."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/rapport_transfert_{timestamp}.txt"
        
        # Créer le dossier reports s'il n'existe pas
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"🎵 YouTube → Spotify Playlist Transfer Report\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Playlist: {self.playlist_name}\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"📊 SUMMARY:\n")
            f.write(f"  - YouTube videos analyzed: {self.total_youtube_videos}\n")
            f.write(f"  - Tracks found on Spotify: {len(self.found_tracks)}\n")
            f.write(f"  - Tracks not found: {len(self.not_found_tracks)}\n")
            f.write(f"  - Success rate: {len(self.found_tracks)/max(self.total_youtube_videos, 1)*100:.1f}%\n")
            f.write(f"  - Playlist URL: {self.playlist_url}\n\n")
            
            if self.found_tracks:
                f.write("✅ FOUND TRACKS:\n")
                f.write("-" * 40 + "\n")
                for i, track in enumerate(self.found_tracks, 1):
                    f.write(f"{i:2d}. {track['youtube_title']}\n")
                    f.write(f"    → {track['spotify_name']} - {track['spotify_artists']}\n")
                    f.write(f"    Score: {track['relevance_score']:.2f}\n\n")
            
            if self.not_found_tracks:
                f.write("❌ NOT FOUND TRACKS:\n")
                f.write("-" * 40 + "\n")
                for i, track in enumerate(self.not_found_tracks, 1):
                    f.write(f"{i:2d}. {track}\n")
        
        print(f"📄 Rapport sauvegardé: {filename}")


def setup_argument_parser():
    """Configure l'analyseur d'arguments en ligne de commande."""
    parser = argparse.ArgumentParser(
        description="🎵 Transfère une playlist YouTube vers Spotify automatiquement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python yt2spotify.py --youtube "https://youtube.com/playlist?list=XXX" --name "Afrobeats Mix"
  python yt2spotify.py -y "URL" -n "Ma Playlist" -d "Description" --private
  python yt2spotify.py -y "URL"  # Nom automatique basé sur l'analyse des titres
        """
    )
    
    parser.add_argument(
        '--youtube', '-y',
        required=True,
        help='URL de la playlist ou mix YouTube'
    )
    
    parser.add_argument(
        '--name', '-n',
        required=False,
        help='Nom de la playlist Spotify (optionnel, nom automatique si non spécifié)'
    )
    
    parser.add_argument(
        '--description', '-d',
        default='',
        help='Description de la playlist Spotify (optionnel)'
    )
    
    parser.add_argument(
        '--private',
        action='store_true',
        help='Créer une playlist privée (par défaut: publique)'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Forcer la création même si une playlist du même nom existe'
    )
    
    parser.add_argument(
        '--report-only',
        action='store_true',
        help='Générer seulement un rapport sans créer la playlist'
    )
    
    parser.add_argument(
        '--max-tracks',
        type=int,
        default=0,
        help='Limite le nombre de pistes à traiter (0 = toutes)'
    )
    
    return parser


def main():
    """Fonction principale du script."""
    # Configuration des arguments
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Initialisation du rapport
    report = PlaylistTransferReport()
    start_time = datetime.now()
    
    print("🎵 YouTube Mix → Spotify Playlist Automator")
    print("="*50)
    
    try:
        # 1. Extraction YouTube
        print(f"📥 Extraction de la playlist YouTube...")
        youtube_extractor = YouTubeExtractor()
        
        # Vérifier l'URL
        if not youtube_extractor.is_valid_youtube_url(args.youtube):
            print("❌ URL YouTube invalide!")
            return 1
        
        # Extraire les vidéos
        videos = youtube_extractor.extract_videos(args.youtube)
        if not videos:
            print("❌ Aucune vidéo trouvée dans la playlist!")
            return 1
        
        # Limiter le nombre de pistes si demandé
        if args.max_tracks > 0:
            videos = videos[:args.max_tracks]
            print(f"⚠️  Limitation à {args.max_tracks} pistes")
        
        report.total_youtube_videos = len(videos)
        print(f"✅ {len(videos)} vidéos extraites")
        
        # 2. Nettoyage et recherche
        print(f"\n🧹 Nettoyage des titres et recherche Spotify...")
        title_cleaner = TitleCleaner()
        spotify_manager = SpotifyManager()
        
        # Authentification Spotify
        if not spotify_manager.authenticate():
            print("❌ Échec de l'authentification Spotify!")
            return 1
        
        # Recherche des pistes
        found_tracks = []
        progress_count = 0
        
        for video in videos:
            progress_count += 1
            title = video['title']
            
            print(f"🔍 [{progress_count}/{len(videos)}] {title[:60]}...")
            
            # Générer les requêtes de recherche
            search_queries = title_cleaner.create_search_queries(title)
            
            # Chercher sur Spotify
            best_match = spotify_manager.find_best_match(search_queries, title)
            
            if best_match:
                found_tracks.append(best_match)
                report.add_found_track(title, best_match)
                artists = ', '.join(best_match['artists'])
                print(f"✅ → {best_match['name']} - {artists}")
            else:
                report.add_not_found_track(title)
                print(f"❌ → Non trouvé")
        
        # 2.5. Génération automatique du nom de playlist si nécessaire
        playlist_name = args.name
        playlist_description = args.description
        
        if not playlist_name and found_tracks:
            print(f"\n🧠 Génération automatique du nom de playlist...")
            naming_engine = PlaylistNamingEngine()
            
            # Extraire les titres pour l'analyse
            track_titles = [f"{track['name']} - {', '.join(track['artists'])}" for track in found_tracks]
            playlist_name, auto_description = naming_engine.create_playlist_identity(track_titles)
            print(f"🎯 Nom généré: '{playlist_name}'")
            
            # Utiliser la description automatique si aucune n'est fournie
            if not playlist_description:
                playlist_description = auto_description
                print(f"📝 Description générée: '{playlist_description[:100]}{'...' if len(playlist_description) > 100 else ''}'")
        
        # Définir le nom final pour le rapport
        if not playlist_name:
            playlist_name = f"Playlist YouTube {datetime.now().strftime('%d-%m-%Y')}"
        
        report.playlist_name = playlist_name
        
        # 3. Création de la playlist (si pas en mode rapport seulement)
        playlist_id = None
        if not args.report_only and found_tracks:
            print(f"\n🎯 Création de la playlist Spotify...")
            
            # Vérifier si la playlist existe déjà
            existing_playlist = spotify_manager.playlist_exists(playlist_name)
            if existing_playlist and not args.force:
                print(f"⚠️  Une playlist '{playlist_name}' existe déjà!")
                print("Utilisez --force pour forcer la création ou choisissez un autre nom.")
                return 1
            
            # Créer la playlist
            final_description = playlist_description or f"Importée depuis YouTube le {datetime.now().strftime('%d/%m/%Y')}"
            playlist_id = spotify_manager.create_playlist(
                name=playlist_name,
                description=final_description,
                public=not args.private
            )
            
            if playlist_id:
                # Ajouter les pistes
                track_uris = [track['uri'] for track in found_tracks]
                if spotify_manager.add_tracks_to_playlist(playlist_id, track_uris):
                    report.playlist_url = spotify_manager.get_playlist_url(playlist_id)
                    print(f"🎉 Playlist créée avec succès!")
                else:
                    print("❌ Erreur lors de l'ajout des pistes")
            else:
                print("❌ Erreur lors de la création de la playlist")
        
        # 4. Génération du rapport
        end_time = datetime.now()
        report.processing_time = (end_time - start_time).total_seconds()
        
        report.print_summary()
        report.save_to_file()
        
        # Code de retour
        if len(found_tracks) == 0:
            return 1  # Aucune piste trouvée
        elif len(found_tracks) < len(videos) * 0.5:
            return 2  # Moins de 50% de réussite
        else:
            return 0  # Succès
            
    except KeyboardInterrupt:
        print("\n⚠️  Transfert interrompu par l'utilisateur")
        return 130
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
