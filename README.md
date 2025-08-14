# 🎵 YouTube Mix → Spotify Playlist Automator

Automatisez le transfert de playlists YouTube (y compris les Mix non exportables) vers Spotify en un seul script Python.

## 🎯 Fonctionnalités

- **Extraction automatique** des vidéos YouTube depuis n'importe quel lien (playlist, mix)
- **Nettoyage intelligent** des titres pour une meilleure correspondance
- **Recherche et création** automatique de playlist Spotify
- **Rapport détaillé** des morceaux trouvés/introuvables
- **Support des Mix YouTube** non exportables
- **Filtrage intelligent** (ignore les vidéos trop courtes, nettoie les hashtags)

## 🚀 Installation rapide

1. **Clonez/téléchargez** ce projet
2. **Installez les dépendances** :

```bash
pip install -r requirements.txt
```

3. **Configurez Spotify** :

   - Créez une app sur [Spotify Developer Dashboard](https://developer.spotify.com/)
   - Copiez `.env.example` vers `.env`
   - Ajoutez vos `SPOTIFY_CLIENT_ID` et `SPOTIFY_CLIENT_SECRET`

4. **Testez l'installation** :

```bash
python demo.py
```

## 📖 Utilisation simple

```bash
python yt2spotify.py --youtube "https://youtube.com/playlist?list=XXXXX" --name "Ma Playlist"
```

### Exemples concrets

**Mix Afrobeats depuis YouTube Music :**

```bash
python yt2spotify.py \
    --youtube "https://music.youtube.com/playlist?list=RDCLAK5uy_kCnwJA4E9RxpXxClBDMC3" \
    --name "Afrobeats Hits 2024" \
    --description "Mix automatique Afrobeats"
```

**Playlist privée avec limite :**

```bash
python yt2spotify.py \
    --youtube "https://www.youtube.com/playlist?list=PLrAudmqGX2leFVt7hqRXfCqaZQGUbWjKK" \
    --name "Mes Découvertes" \
    --private \
    --max-tracks 25
```

## � Résultats attendus

```
🎵 29 vidéos trouvées sur YouTube
✅ 25 titres ajoutés à la playlist Spotify
❌ 4 titres introuvables (voir rapport_transfert.txt)
🎯 Playlist créée : https://open.spotify.com/playlist/XXXX
📈 Taux de réussite: 86.2%
```

## 🛠️ Structure du projet

- `yt2spotify.py` : Script principal
- `src/` : Modules du projet
  - `youtube_extractor.py` : Extraction YouTube via yt-dlp
  - `title_cleaner.py` : Nettoyage intelligent des titres
  - `spotify_manager.py` : Gestion API Spotify
- `demo.py` : Démonstration des fonctionnalités
- `test_components.py` : Tests des composants
- `USAGE.md` : Guide détaillé d'utilisation

## ✨ Types d'URLs supportées

- **Playlists YouTube** : `https://youtube.com/playlist?list=PLxxxxx`
- **Mix automatiques** : `https://music.youtube.com/playlist?list=RDxxxxx`
- **Radio YouTube Music** : `https://music.youtube.com/playlist?list=RDCLAKxxxxx`
- **Vidéo avec playlist** : `https://youtube.com/watch?v=xxxxx&list=PLxxxxx`

## 🔧 Options disponibles

| Option              | Description                        |
| ------------------- | ---------------------------------- |
| `--youtube, -y`     | URL YouTube (obligatoire)          |
| `--name, -n`        | Nom playlist Spotify (obligatoire) |
| `--description, -d` | Description playlist (optionnel)   |
| `--private`         | Créer une playlist privée          |
| `--force`           | Forcer même si playlist existe     |
| `--report-only`     | Générer seulement le rapport       |
| `--max-tracks N`    | Limiter à N pistes                 |

## 🎵 Dépendances

- `yt-dlp` : Extraction vidéos YouTube
- `spotipy` : API Spotify officielle
- `python-dotenv` : Variables d'environnement

## 📄 Documentation complète

Consultez [USAGE.md](USAGE.md) pour le guide détaillé avec exemples et dépannage.

## 🎯 Pourquoi ce projet ?

Ce projet permet de récupérer facilement les **Mix YouTube automatiques** qui ne peuvent pas être sauvegardés directement ou exportés via Soundiiz sans abonnement premium. Il automatise complètement le processus en un seul script Python gratuit.

## 📄 Licence

MIT License - Utilisez librement pour vos projets !
