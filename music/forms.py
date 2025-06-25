# music/forms.py
from django import forms
from .models import Song, Genre, Playlist

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'genre', 'duration']
        widgets = {
            'duration': forms.TimeInput(format='%H:%M:%S', attrs={'type': 'time'}),
        }

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome genere'}),
        }

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'songs']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Titolo playlist'}),
            'songs': forms.CheckboxSelectMultiple,
        }