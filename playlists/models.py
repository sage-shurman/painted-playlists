# playlists/models.py

from django.db import models  # Import Django's models module
from django.contrib.auth.models import User  # Import the User model for user associations

class Playlist(models.Model):
    """
    Model representing a music playlist.
    """
    spotify_playlist_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    # Unique identifier for the Spotify playlist, can be blank or null
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=250, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    # ForeignKey to associate the playlist with a user
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp for when the playlist was created

    def __str__(self):
        # String representation of the Playlist model
        return self.title

class Song(models.Model):
    """
    Model representing a song within a playlist.
    """
    title = models.CharField(max_length=80)
    spotify_track_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    # Unique identifier for the Spotify track, can be blank or null
    photo = models.ImageField(upload_to='song_photos/', blank=True, null=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='songs')
    # ForeignKey to associate the song with a playlist
    added_at = models.DateTimeField(auto_now_add=True)
    # Timestamp for when the song was added to the playlist

    def __str__(self):
        return self.title


class SpotifyToken(models.Model):
    """
    Model to store Spotify authentication tokens for a user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # One-to-one relationship with the User model
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=50)
    expires_in = models.IntegerField()
    scope = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Spotify Token for {self.user.username}'
