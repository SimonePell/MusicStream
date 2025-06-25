# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.models import Group

class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('listener', 'Listener'),
        ('curator',  'Curator'),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        label="Seleziona ruolo"
    )
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def save(self, commit=True):
        # salva l'utente
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            selected_role = self.cleaned_data['role']
            group_name = selected_role.capitalize()
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user