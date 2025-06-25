# accounts/migrations/0002_create_groups.py
from django.db import migrations

def create_groups_and_permissions(apps, schema_editor):
    Group       = apps.get_model('auth', 'Group')
    Permission  = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    # Modelli per cui assegnare permessi
    SongCT  = ContentType.objects.get(app_label='music', model='song')
    GenreCT = ContentType.objects.get(app_label='music', model='genre')
    PlCT    = ContentType.objects.get(app_label='music', model='playlist')
    RecCT   = ContentType.objects.get(app_label='music', model='recommendation')

    # Creazione gruppi
    listener, _ = Group.objects.get_or_create(name='Listener')
    curator,  _ = Group.objects.get_or_create(name='Curator')

    # Permessi da assegnare
    perms = {
        'Listener': [
            # view su tutto
            'view_song', 'view_genre', 'view_playlist', 'view_recommendation',
            # crud solo su playlist
            'add_playlist', 'change_playlist', 'delete_playlist',
        ],
        'Curator': [
            # include i permessi di Listener...
            'view_song', 'view_genre', 'view_playlist', 'view_recommendation',
            'add_playlist', 'change_playlist', 'delete_playlist',
            # ...e crud su song e genre
            'add_song', 'change_song', 'delete_song',
            'add_genre', 'change_genre', 'delete_genre',
        ],
    }

    # Helper per recuperare e assegnare
    ct_map = {
        'view_song':   SongCT, 'add_song':   SongCT, 'change_song':   SongCT, 'delete_song':   SongCT,
        'view_genre':  GenreCT,'add_genre':  GenreCT,'change_genre':  GenreCT,'delete_genre':  GenreCT,
        'view_playlist':  PlCT,'add_playlist':  PlCT,'change_playlist':  PlCT,'delete_playlist':  PlCT,
        'view_recommendation': RecCT,
    }

    # Assegna i permessi
    for group_name, codenames in perms.items():
        grp = listener if group_name=='Listener' else curator
        for codename in codenames:
            perm = Permission.objects.get(codename=codename, content_type=ct_map[codename])
            grp.permissions.add(perm)

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('music',    '0001_initial'),
        ('auth',     '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions),
    ]
