from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from .models import Song, Genre, Playlist, Recommendation
from .forms import SongForm, GenreForm, PlaylistForm


class SongListView(LoginRequiredMixin, ListView):
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

    def form_valid(self, form):
        # assegno il nome utente corrente come artist
        form.instance.artist = self.request.user.username
        return super().form_valid(form)

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
    model         = Playlist
    form_class    = PlaylistForm
    template_name = 'music/playlist_form.html'
    success_url   = reverse_lazy('music:playlist-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # passo l'utente corrente al form
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        # salva l'istanza principale
        response = super().form_valid(form)
        # salva i M2M (songs + shared_with)
        return response
    

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
class GenreListView(LoginRequiredMixin, ListView):
    model = Genre
    template_name = 'music/genre_list.html'
    context_object_name = 'genres'


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

class PlaylistLeaveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        playlist = get_object_or_404(Playlist, pk=pk)
        if request.user in playlist.shared_with.all():
            playlist.shared_with.remove(request.user)
            messages.success(request, f"Hai lasciato la playlist “{playlist.name}”.")
        else:
            messages.warning(request, "Non puoi lasciare una playlist che non è condivisa con te.")
        return redirect('music:playlist-list')