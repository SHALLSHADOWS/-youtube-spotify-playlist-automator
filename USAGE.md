# Guide d'utilisation détaillé

## 🚀 Installation et configuration

### 1. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 2. Configuration Spotify

1. Allez sur [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Créez une nouvelle application
3. Notez votre `Client ID` et `Client Secret`
4. Ajoutez `http://localhost:8080/callback` dans les URI de redirection
5. Copiez `.env.example` vers `.env` et complétez :

```env
SPOTIFY_CLIENT_ID=votre_client_id_ici
SPOTIFY_CLIENT_SECRET=votre_client_secret_ici
SPOTIFY_REDIRECT_URI=http://localhost:8080/callback
```

## 📖 Utilisation

### Commande de base

```bash
python yt2spotify.py --youtube "URL_YOUTUBE" --name "NOM_PLAYLIST"
```

### Exemples concrets

#### 1. Mix Afrobeats

```bash
python yt2spotify.py \
    --youtube "https://music.youtube.com/playlist?list=RDCLAK5uy_kCnwJA4E9RxpXxClBDMC3" \
    --name "Afrobeats Hits 2024" \
    --description "Mix automatique Afrobeats"
```

#### 2. Playlist privée avec limite

```bash
python yt2spotify.py \
    --youtube "https://www.youtube.com/playlist?list=PLrAudmqGX2leFVt7hqRXfCqaZQGUbWjKK" \
    --name "Ma Découverte Musicale" \
    --description "Nouvelles découvertes" \
    --private \
    --max-tracks 50
```

#### 3. Mode rapport seulement (sans créer la playlist)

```bash
python yt2spotify.py \
    --youtube "https://youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ" \
    --name "Test Analysis" \
    --report-only
```

### Options disponibles

| Option              | Description                        | Exemple                                   |
| ------------------- | ---------------------------------- | ----------------------------------------- |
| `--youtube, -y`     | URL YouTube (obligatoire)          | `"https://youtube.com/playlist?list=XXX"` |
| `--name, -n`        | Nom playlist Spotify (obligatoire) | `"Ma Playlist"`                           |
| `--description, -d` | Description playlist               | `"Importée de YouTube"`                   |
| `--private`         | Créer une playlist privée          | (pas de valeur)                           |
| `--force`           | Forcer même si playlist existe     | (pas de valeur)                           |
| `--report-only`     | Générer seulement le rapport       | (pas de valeur)                           |
| `--max-tracks`      | Limiter le nombre de pistes        | `50`                                      |

## 🎯 Types d'URLs YouTube supportées

- **Playlists classiques** : `https://youtube.com/playlist?list=PLxxxxx`
- **Mix automatiques** : `https://music.youtube.com/playlist?list=RDxxxxx`
- **Radio stations** : `https://music.youtube.com/playlist?list=RDCLAKxxxxx`
- **Vidéo avec playlist** : `https://youtube.com/watch?v=xxxxx&list=PLxxxxx`

## 📊 Interprétation des résultats

### Codes de sortie

- `0` : Succès complet
- `1` : Erreur générale ou aucune piste trouvée
- `2` : Moins de 50% de réussite
- `130` : Interruption par l'utilisateur (Ctrl+C)

### Rapport généré

Le script génère automatiquement un rapport dans `reports/rapport_transfert_YYYYMMDD_HHMMSS.txt` avec :

- Résumé des statistiques
- Liste des pistes trouvées avec scores de pertinence
- Liste des pistes non trouvées
- URL de la playlist créée

## 🔧 Résolution de problèmes

### Erreur d'authentification Spotify

```
❌ Variables d'environnement manquantes!
```

**Solution** : Vérifiez votre fichier `.env` et vos credentials Spotify.

### Aucune vidéo trouvée

```
❌ Aucune vidéo trouvée dans la playlist!
```

**Solutions** :

- Vérifiez que l'URL est correcte
- La playlist peut être privée ou supprimée
- Certains mix YouTube ont des restrictions géographiques

### Playlist existe déjà

```
⚠️ Une playlist 'Mon Nom' existe déjà!
```

**Solutions** :

- Utilisez `--force` pour forcer la création
- Choisissez un autre nom avec `--name`

### Peu de correspondances trouvées

Si moins de 50% des pistes sont trouvées :

- Les titres YouTube peuvent être mal formatés
- Essayez avec des playlists de meilleure qualité
- Vérifiez le rapport pour voir les requêtes de recherche utilisées

## 🎵 Conseils pour de meilleurs résultats

### URLs recommandées

- **Playlists officielles** (labels, artistes) ont de meilleurs titres
- **Mix YouTube Music** sont généralement bien formatés
- **Évitez** les compilations avec beaucoup de remixes amateurs

### Optimisation

- Utilisez `--max-tracks` pour tester avec peu de pistes d'abord
- Le script respecte les rate limits Spotify automatiquement
- Les pistes trop courtes (<30s) sont automatiquement ignorées

## 🔬 Mode test

Pour tester les composants sans faire de transfert complet :

```bash
python test_components.py
```

Cela vérifie :

- ✅ Variables d'environnement
- ✅ Nettoyage des titres
- ✅ Validation des URLs YouTube
- ✅ Initialisation Spotify

## 📝 Exemples de sorties

### Succès complet

```
🎵 YouTube Mix → Spotify Playlist Automator
==================================================
📥 Extraction de la playlist YouTube...
🎵 45 vidéos trouvées sur YouTube
✅ 45 vidéos extraites

🧹 Nettoyage des titres et recherche Spotify...
🔍 [1/45] Rema - Calm Down (Official Music Video)...
✅ → Calm Down - Rema
🔍 [2/45] Burna Boy - Last Last [Official Video]...
✅ → Last Last - Burna Boy
...

🎯 Création de la playlist Spotify...
✅ Playlist créée: Afrobeats Hits 2024
✅ 43 pistes ajoutées à la playlist
🎉 Playlist créée avec succès!

============================================================
📊 RÉSUMÉ DU TRANSFERT
============================================================
🎵 Vidéos YouTube analysées: 45
✅ Pistes trouvées sur Spotify: 43
❌ Pistes non trouvées: 2
📈 Taux de réussite: 95.6%
🎯 Playlist créée: https://open.spotify.com/playlist/37i9dQZF1DXxxxxxx
⏱️  Temps de traitement: 127.3s
============================================================
📄 Rapport sauvegardé: reports/rapport_transfert_20250814_143022.txt
```
