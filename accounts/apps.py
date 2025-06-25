# accounts/apps.py
from django.apps import AppConfig, apps
from django.db.models.signals import post_migrate

def assign_curator_permissions(sender, **kwargs):
    Group       = apps.get_model('auth', 'Group')
    Permission  = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Song        = apps.get_model('music', 'Song')
    Genre       = apps.get_model('music', 'Genre')

    curator_group, _ = Group.objects.get_or_create(name='Curator')

    # content types per Song e Genre
    song_ct  = ContentType.objects.get_for_model(Song)
    genre_ct = ContentType.objects.get_for_model(Genre)

    # tutte le permission di add/change/delete/view su Song e Genre
    perms = Permission.objects.filter(
        content_type__in=[song_ct, genre_ct],
        codename__in=[
            'add_song','change_song','delete_song','view_song',
            'add_genre','change_genre','delete_genre','view_genre'
        ]
    )
    # assegna
    curator_group.permissions.set(perms)

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        post_migrate.connect(assign_curator_permissions, sender=self)
