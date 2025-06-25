from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', home, name='home'),               # ← la tua home
    path('app/', include('music.urls', namespace='music')),  # oppure sposta music qui
]
