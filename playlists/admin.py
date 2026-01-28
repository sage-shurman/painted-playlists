from django.contrib import admin
from .models import Playlist, Song, SpotifyToken

class SongInline(admin.TabularInline):
    model = Song
    extra = 1

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    inlines = [SongInline]

admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Song)
admin.site.register(SpotifyToken)
