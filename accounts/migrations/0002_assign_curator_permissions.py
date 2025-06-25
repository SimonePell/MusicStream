# accounts/migrations/0002_assign_curator_permissions.py

from django.db import migrations

def assign_curator_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Song = apps.get_model('music', 'Song')
    Genre = apps.get_model('music', 'Genre')

    # prendi o crea il gruppo Curator
    curator_group, _ = Group.objects.get_or_create(name='Curator')

    # trova i content types di Song e Genre
    song_ct  = ContentType.objects.get_for_model(Song)
    genre_ct = ContentType.objects.get_for_model(Genre)

    # filtra i permessi da assegnare
    perms = Permission.objects.filter(
        content_type__in=[song_ct, genre_ct],
        codename__in=[
            'add_song', 'change_song', 'delete_song', 'view_song',
            'add_genre', 'change_genre', 'delete_genre', 'view_genre'
        ]
    )

    # assegna al gruppo Curator
    curator_group.permissions.set(perms)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('music',    '0001_initial'),
    ]

    operations = [
        migrations.RunPython(assign_curator_permissions, reverse_code=migrations.RunPython.noop),
    ]
