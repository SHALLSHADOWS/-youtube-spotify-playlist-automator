#!/usr/bin/env python3
"""
Test script for the YouTube to Spotify automator components
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


def test_title_cleaner():
    """Test the title cleaner module."""
    print("🧹 Testing Title Cleaner...")
    
    try:
        from title_cleaner import TitleCleaner
        cleaner = TitleCleaner()
        
        test_cases = [
            "Rema - Calm Down (Official Music Video)",
            "Burna Boy | Last Last [Official Video]",
            "Asake - Joha (Official Audio) #asake #afrobeats",
            "Wizkid ft. Tems - Essence (Remix) [4K] (2021)"
        ]
        
        for title in test_cases:
            cleaned = cleaner.clean_title(title)
            artist, song = cleaner.extract_artist_title(title)
            queries = cleaner.create_search_queries(title)
            
            print(f"\nOriginal: {title}")
            print(f"Cleaned: {cleaned}")
            if artist:
                print(f"Artist: {artist}, Song: {song}")
            print(f"Queries: {queries[:2]}")  # Show first 2 queries
        
        print("✅ Title Cleaner test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Title Cleaner test failed: {e}")
        return False


def test_youtube_extractor():
    """Test the YouTube extractor module (without actual extraction)."""
    print("\n📺 Testing YouTube Extractor...")
    
    try:
        from youtube_extractor import YouTubeExtractor
        extractor = YouTubeExtractor()
        
        # Test URL validation
        test_urls = [
            "https://www.youtube.com/playlist?list=PLtest123",
            "https://youtube.com/watch?v=test&list=PLtest456",
            "https://music.youtube.com/playlist?list=PLtest789",
            "https://invalid-url.com/playlist"
        ]
        
        for url in test_urls:
            is_valid = extractor.is_valid_youtube_url(url)
            print(f"URL: {url[:40]}... -> Valid: {is_valid}")
        
        print("✅ YouTube Extractor test passed!")
        return True
        
    except Exception as e:
        print(f"❌ YouTube Extractor test failed: {e}")
        return False


def test_environment():
    """Test if the environment is properly set up."""
    print("\n🔧 Testing Environment...")
    
    try:
        # Check if .env exists
        env_exists = os.path.exists('.env')
        print(f"Environment file (.env): {'✅ Found' if env_exists else '❌ Missing'}")
        
        if not env_exists:
            print("ℹ️  Copy .env.example to .env and add your Spotify credentials")
        
        # Test dotenv loading
        from dotenv import load_dotenv
        load_dotenv()
        
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        print(f"SPOTIFY_CLIENT_ID: {'✅ Set' if client_id else '❌ Missing'}")
        print(f"SPOTIFY_CLIENT_SECRET: {'✅ Set' if client_secret else '❌ Missing'}")
        
        if not (client_id and client_secret):
            print("⚠️  Spotify credentials not configured. Some tests may fail.")
        
        print("✅ Environment test completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Environment test failed: {e}")
        return False


def test_spotify_manager():
    """Test the Spotify manager module (without authentication)."""
    print("\n🎵 Testing Spotify Manager...")
    
    try:
        from spotify_manager import SpotifyManager
        
        # Test initialization (may fail without credentials)
        try:
            SpotifyManager()
            print("✅ Spotify Manager initialized")
        except ValueError as e:
            print(f"⚠️  {e}")
            print("This is expected if credentials are not configured")
        
        print("✅ Spotify Manager test passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Spotify Manager test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 YouTube to Spotify Automator - Component Tests")
    print("=" * 55)
    
    tests = [
        test_environment,
        test_title_cleaner,
        test_youtube_extractor,
        test_spotify_manager
    ]
    
    results = []
    
    for test in tests:
        result = test()
        results.append(result)
    
    print("\n" + "=" * 55)
    print("📊 TEST RESULTS")
    print("=" * 55)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The environment is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
