from django.urls import path
from .views import (
    SongListView, SongDetailView, SongCreateView, SongUpdateView, SongDeleteView,
    GenreListView, GenreCreateView, GenreUpdateView, GenreDeleteView,
    PlaylistListView, PlaylistDetailView, PlaylistCreateView, PlaylistUpdateView, PlaylistDeleteView, PlaylistLeaveView,
    RecommendationListView
)

app_name = 'music'

urlpatterns = [
    # Songs CRUD
    path('', SongListView.as_view(), name='song-list'),
    path('<int:pk>/', SongDetailView.as_view(), name='song-detail'),
    path('songs/add/', SongCreateView.as_view(), name='song-add'),
    path('songs/<int:pk>/edit/', SongUpdateView.as_view(), name='song-edit'),
    path('songs/<int:pk>/delete/', SongDeleteView.as_view(), name='song-delete'),

    # Generi CRUD
    path('genres/',             GenreListView.as_view(),   name='genre-list'),
    path('genres/add/',         GenreCreateView.as_view(), name='genre-add'),
    path('genres/<int:pk>/edit/',   GenreUpdateView.as_view(), name='genre-edit'),
    path('genres/<int:pk>/delete/', GenreDeleteView.as_view(), name='genre-delete'),


    # Playlists CRUD
    path('playlists/', PlaylistListView.as_view(), name='playlist-list'),
    path('playlists/add/', PlaylistCreateView.as_view(), name='playlist-add'),
    path('playlists/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('playlists/<int:pk>/edit/', PlaylistUpdateView.as_view(), name='playlist-edit'),
    path('playlists/<int:pk>/delete/', PlaylistDeleteView.as_view(), name='playlist-delete'),
    path('playlists/<int:pk>/leave/', PlaylistLeaveView.as_view(), name='playlist-leave'),

    # Recommendations
    path('recommendations/', RecommendationListView.as_view(), name='recommendation-list'),

]