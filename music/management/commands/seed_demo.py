# music/management/commands/seed_demo.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from music.models import Genre, Song, Playlist, Recommendation

class Command(BaseCommand):
    help = "Popola il DB con dati demo: gruppi, utenti, generi, canzoni, playlist e raccomandazioni"

    def handle(self, *args, **options):
        User = get_user_model()

        # 1) Gruppi
        listener_grp, _ = Group.objects.get_or_create(name='Listener')
        curator_grp, _  = Group.objects.get_or_create(name='Curator')
        self.stdout.write(self.style.SUCCESS(" Gruppi Listener e Curator creati"))

        # 2) Utenti
        curator, created = User.objects.get_or_create(username='curator', defaults={'email':'curator@demo.com'})
        if created:
            curator.set_password('Curator123')
            curator.save()
        curator.groups.add(curator_grp)
        self.stdout.write(self.style.SUCCESS(" Utente Curator creato (username: curator / pwd: Curator123)"))

        listener, created = User.objects.get_or_create(username='listener', defaults={'email':'listener@demo.com'})
        if created:
            listener.set_password('Listener123')
            listener.save()
        listener.groups.add(listener_grp)
        self.stdout.write(self.style.SUCCESS(" Utente Listener creato (username: listener / pwd: Listener123)"))

        # 3) Generi
        genres = ['Rock', 'Pop', 'Jazz']
        genre_objs = []
        for name in genres:
            g, _ = Genre.objects.get_or_create(name=name)
            genre_objs.append(g)
        self.stdout.write(self.style.SUCCESS(f" Generi creati: {', '.join(genres)}"))

        # 4) Canzoni
        songs_data = [
            ('Bohemian Rhapsody', 'Queen', 'Rock', '00:05:55'),
            ('Billie Jean',       'Michael Jackson', 'Pop', '00:04:54'),
            ('Take Five',         'Dave Brubeck', 'Jazz', '00:05:24'),
        ]
        song_objs = []
        for title, artist, gen_name, duration in songs_data:
            genre = Genre.objects.get(name=gen_name)
            s, _ = Song.objects.get_or_create(
                title=title, artist=artist, genre=genre, duration=duration
            )
            song_objs.append(s)
        self.stdout.write(self.style.SUCCESS(" Canzoni demo create"))

        # 5) Playlist per listener
        pl, _ = Playlist.objects.get_or_create(name='La mia Prima Playlist', owner=listener)
        pl.songs.set(song_objs[:2])  # le prime due
        self.stdout.write(self.style.SUCCESS(" Playlist demo creata"))

        # 6) Raccomandazioni
        # diamo un punteggio crescente
        for idx, song in enumerate(song_objs, start=1):
            Recommendation.objects.update_or_create(
                user=listener, song=song,
                defaults={'score': 5.0 - idx}  # es. 4.0,3.0,2.0
            )
        self.stdout.write(self.style.SUCCESS(" Raccomandazioni demo create"))

        self.stdout.write(self.style.SUCCESS(" Seed demo completato!"))
