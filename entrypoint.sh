#!/bin/sh

# Exécuter le script ETL
python /app/creation_bdd.py

# Démarrer l'application FastAPI
exec uvicorn main:app --host 0.0.0.0 --port 80
