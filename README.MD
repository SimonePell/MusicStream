# Music Streaming Service

Un’applicazione web di streaming musicale realizzata con Django 4.2.

---

##  Sommario

- **Modelli**: Song, Genre, Playlist, Recommendation e UserProfile esteso.  
- **Autenticazione**: registrazione, login, profilo utente.  
- **Gruppi & Permessi**:  
  - **Listener**: naviga brani, crea/modifica/elimina le proprie playlist, vede raccomandazioni.  
  - **Curator**: tutto del Listener + crud su brani e generi.  
- **Funzionalità**:  
  - Elenco brani con ricerca full-text e filtro per genere.  
  - CRUD playlist: selezione brani in un pannello scrollabile, condivisione con altri utenti.  
  - Raccomandazioni personalizzate ordinate per score.  
  - CRUD generi (solo Curator).  
- **Profilo utente**: modifica la propria bio e visualizza statistiche di brani e playlist.
- **Stack**: Python 3.10+, Django ≥4.2, PostgreSQL (opzionale), Bootstrap 5.

---

##  Installazione

1. **Clona il repo**  

   git clone https://github.com/tuo-username/music-streaming-service.git

   cd music-streaming-service

   python3 -m venv venv

   source venv/bin/activate

   pip install -r requirements.txt

   copia .env.example in .env con:
   DJANGO_SECRET_KEY=tuo_secret_key
  DEBUG=True
  DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
  DATABASE_URL=postgresql://user:pass@localhost:5432/musicdb
   
   python manage.py migrate

   python manage.py seed_demo

   python manage.py createsuperuser

   python manage.py runserver

## Funzionalità

Browser: elenco e dettaglio brani, con ricerca full-text e filtro per genere.

Playlist: CRUD, selezione brani in un pannello scrollabile, condivisione con altri utenti.

Raccomandazioni: punteggio ordinato, pagina dedicata con ricerca.

Gestione generi: lista, aggiunta, modifica, cancellazione (solo Curator).

Profilo utente: visualizzazione dati e lista delle proprie playlist.
  
##  Credenziali Demo

Listener:

Username: demo_listener1

Password: qsxdr1234

Curator:

Username: demo_curator1

Password: qsxdr1234

 https://musicstream-production.up.railway.app/
