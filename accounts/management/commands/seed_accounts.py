import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from music.models import Playlist

class Command(BaseCommand):
    help = "Seed demo users: molti listener, pochi curator, e condividi le loro playlist"

    def handle(self, *args, **options):
        User = get_user_model()

        # Prendi i gruppi già creati dalle migrazioni
        listener_grp = Group.objects.get(name='Listener')
        curator_grp  = Group.objects.get(name='Curator')

        # Crea 5 curator
        curators = []
        for i in range(5):
            username = f'curator{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@example.com'}
            )
            if created:
                user.set_password('password123')
                user.save()
            user.groups.set([curator_grp])
            curators.append(user)

        # Crea 50 listener
        listeners = []
        for i in range(50):
            username = f'listener{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@example.com'}
            )
            if created:
                user.set_password('password123')
                user.save()
            user.groups.set([listener_grp])
            listeners.append(user)

        # Prendi tutte le playlist esistenti (seed_music ne creerà qualcuna)
        playlists = list(Playlist.objects.all())
        if not playlists:
            self.stdout.write(self.style.WARNING(
                "Non ho trovato playlist: esegui prima `seed_music` o crea manualmente qualche playlist."
            ))
        else:
            # Per ogni playlist, condividila con 2–5 utenti casuali (listener e qualche curator)
            for pl in playlists:
                # share with random listeners
                to_share = random.sample(listeners, k=random.randint(2, 5))
                for u in to_share:
                    pl.shared_with.add(u)
                # share with qualche curator
                for u in random.sample(curators, k=random.randint(1, 2)):
                    pl.shared_with.add(u)

        self.stdout.write(self.style.SUCCESS(" accounts seminati: listener, curator e condivisione playlist"))
