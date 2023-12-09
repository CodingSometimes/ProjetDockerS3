# Utiliser une image de base Python
FROM python:3.9

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances et les installer
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copier le reste du code source
COPY . /app/

# Exposer le port sur lequel l'application s'exécute
EXPOSE 6969

# Commande pour créer et appliquer les migrations
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
# Commande pour lancer l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:6969"]
