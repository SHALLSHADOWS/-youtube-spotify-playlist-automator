#!/usr/bin/env python3
"""
Script de test pour les améliorations du title cleaning.
Teste spécifiquement les cas d'échec identifiés.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.title_cleaner import TitleCleaner
from src.spotify_manager import SpotifyManager
import time

def test_failed_cases():
    """Test des cas qui ont échoué dans le rapport précédent."""
    
    print("🧪 Test des améliorations de Title Cleaning")
    print("=" * 50)
    
    # Cas d'échec identifiés
    failed_cases = [
        "Rema - DND (Official Music Video)",
        "Omah Lay - Understand (Official Music Video)", 
        "Fireboy DML, Asake - Bandana (Official Video)",
        "Didi B - Good vibes feat @ZinoleeskyOfficialMusic  (Official Visualizer)",
        "Joeboy - Baby (Visualizer)",
        "Rema - Ginger Me (Official Music Video)",
        "CKay - Emiliana [Official Music Video]",
    ]
    
    cleaner = TitleCleaner()
    
    try:
        spotify = SpotifyManager()
        print(f"✅ Connecté à Spotify\n")
    except Exception as e:
        print(f"❌ Erreur Spotify: {e}")
        print("🔄 Test du cleaning seulement...\n")
        spotify = None
    
    results = {
        'improved': 0,
        'still_failed': 0,
        'total': len(failed_cases)
    }
    
    for i, title in enumerate(failed_cases, 1):
        print(f"🔍 [{i}/{len(failed_cases)}] {title}")
        
        # Nettoyer et générer requêtes
        cleaned = cleaner.clean_title(title)
        queries = cleaner.create_search_queries(title)
        
        print(f"   📝 Nettoyé: {cleaned}")
        print(f"   🔎 Requêtes: {queries[:3]}...")  # Afficher les 3 premières
        
        if spotify:
            # Tester la recherche
            found = False
            for query in queries[:3]:  # Tester les 3 premières requêtes
                tracks = spotify.search_track(query)
                if tracks:
                    best_track = tracks[0]
                    artists_str = ", ".join(best_track['artists'])
                    print(f"   ✅ TROUVÉ: {best_track['name']} - {artists_str}")
                    results['improved'] += 1
                    found = True
                    break
                time.sleep(0.1)  # Éviter rate limiting
            
            if not found:
                print(f"   ❌ Toujours pas trouvé")
                results['still_failed'] += 1
        
        print()
    
    if spotify:
        print("📊 RÉSULTATS:")
        print(f"✅ Améliorés: {results['improved']}/{results['total']}")
        print(f"❌ Toujours échoués: {results['still_failed']}/{results['total']}")
        print(f"📈 Taux d'amélioration: {(results['improved']/results['total']*100):.1f}%")
    
    return results

def test_cleaning_specifics():
    """Test des améliorations spécifiques du cleaning."""
    
    print("\n🧹 Test des améliorations spécifiques")
    print("=" * 40)
    
    cleaner = TitleCleaner()
    
    test_cases = [
        ("Rema - DND (Official Music Video)", ["DND", "Rema DND", "DND Rema"]),
        ("Didi B feat @ZinoleeskyOfficialMusic", ["Didi B", "Zinoleesky", "Didi B Zinoleesky"]),
        ("STARBOY - SOCO ft. TERRI X SPOTLESS", ["SOCO", "STARBOY SOCO"]),
    ]
    
    for title, expected_elements in test_cases:
        print(f"\n📝 Titre: {title}")
        
        cleaned = cleaner.clean_title(title)
        queries = cleaner.create_search_queries(title)
        
        print(f"   Nettoyé: {cleaned}")
        print(f"   Requêtes: {queries}")
        
        # Vérifier si les éléments attendus sont présents
        all_text = ' '.join(queries).lower()
        found_elements = []
        for element in expected_elements:
            if element.lower() in all_text:
                found_elements.append(element)
        
        print(f"   ✅ Éléments trouvés: {found_elements}")
        if len(found_elements) == len(expected_elements):
            print(f"   🎯 PARFAIT!")
        else:
            missing = [e for e in expected_elements if e not in found_elements]
            print(f"   ⚠️  Manquants: {missing}")

if __name__ == "__main__":
    test_cleaning_specifics()
    test_failed_cases()
