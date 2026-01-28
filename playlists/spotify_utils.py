# playlists/spotify_utils.py

import spotipy  # Import the Spotipy library for interacting with the Spotify API
from spotipy.oauth2 import SpotifyOAuth  # Import SpotifyOAuth for handling authentication
from django.conf import settings  # Import Django settings to access environment variables
from .models import SpotifyToken  # Import the SpotifyToken model to manage user tokens

def get_spotify_auth_manager(user):
    """
    Create a SpotifyOAuth manager for a specific user.
    This handles the authentication flow and token management.
    """
    scope = 'playlist-read-private playlist-read-collaborative'
    # Define the scope of permissions required from the Spotify API
    # Use a unique cache path for each user to ensure tokens are user-specific
    return SpotifyOAuth(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI,
        scope=scope,
        cache_path=None  # Manage caching via the SpotifyToken model
    )

def get_spotify_client(user):
    """
    Retrieve a Spotipy client for a user, ensuring the token is valid.
    Returns None if the user hasn't connected Spotify or if the token is invalid.
    """
    try:  # Attempt to exchange code for access token
        token = SpotifyToken.objects.get(user=user)
    except SpotifyToken.DoesNotExist:
        # Return None if the user hasn't connected their Spotify account
        return None  # User hasn't connected Spotify

    # Ensure the token is associated with the correct user
    # Return None if the token does not belong to the user
    if token.user != user:
        return None

    auth_manager = get_spotify_auth_manager(user)

    # Prepare token_info dictionary for expiration check
    # This dictionary mimics the structure expected by Spotipy
    token_info = {
        'access_token': token.access_token,
        'refresh_token': token.refresh_token,
        'expires_in': token.expires_in,
        'token_type': token.token_type,
        'scope': token.scope,
        'expires_at': token.created_at.timestamp() + token.expires_in
    }

    # Check if token is expired and refresh if necessary
    # Update the SpotifyToken model with new token info if refreshed
    if auth_manager.is_token_expired(token_info):
        token_info = auth_manager.refresh_access_token(token.refresh_token)
        # Update the SpotifyToken model with new token info
        token.access_token = token_info['access_token']
        token.expires_in = token_info['expires_in']
        token.token_type = token_info['token_type']
        token.scope = token_info['scope']
        token.save()

    # Initialize Spotipy client with the token
    # Return the Spotipy client for making API calls
    return spotipy.Spotify(auth=token.access_token)
