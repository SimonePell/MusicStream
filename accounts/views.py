from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegistrationForm
from .models import UserProfile

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['bio']
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user.profile