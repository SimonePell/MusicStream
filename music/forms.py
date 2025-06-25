# music/forms.py

from django import forms
from django.contrib.auth import get_user_model
from .models import Song, Genre, Playlist

User = get_user_model()

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
    shared_with = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),  # verrà settato dinamicamente
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Condividi con"
    )

    class Meta:
        model = Playlist
        fields = ['name', 'songs', 'shared_with']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Titolo playlist'}),
            'songs': forms.CheckboxSelectMultiple(),
            'shared_with': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        # estrai user da kwargs se passato (vedi View più avanti)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # popola la lista dei brani e degli utenti
        self.fields['songs'].queryset = Song.objects.all()
        if user:
            self.fields['shared_with'].queryset = User.objects.exclude(pk=user.pk)
        else:
            self.fields['shared_with'].queryset = User.objects.all()
