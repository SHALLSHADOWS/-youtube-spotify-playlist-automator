"""
Configuration settings for the YouTube to Spotify automator
"""

# YouTube extraction settings
YOUTUBE_CONFIG = {
    'min_duration': 30,  # Minimum video duration in seconds
    'max_duration': 600,  # Maximum video duration in seconds (10 min)
    'skip_shorts': True,  # Skip YouTube Shorts
    'extraction_timeout': 60,  # Timeout for video extraction in seconds
}

# Spotify search settings
SPOTIFY_CONFIG = {
    'search_limit': 10,  # Number of results per search query
    'relevance_threshold': 0.3,  # Minimum relevance score to accept a match
    'max_search_queries': 5,  # Maximum number of search variations per title
    'rate_limit_delay': 0.1,  # Delay between API calls in seconds
}

# Title cleaning settings
CLEANING_CONFIG = {
    'remove_brackets': True,  # Remove content in brackets/parentheses
    'remove_hashtags': True,  # Remove hashtags
    'remove_mentions': True,  # Remove @mentions
    'normalize_unicode': True,  # Normalize unicode characters
    'min_artist_length': 2,  # Minimum artist name length
    'min_title_length': 2,  # Minimum song title length
}

# Report settings
REPORT_CONFIG = {
    'save_detailed_report': True,  # Save detailed report to file
    'report_format': 'txt',  # Report format: 'txt' or 'csv'
    'include_scores': True,  # Include relevance scores in report
    'backup_reports': True,  # Keep backup of previous reports
}

# Playlist settings
PLAYLIST_CONFIG = {
    'default_public': True,  # Create public playlists by default
    'add_timestamp': False,  # Add timestamp to playlist name
    'max_playlist_size': 1000,  # Maximum tracks per playlist
    'default_description_template': "Playlist imported from YouTube on {date}",
}

# Error handling
ERROR_CONFIG = {
    'max_retries': 3,  # Maximum retries for failed operations
    'retry_delay': 2,  # Delay between retries in seconds
    'continue_on_error': True,  # Continue processing even if some tracks fail
    'log_errors': True,  # Log errors to file
}
