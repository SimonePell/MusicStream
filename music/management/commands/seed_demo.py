# music/management/commands/seed_demo.py
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from music.models import Genre, Song, Playlist, Recommendation

User = get_user_model()

class Command(BaseCommand):
    help = "Popola il DB con dati demo (utenti, generi, canzoni, playlist, raccomandazioni)"

    def handle(self, *args, **options):
        self.stdout.write(" Pulizia tabelle demo…")
        # elimina demo-only
        Recommendation.objects.all().delete()
        Playlist.objects.all().delete()
        Song.objects.all().delete()
        Genre.objects.all().delete()
        # non tocchiamo superuser o account reale, rimuoviamo solo demo_
        User.objects.filter(username__startswith='demo_').delete()

        # Gruppi
        listener_group, _ = Group.objects.get_or_create(name='Listener')
        curator_group, _ = Group.objects.get_or_create(name='Curator')

        self.stdout.write(" Creazione utenti demo…")
        # 10 listener
        listeners = []
        for i in range(1, 11):
            u = User.objects.create_user(
                username=f'demo_listener{i}',
                email=f'listener{i}@demo.local',
                password='pass1234'
            )
            u.groups.add(listener_group)
            listeners.append(u)
        # 3 curator
        curators = []
        for i in range(1, 4):
            u = User.objects.create_user(
                username=f'demo_curator{i}',
                email=f'curator{i}@demo.local',
                password='pass1234'
            )
            u.groups.add(listener_group, curator_group)
            curators.append(u)

        self.stdout.write(" Creazione generi e canzoni…")
        genres = []
        for name in ('Rock', 'Pop', 'Jazz', 'Classical', 'Hip-Hop', 'Electronic'):
            genres.append(Genre.objects.create(name=name))
        # 50 canzoni
        songs = []
        for i in range(1, 51):
            g = random.choice(genres)
            s = Song.objects.create(
                title=f'Song {i}',
                artist=f'Artist {random.randint(1,20)}',
                genre=g,
                duration=timedelta(minutes=random.randint(2,5), seconds=random.randint(0,59))
            )
            songs.append(s)

        self.stdout.write(" Creazione playlist e condivisioni…")
        all_users = listeners + curators
        for u in all_users:
            for j in range(2):  # 2 playlist per utente
                pl = Playlist.objects.create(
                    name=f'{u.username} PL {j+1}',
                    owner=u
                )
                # aggiungo 5 canzoni random
                pl.songs.set(random.sample(songs, 5))
                # condivido con altri listener
                shared = random.sample([x for x in listeners if x!=u], k=3)
                pl.shared_with.set(shared)

        self.stdout.write(" Generazione raccomandazioni…")
        for u in all_users:
            top_songs = random.sample(songs, 10)
            for idx, s in enumerate(top_songs, start=1):
                Recommendation.objects.create(
                    user=u,
                    song=s,
                    score=round(random.uniform(0.1, 1.0), 2)
                )

        self.stdout.write(self.style.SUCCESS(" Dati demo creati con successo!"))
