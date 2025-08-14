"""
Title Cleaner Module
Nettoie et normalise les titres des vidéos YouTube pour une meilleure correspondance Spotify
"""

import re
from typing import Tuple, Optional, List


class TitleCleaner:
    def __init__(self):
        """Initialise le nettoyeur de titres avec les patterns de nettoyage."""
        
        # Patterns à supprimer des titres
        self.remove_patterns = [
            # Vidéos officielles
            r'\(Official.*?\)',
            r'\[Official.*?\]',
            r'Official Video',
            r'Official Audio',
            r'Official Music Video',
            
            # Types de contenu
            r'\(.*?Video.*?\)',
            r'\[.*?Video.*?\]',
            r'\(.*?Audio.*?\)',
            r'\[.*?Audio.*?\]',
            r'\(Lyric.*?\)',
            r'\[Lyric.*?\]',
            r'\(Live.*?\)',
            r'\[Live.*?\]',
            
            # Qualité/Format
            r'\(HD\)',
            r'\[HD\]',
            r'\(4K\)',
            r'\[4K\]',
            r'\(1080p\)',
            r'\[1080p\]',
            
            # Hashtags et mentions
            r'#\w+',
            r'@\w+',
            r'@[A-Za-z0-9]+(?:Official)?(?:Music)?',  # Mentions complexes
            
            # Années entre parenthèses/crochets
            r'\(20\d{2}\)',
            r'\[20\d{2}\]',
            r'\(19\d{2}\)',
            r'\[19\d{2}\]',
            
            # Autres éléments communs
            r'\(Remix\)',
            r'\[Remix\]',
            r'\(Remastered\)',
            r'\[Remastered\]',
            r'\(Extended.*?\)',
            r'\[Extended.*?\]',
            r'\(feat\..*?\)',
            r'\[feat\..*?\]',
            r'\(ft\..*?\)',
            r'\[ft\..*?\]',
            
            # Emojis et caractères spéciaux
            r'[\U0001F600-\U0001F64F]',  # Emoticons
            r'[\U0001F300-\U0001F5FF]',  # Symboles et pictogrammes
            r'[\U0001F680-\U0001F6FF]',  # Transport et cartes
            r'[\U0001F1E0-\U0001F1FF]',  # Drapeaux
        ]
        
        # Séparateurs communs entre artiste et titre
        self.separators = ['-', '–', '—', '|', '•', ':', '/', '\\']
    
    def clean_title(self, title: str) -> str:
        """
        Nettoie un titre de vidéo YouTube.
        
        Args:
            title: Titre brut de la vidéo
            
        Returns:
            Titre nettoyé
        """
        if not title:
            return ""
        
        cleaned = title
        
        # Supprimer les patterns indésirables
        for pattern in self.remove_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Normaliser les espaces
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Supprimer les caractères de début/fin
        cleaned = cleaned.strip(' -–—|•:/')
        
        return cleaned
    
    def extract_artist_title(self, title: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Tente d'extraire l'artiste et le titre depuis un titre de vidéo.
        
        Args:
            title: Titre de la vidéo
            
        Returns:
            Tuple (artiste, titre) ou (None, titre_nettoyé) si pas de séparation claire
        """
        cleaned_title = self.clean_title(title)
        
        # Chercher un séparateur
        for sep in self.separators:
            if sep in cleaned_title:
                parts = cleaned_title.split(sep, 1)
                if len(parts) == 2:
                    artist = parts[0].strip()
                    song_title = parts[1].strip()
                    
                    # Vérifier que les deux parties ont du sens
                    if len(artist) > 1 and len(song_title) > 1:
                        return artist, song_title
        
        # Si aucun séparateur trouvé, retourner le titre nettoyé
        return None, cleaned_title
    
    def normalize_for_search(self, text: str) -> str:
        """
        Normalise le texte pour la recherche Spotify.
        
        Args:
            text: Texte à normaliser
            
        Returns:
            Texte normalisé pour la recherche
        """
        if not text:
            return ""
        
        # Convertir en minuscules
        normalized = text.lower()
        
        # Supprimer les accents et caractères spéciaux
        normalized = re.sub(r'[àáâãäå]', 'a', normalized)
        normalized = re.sub(r'[èéêë]', 'e', normalized)
        normalized = re.sub(r'[ìíîï]', 'i', normalized)
        normalized = re.sub(r'[òóôõö]', 'o', normalized)
        normalized = re.sub(r'[ùúûü]', 'u', normalized)
        normalized = re.sub(r'[ç]', 'c', normalized)
        normalized = re.sub(r'[ñ]', 'n', normalized)
        
        # Supprimer la ponctuation excessive
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        
        # Normaliser les espaces
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized
    
    def create_search_queries(self, title: str) -> List[str]:
        """
        Crée plusieurs variantes de requêtes de recherche pour maximiser les chances de trouvaille.
        
        Args:
            title: Titre original
            
        Returns:
            Liste de requêtes de recherche
        """
        queries = []
        
        # Extraire artiste et titre
        artist, song_title = self.extract_artist_title(title)
        
        if artist and song_title:
            # Requête principale: "artiste titre"
            queries.append(f"{artist} {song_title}")
            
            # Requête inversée: "titre artiste"
            queries.append(f"{song_title} {artist}")
            
            # Requête avec track: pour être plus précis
            queries.append(f"track:{song_title} artist:{artist}")
        
        # Toujours inclure le titre nettoyé simple
        cleaned = self.clean_title(title)
        if cleaned not in [q for q in queries]:
            queries.append(cleaned)
        
        # Version normalisée
        normalized = self.normalize_for_search(cleaned)
        if normalized not in [self.normalize_for_search(q) for q in queries]:
            queries.append(normalized)
        
        return queries[:5]  # Limiter à 5 variantes max


def main():
    """Test du module de nettoyage de titres."""
    cleaner = TitleCleaner()
    
    # Exemples de titres YouTube à tester
    test_titles = [
        "Rema - Calm Down (Official Music Video)",
        "Burna Boy | Last Last [Official Video]",
        "Asake - Joha (Official Audio) #asake #afrobeats",
        "Wizkid ft. Tems - Essence (Remix) [4K] (2021)",
        "🎵 DAVIDO - FEM (Official Video) 🔥",
        "Omah Lay • Bad Influence | Live Performance",
        "Fireboy DML: Peru [Lyrics Video] HD"
    ]
    
    print("🧹 Test du nettoyage de titres:")
    print("=" * 50)
    
    for title in test_titles:
        print(f"\nTitre original: {title}")
        
        # Nettoyage simple
        cleaned = cleaner.clean_title(title)
        print(f"Nettoyé: {cleaned}")
        
        # Extraction artiste/titre
        artist, song = cleaner.extract_artist_title(title)
        if artist:
            print(f"Artiste: {artist}")
            print(f"Titre: {song}")
        else:
            print(f"Titre seul: {song}")
        
        # Requêtes de recherche
        queries = cleaner.create_search_queries(title)
        print(f"Requêtes: {queries}")
        print("-" * 30)


if __name__ == "__main__":
    main()
