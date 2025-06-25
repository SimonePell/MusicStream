from django.conf import settings
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Song(models.Model):
    title    = models.CharField(max_length=200)
    artist   = models.CharField(max_length=200)
    genre    = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='songs')
    duration = models.DurationField()

    def __str__(self):
        return f"{self.title} – {self.artist}"

class Playlist(models.Model):
    name       = models.CharField(max_length=200)
    owner      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlists')
    songs      = models.ManyToManyField(Song, blank=True, related_name='playlists')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.owner.username}"

class Recommendation(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations')
    song  = models.ForeignKey(Song, on_delete=models.CASCADE)
    score = models.FloatField(default=0)

    class Meta:
        unique_together = ('user', 'song')
