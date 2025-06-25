# music_streaming/views.py
from django.shortcuts import redirect

def home(request):
    # reindirizza subito all'elenco canzoni
    return redirect('music:song-list')
