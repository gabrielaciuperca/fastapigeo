# Utiliser une image de base Python
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY ./requirements.txt /app/requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copier le reste du code de l'application dans le conteneur
COPY . /app

# Donner les droits d'exécution au script ETL et au script d'entrée
COPY creation_bdd.py /app/creation_bdd.py
RUN chmod +x /app/creation_bdd.py
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Définir le script d'entrée comme point d'entrée
ENTRYPOINT ["/app/entrypoint.sh"]
