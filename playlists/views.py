# playlists/views.py

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Playlist, Song, SpotifyToken
from .spotify_utils import get_spotify_client, get_spotify_auth_manager

import spotipy
from django.http import JsonResponse
from django.urls import reverse

@login_required
def home(request):
    playlists = Playlist.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'playlists/home.html', {'playlists': playlists})


@login_required
def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    songs = playlist.songs.all().order_by('-added_at')

    if request.method == 'POST' and 'photo' in request.FILES:
        song_id = request.POST.get('song_id')
        photo = request.FILES['photo']
        try:
            song = Song.objects.get(id=song_id, playlist=playlist)
            song.photo = photo
            song.save()
            messages.success(request, 'Photo uploaded successfully.')
        except Song.DoesNotExist:
            messages.error(request, 'Song not found.')

    return render(request, 'playlists/playlist_detail.html', {
        'playlist': playlist,
        'songs': songs
    })

@login_required
def import_spotify_playlist(request):
    """
    Displays the user's Spotify playlists in a dropdown menu for selection.
    """
    spotify_client = get_spotify_client(request.user)
    if not spotify_client:
        messages.info(request, 'Connect Spotify to import playlists.')
        return redirect('playlists:spotify_login')
    else:
        messages.success(request, 'Spotify account connected successfully!')

    try:
        spotify_playlists = []  # Initialize an empty list for playlists
        offset = 0
        while True:
            playlists_data = spotify_client.current_user_playlists(limit=50, offset=offset)
            print("Fetched Spotify playlists data:", playlists_data)  # Debugging line
            if not playlists_data or not playlists_data.get('items'):
                break
            for pl in playlists_data['items']:
                if pl is None:
                    print("Warning: Found None in playlists_data['items']")
                    continue
                spotify_playlists.append({
                    'id': pl.get('id', 'Unknown ID'),
                    'name': pl.get('name', 'Unknown Name'),
                    'tracks': pl.get('tracks', {}).get('total', 0)
                })
            if not playlists_data['next']:
                break
            offset += 50
    except spotipy.SpotifyException as e:
        messages.error(request, f'Error fetching playlists: {e}')
        spotify_playlists = []
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        spotify_playlists = []

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print("Returning Spotify playlists:", spotify_playlists)  # Debugging line
        return JsonResponse({'spotify_playlists': spotify_playlists})

    return render(request, 'playlists/import_spotify_playlist.html', {
        'spotify_playlists': spotify_playlists
    })

@login_required
def import_selected_playlist(request):
    """
    Handles the import action for the selected Spotify playlist.
    """
    logger = logging.getLogger(__name__)
    logger.info('Received request to import selected playlist.')

    if request.method != 'POST':
        messages.error(request, 'Invalid request method.')
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

    playlist_id = request.POST.get('playlist_id')
    logger.info(f'Received playlist ID: {playlist_id}')

    if not playlist_id:
        messages.error(request, 'No playlist selected.')
        return JsonResponse({'success': False, 'error': 'No playlist selected.'}, status=400)

    spotify_client = get_spotify_client(request.user)
    if not spotify_client:
        messages.info(request, 'Connect Spotify to import playlists.')
        return JsonResponse({'success': False, 'error': 'Spotify client not available. Please connect your Spotify account.'}, status=400)

    try:
        # Fetch playlist details from Spotify
        playlist_data = spotify_client.playlist(playlist_id)
        playlist_name = playlist_data.get('name', 'Imported Playlist')

        logger.info(f'Fetched playlist data from Spotify: {playlist_data}')

        # Create or update Playlist in Django with the fetched name and description
        playlist, created = Playlist.objects.update_or_create(
            spotify_playlist_id=playlist_id,
            defaults={
                'title': playlist_name,
                'user': request.user,
                'description': playlist_data.get('description', '')
            }
        )
        logger.info(f'Playlist "{playlist.title}" with ID "{playlist.spotify_playlist_id}" {"created" if created else "updated"} successfully.')

        # **Add Songs to the Playlist**
        tracks_data = playlist_data['tracks']
        while True:
            for item in tracks_data['items']:
                track = item['track']
                if track:
                    Song.objects.update_or_create(
                        spotify_track_id=track['id'],
                        defaults={
                            'title': track['name'],
                            'playlist': playlist,
                            'photo': None  # Initialize with no photo
                            # Add more fields if necessary
                        }
                    )
            if tracks_data['next']:
                tracks_data = spotify_client.next(tracks_data)
            else:
                break

        message = f'Playlist "{playlist.title}" imported successfully with {playlist.songs.count()} songs.'

        logger.info(f'Returning success response for playlist "{playlist.title}".')
        return JsonResponse({
            'success': True,
            'message': message,
            'redirect_url': reverse('playlists:playlist_detail', args=[playlist.id])
        })
    except spotipy.SpotifyException as e:
        logger.error(f'Spotify API error: {e}')
        return JsonResponse({'success': False, 'error': f'Spotify API error: {e}'}, status=500)
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}')
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred.'}, status=500)


@login_required
def spotify_login(request):
    """
    Initiates the Spotify OAuth authentication process.
    """
    auth_manager = get_spotify_auth_manager(request.user)
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)

@login_required
def spotify_callback(request):
    """
    Handles the callback from Spotify after user authorization.
    """
    auth_manager = get_spotify_auth_manager(request.user)
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        messages.error(request, f'Spotify authentication failed: {error}')
        return redirect('playlists:import_spotify_playlist')

    if code:
        try:
            token_info = auth_manager.get_access_token(code)
            # Save or update the SpotifyToken model
            token, created = SpotifyToken.objects.update_or_create(
                user=request.user,
                defaults={
                    'access_token': token_info['access_token'],
                    'refresh_token': token_info['refresh_token'],
                    'token_type': token_info['token_type'],
                    'expires_in': token_info['expires_in'],
                    'scope': token_info['scope'],
                }
            )
            if created:
                messages.success(request, 'New Spotify account connected successfully.')
            else:
                messages.success(request, 'Spotify account reconnected successfully.')
            messages.success(request, 'Spotify account connected successfully.')
        except spotipy.SpotifyOauthError as e:
            messages.error(request, 'Failed to authenticate with Spotify.')
    else:
        messages.error(request, 'No code provided for Spotify authentication.')

    return redirect('playlists:import_spotify_playlist')


