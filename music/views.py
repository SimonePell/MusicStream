from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from .models import Song, Genre, Playlist
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
        return Playlist.objects.filter(owner=self.request.user)

class PlaylistDetailView(LoginRequiredMixin, DetailView):
    model = Playlist
    template_name = 'music/playlist_detail.html'
    context_object_name = 'playlist'

class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'music/playlist_form.html'
    success_url = reverse_lazy('music:playlist-list')

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

class PlaylistDeleteView(LoginRequiredMixin, DeleteView):
    model = Playlist
    template_name = 'music/playlist_confirm_delete.html'
    success_url = reverse_lazy('music:playlist-list')

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)