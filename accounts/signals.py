from django.apps import AppConfig, apps
from django.db.models.signals import post_migrate

def assign_curator_perms(sender, **kwargs):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Song  = apps.get_model('music', 'Song')
    Genre = apps.get_model('music', 'Genre')

    curator, _ = Group.objects.get_or_create(name='Curator')
    song_ct  = ContentType.objects.get_for_model(Song)
    genre_ct = ContentType.objects.get_for_model(Genre)

    perms = Permission.objects.filter(
        content_type__in=[song_ct, genre_ct],
        codename__in=[
            'add_song','change_song','delete_song','view_song',
            'add_genre','change_genre','delete_genre','view_genre'
        ]
    )
    curator.permissions.set(perms)

class AccountsConfig(AppConfig):
    name = 'accounts'
    def ready(self):
        post_migrate.connect(assign_curator_perms, sender=self)
