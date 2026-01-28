# playlists/urls.py

from django.urls import path
from . import views

app_name = 'playlists'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('import_spotify/', views.import_spotify_playlist, name='import_spotify_playlist'),
    path('spotify_login/', views.spotify_login, name='spotify_login'),
    path('spotify_callback/', views.spotify_callback, name='spotify_callback'),
    path('import_selected/', views.import_selected_playlist, name='import_selected_playlist'),

]
