from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Song, Genre, Playlist, Recommendation
from .forms import SongForm, GenreForm, PlaylistForm


class SongListView(ListView):
    model = Song
    template_name = 'music/song_list.html'
    context_object_name = 'songs'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(artist__icontains=q)
        genre = self.request.GET.get('genre')
        if genre:
            qs = qs.filter(genre__name=genre)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['genres'] = Genre.objects.all()
        return ctx

class SongDetailView(DetailView):
    model = Song
    template_name = 'music/song_detail.html'
    context_object_name = 'song'

class SongCreateView(PermissionRequiredMixin, CreateView):
    model = Song
    form_class = SongForm
    template_name = 'music/song_form.html'
    success_url = reverse_lazy('music:song-list')
    permission_required = 'music.add_song'

class SongUpdateView(PermissionRequiredMixin, UpdateView):
    model = Song
    form_class = SongForm
    template_name = 'music/song_form.html'
    success_url = reverse_lazy('music:song-list')
    permission_required = 'music.change_song'

class SongDeleteView(PermissionRequiredMixin, DeleteView):
    model = Song
    template_name = 'music/song_confirm_delete.html'
    success_url = reverse_lazy('music:song-list')
    permission_required = 'music.delete_song'

class GenreCreateView(PermissionRequiredMixin, CreateView):
    model = Genre
    form_class = GenreForm
    template_name = 'music/genre_form.html'
    success_url = reverse_lazy('music:song-list')
    permission_required = 'music.add_genre'

class PlaylistListView(LoginRequiredMixin, ListView):
    model = Playlist
    template_name = 'music/playlist_list.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        user = self.request.user
        # owner O condivise con l’utente
        return Playlist.objects.filter(
            Q(owner=user) | Q(shared_with=user)
        ).distinct()


class PlaylistDetailView(LoginRequiredMixin, DetailView):
    model = Playlist
    template_name = 'music/playlist_detail.html'
    context_object_name = 'playlist'


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'music/playlist_form.html'
    success_url = reverse_lazy('music:playlist-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PlaylistUpdateView(LoginRequiredMixin, UpdateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'music/playlist_form.html'
    success_url = reverse_lazy('music:playlist-list')

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PlaylistDeleteView(LoginRequiredMixin, DeleteView):
    model = Playlist
    template_name = 'music/playlist_confirm_delete.html'
    success_url = reverse_lazy('music:playlist-list')

    def get_queryset(self):
        # solo le proprie playlist
        return Playlist.objects.filter(owner=self.request.user)

class RecommendationListView(LoginRequiredMixin, ListView):
    model = Recommendation
    template_name = 'music/recommendation_list.html'
    context_object_name = 'recommendations'
    paginate_by = 20

    def get_queryset(self):
        qs = Recommendation.objects.filter(user=self.request.user)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(song__title__icontains=q)
        return qs

# Lista generi (view per Curator e Listener – entrambi possono vedere i generi)
class GenreListView(PermissionRequiredMixin, ListView):
    model = Genre
    template_name = 'music/genre_list.html'
    context_object_name = 'genres'
    permission_required = 'music.view_genre'


# Creazione (già esistente)
class GenreCreateView(PermissionRequiredMixin, CreateView):
    model = Genre
    form_class = GenreForm
    template_name = 'music/genre_form.html'
    success_url = reverse_lazy('music:genre-list')
    permission_required = 'music.add_genre'


# Modifica
class GenreUpdateView(PermissionRequiredMixin, UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = 'music/genre_form.html'
    success_url = reverse_lazy('music:genre-list')
    permission_required = 'music.change_genre'


# Eliminazione
class GenreDeleteView(PermissionRequiredMixin, DeleteView):
    model = Genre
    template_name = 'music/genre_confirm_delete.html'
    success_url = reverse_lazy('music:genre-list')
    permission_required = 'music.delete_genre'