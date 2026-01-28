# playlists/forms.py

# Import Django's forms module
from django import forms
from .models import Playlist, Song

class PlaylistForm(forms.ModelForm, forms.Form):
    """
    Form for creating and updating Playlist instances.
    Includes a dynamic ChoiceField for selecting a Spotify playlist.
    """
    spotify_playlist_id = forms.ChoiceField(
        # ChoiceField for selecting a Spotify playlist
        label='Select a Spotify Playlist',
        choices=[],  # Choices are populated dynamically in the __init__ method
        widget=forms.Select(attrs={'class': 'form-select', 'required': False}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        # Extract spotify_playlists from kwargs, defaulting to an empty list
        # Extract spotify_playlists from kwargs, defaulting to an empty list
        spotify_playlists = kwargs.pop('spotify_playlists', [])
        super().__init__(*args, **kwargs)
        # Populate the spotify_playlist_id choices with the provided playlists
        if spotify_playlists is not None:
            self.fields['spotify_playlist_id'].choices = [(pl['id'], f"{pl['name']} ({pl['tracks']} tracks)") for pl in spotify_playlists]
        else:  # Exit loop if no more tracks
            self.fields['spotify_playlist_id'].choices = []
    class Meta:
        """
        Meta class to specify the model and fields to include in the form.
        """
        """
        Meta class to specify the model and fields to include in the form.
        """
        model = Playlist
        fields = ['title', 'description']
        widgets = {  # Custom widgets for form fields
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Playlist Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Playlist Description', 'rows': 3}),
        }

class SongForm(forms.ModelForm):
    """
    Form for creating and updating Song instances.
    """
    class Meta:
        model = Song
        fields = ['title', 'photo']
        widgets = {  # Custom widgets for form fields
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Song Title'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


    def __init__(self, *args, **kwargs):
        spotify_playlists = kwargs.pop('spotify_playlists', [])
        super().__init__(*args, **kwargs)
        # Populate the playlist_id choices with the provided playlists
        self.fields['playlist_id'].choices = [(pl['id'], f"{pl['name']} ({pl['tracks']} tracks)") for pl in spotify_playlists]
