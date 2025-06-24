from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class User(AbstractUser):
    # Ereditiamo tutti i campi di AbstractUser (username, email, password) e potremmo aggiungerne di nuovi in futuro
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    # eventuali campi aggiuntivi: foto, preferenze

    def __str__(self):
        return f"Profilo di {self.user.username}"

# Signal: crea automaticamente il profilo quando si registra un nuovo User\@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Signal: salva il profilo ogni volta che si salva l'User\@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()