# Projet Communes API

## Description

Ce projet implémente une API FastAPI pour gérer les informations des communes françaises. Il utilise SQLite comme base de données et offre plusieurs fonctionnalités via ses endpoints.

## Installation

1. Installer les dépendances Python :
    ```bash
    pip install uvicorn fastapi
    ```

2. Pour démarrer l'API, naviguez jusqu'au dossier de l'application et exécutez :
    ```bash
    python -m uvicorn main:app --reload
    ```

## Utilisation

L'API fournit plusieurs endpoints :

- **Obtenir les informations d'une commune** :
  `http://localhost:8000/communes/{nom_commune}`

- **Lister les communes d'un département** :
  `http://localhost:8000/departements/{num_departement}/communes`

- **Ajouter une commune** :
  Utilisez `curl` ou `Invoke-RestMethod` pour les utilisateurs de PowerShell :
  ```powershell
  Invoke-RestMethod -Method Post -Uri "http://localhost:8000/communes" -ContentType "application/json" -Body '{"code_postal": "75001", "nom_commune": "Paris", "departement": "75"}'

Dockerisation

Le projet est dockerisé avec deux services principaux :

    Service FastAPI : Exécute l'application FastAPI.
    Service Pelias : Sert pour le géocodage des communes.

Pour démarrer les services, utilisez :

bash

docker-compose up

Notes Supplémentaires

    L'API a été testée localement et via Docker.
    Utilisez SQLiteBrowser pour inspecter la base de données.
    Un script creation_bdd.py séparé est utilisé pour le processus ETL.

Conclusion

Ce projet offre une approche simple et efficace pour gérer les informations des communes, en utilisant FastAPI, Docker, et Pelias pour le géocodage.



Ce `README.md` résume le projet et fournit des instructions claires sur comment l'installer, l'utiliser, et les technologies utilisées.
