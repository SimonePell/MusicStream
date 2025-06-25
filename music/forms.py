# music/forms.py

from django import forms
from django.contrib.auth import get_user_model
from .models import Song, Genre, Playlist
from datetime import timedelta

User = get_user_model()

class SongForm(forms.ModelForm):
    duration_min = forms.IntegerField(
        label="Durata (minuti)",
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Es. 3'
        })
    )

    class Meta:
        model = Song
        # NON includiamo più 'artist' fra i campi del form: la mettiamo da view
        fields = ['title', 'genre']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # inizializza duration_min se stai editando
        if self.instance and self.instance.pk:
            secs = self.instance.duration.total_seconds()
            self.fields['duration_min'].initial = int(secs // 60)

    def save(self, commit=True):
        inst = super().save(commit=False)
        # metto la durata
        mins = self.cleaned_data['duration_min']
        inst.duration = timedelta(minutes=mins)
        if commit:
            inst.save()
        return inst

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome genere'}),
        }

class PlaylistForm(forms.ModelForm):
    shared_with = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2',
            'style': 'width: 100%;'
        }),
        label="Condividi con"
    )

    class Meta:
        model = Playlist
        fields = ['name', 'songs', 'shared_with']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titolo playlist'}),
            'songs': forms.SelectMultiple(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'size': 10}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['songs'].queryset = Song.objects.all()
        if user:
            self.fields['shared_with'].queryset = User.objects.exclude(pk=user.pk)
        else:
            self.fields['shared_with'].queryset = User.objects.all()
