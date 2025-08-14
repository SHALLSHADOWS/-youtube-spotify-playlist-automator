#!/usr/bin/env python3
"""
Demo script - Example usage of the YouTube to Spotify automator
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from title_cleaner import TitleCleaner


def demo_title_cleaning():
    """Demonstrate title cleaning capabilities."""
    print("🎵 YouTube to Spotify Automator - Demo")
    print("="*50)
    print("\n🧹 Title Cleaning Demo:")
    print("-"*30)
    
    cleaner = TitleCleaner()
    
    # Example YouTube titles that might be found in playlists
    example_titles = [
        "Rema - Calm Down (Official Music Video)",
        "Burna Boy | Last Last [Official Video]",
        "Asake - Joha (Official Audio) #asake #afrobeats",
        "Wizkid ft. Tems - Essence (Remix) [4K] (2021)",
        "🔥 DAVIDO - FEM (Official Video) 🔥 #davido #afrobeats",
        "Omah Lay • Bad Influence | Live Performance",
        "Fireboy DML: Peru [Lyrics Video] HD (Remastered)",
        "Shallipopi - Elon Musk (Remix) feat. Zlatan (Official Audio)",
        "CKay - love nwantiti (ah ah ah) [Official Music Video]"
    ]
    
    for i, title in enumerate(example_titles, 1):
        print(f"\n{i}. Original Title:")
        print(f"   {title}")
        
        # Clean the title
        cleaned = cleaner.clean_title(title)
        print(f"   Cleaned: {cleaned}")
        
        # Extract artist and song
        artist, song = cleaner.extract_artist_title(title)
        if artist:
            print(f"   Artist: {artist}")
            print(f"   Song: {song}")
        
        # Generate search queries
        queries = cleaner.create_search_queries(title)
        print(f"   Search queries: {queries[:3]}")  # Show first 3
    
    print("\n" + "="*50)
    print("✅ Demo completed!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env")
    print("2. Add your Spotify credentials")
    print("3. Run: python yt2spotify.py --help")
    print("4. Try with a real YouTube playlist!")


if __name__ == "__main__":
    demo_title_cleaning()
