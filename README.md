# Gestion d'Hôtel API avec FastAPI et Docker

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)

## Description

Ce projet est une API de gestion d'hôtel développée en Python avec le framework FastAPI. L'API permet de gérer les clients, les chambres, les hôtels et les réservations dans un système de gestion d'hôtel. L'application utilise une base de données SQLite pour stocker les informations des clients, des chambres et des réservations.

## Prérequis

Avant de lancer l'application, assurez-vous d'avoir installé Docker sur votre système. Si vous n'avez pas encore installé Docker, vous pouvez le télécharger à partir du site officiel de Docker : [https://www.docker.com/](https://www.docker.com/)

## Installation

1. Clonez le dépôt :

```bash
git clone https://github.com/VOTRE_NOM_UTILISATEUR/NOM_DU_DEPOT.git
cd NOM_DU_DEPOT
```
2. Construisez l'image Docker :
```bash
docker build -t hotel-gest-api .
```
3. Construisez l'image Docker :
```bash
docker run  -p 8080:80 --name hotel-gest-app hotel-gest-api
```
L'application FastAPI sera maintenant accessible à l'adresse `http://localhost:8080/docs` sur votre navigateur.

L'API FastAPI de gestion d'hôtel fournit les endpoints suivants pour l'entité Client par exemple :

-   `/AjouterClient` : Ajouter un nouveau client à la base de données.
-   `/ListerClient` : Lister tous les clients enregistrés.
-   `/Client` : Obtenir les détails d'un client par son identifiant ou son email.
-   `/Client/{client_id}` : Mettre à jour les informations d'un client existant.


Consultez la documentation interactive Swagger à l'adresse `http://localhost:80/docs` pour plus de détails sur les points d'extrémité, les paramètres et les réponses.

## Auteur

Ce projet a été développé par Espoir HOUEDJI

