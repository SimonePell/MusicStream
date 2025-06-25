import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from music.models import Genre, Song, Playlist
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Seed demo music: genera generi, 200 canzoni e 1-3 playlist per listener"

    def handle(self, *args, **options):
        User = get_user_model()

        #  Generi di esempio
        genres = ['Pop', 'Rock', 'Jazz', 'Classical', 'Hip-Hop', 'Electronic', 'Reggae', 'Country']
        for name in genres:
            Genre.objects.get_or_create(name=name)
        all_genres = list(Genre.objects.all())

        #  Genera 200 canzoni
        for i in range(1, 201):
            title  = f"Song {i:03d}"
            artist = f"Artist {random.randint(1,50)}"
            genre  = random.choice(all_genres)
            # durata casuale tra 2:00 e 5:59
            duration = timedelta(minutes=random.randint(2,5), seconds=random.randint(0,59))
            Song.objects.get_or_create(
                title=title,
                artist=artist,
                genre=genre,
                duration=duration
            )

        all_songs = list(Song.objects.all())

        #  Per ciascun listener crea 1-3 playlist con 5-20 canzoni ciascuna
        listeners = User.objects.filter(groups__name='Listener')
        for user in listeners:
            for n in range(random.randint(1, 3)):
                pl_name = f"{user.username} Playlist {n+1}"
                pl, created = Playlist.objects.get_or_create(name=pl_name, owner=user)
                # aggiungi 5-20 canzoni casuali
                pl.songs.set(random.sample(all_songs, k=random.randint(5,20)))

        self.stdout.write(self.style.SUCCESS(" musica seminata: generi, canzoni e playlist ascoltatori"))
