# accounts/migrations/0002_create_groups.py
from django.db import migrations

def create_groups_and_permissions(apps, schema_editor):
    Group       = apps.get_model('auth', 'Group')
    Permission  = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    # Assicuriamoci di avere un ContentType valido, anche se mancasse:
    SongCT, _  = ContentType.objects.get_or_create(app_label='music', model='song')
    GenreCT, _ = ContentType.objects.get_or_create(app_label='music', model='genre')
    PlCT, _    = ContentType.objects.get_or_create(app_label='music', model='playlist')
    RecCT, _   = ContentType.objects.get_or_create(app_label='music', model='recommendation')

    listener, _ = Group.objects.get_or_create(name='Listener')
    curator,  _ = Group.objects.get_or_create(name='Curator')

    perms = {
        'Listener': [
            'view_song','view_genre','view_playlist','view_recommendation',
            'add_playlist','change_playlist','delete_playlist',
        ],
        'Curator': [
            'view_song','view_genre','view_playlist','view_recommendation',
            'add_playlist','change_playlist','delete_playlist',
            'add_song','change_song','delete_song',
            'add_genre','change_genre','delete_genre',
        ],
    }
    ct_map = {
        'view_song':SongCT, 'add_song':SongCT, 'change_song':SongCT, 'delete_song':SongCT,
        'view_genre':GenreCT,'add_genre':GenreCT,'change_genre':GenreCT,'delete_genre':GenreCT,
        'view_playlist':PlCT,'add_playlist':PlCT,'change_playlist':PlCT,'delete_playlist':PlCT,
        'view_recommendation':RecCT,
    }

    for group_name, codenames in perms.items():
        grp = listener if group_name=='Listener' else curator
        for codename in codenames:
            # Se per qualche motivo il permesso non esiste, lo saltiamo
            try:
                perm = Permission.objects.get(codename=codename, content_type=ct_map[codename])
                grp.permissions.add(perm)
            except Permission.DoesNotExist:
                pass

class Migration(migrations.Migration):

    dependencies = [
    ('contenttypes', '0001_initial'),
    ('music',       '0001_initial'),
    ('accounts',    '0001_initial'),
    ('auth',        '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions),
    ]
