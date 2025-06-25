from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Genre, Song, Playlist, Recommendation

User = get_user_model()

class MusicTests(TestCase):
    def setUp(self):
        # Utente e login
        self.user = User.objects.create_user('listener', password='pwd12345')
        self.client.login(username='listener', password='pwd12345')

        # Genere e canzoni
        self.genre = Genre.objects.create(name='Rock')
        self.song1 = Song.objects.create(
            title='S1', artist='A1', genre=self.genre, duration='00:03:00'
        )
        self.song2 = Song.objects.create(
            title='S2', artist='A2', genre=self.genre, duration='00:04:00'
        )

        # Playlist
        self.pl = Playlist.objects.create(name='PL1', owner=self.user)
        self.pl.songs.add(self.song1)

    def test_song_list_and_detail(self):
        # List
        resp = self.client.get(reverse('music:song-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'S1')
        self.assertContains(resp, 'S2')

        # Detail
        resp = self.client.get(reverse('music:song-detail', args=[self.song1.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'A1')

    def test_playlist_crud(self):
        # List playlist
        resp = self.client.get(reverse('music:playlist-list'))
        self.assertContains(resp, 'PL1')

        # Detail playlist
        resp = self.client.get(
            reverse('music:playlist-detail', args=[self.pl.pk])
        )
        self.assertContains(resp, 'S1')

    def test_recommendation_list_empty(self):
        resp = self.client.get(reverse('music:recommendation-list'))
        self.assertContains(resp, 'Non ci sono raccomandazioni')

    def test_genre_add_permission(self):
        # listener non può aggiungere generi
        resp = self.client.get(reverse('music:genre-add'))
        self.assertEqual(resp.status_code, 403)
