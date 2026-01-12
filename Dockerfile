FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les requirements et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app/ ./app/
COPY agent/ ./agent/

# Créer les dossiers nécessaires
RUN mkdir -p /app/output /app/agent/data /app/agent/runs /app/agent/code_library

# Exposer le port Flask
EXPOSE 8080

# Variables d'environnement
ENV FLASK_APP=app/main.py
ENV PYTHONUNBUFFERED=1

# Lancer l'application
CMD ["python", "app/main.py"]
