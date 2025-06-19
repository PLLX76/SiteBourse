# Site de Bourse Simplifié

Ce projet est un site web simple qui permet d'afficher des informations boursières en utilisant Flask pour le backend et HTML pour le frontend. Il n'utilise pas de base de données et se base sur le web scraping pour récupérer les données boursières en temps réel.

## Fonctionnalités

- Affichage des cours de bourses actuels.
- Web scraping pour la récupération des données.

## Sites Supportés

- JustETF
- Boursier.com
- Boursorama

## Technologies Utilisées

- **Backend:** Flask (Python)
- **Frontend:** HTML
- **Web Scraping:** Cloudscraper (Python)

## Installation

1. **Cloner le dépôt:**

   ```bash
   git clone https://github.com/PLLX76/SiteBourse.git
   cd SiteBourse
   ```

2. **Créer un environnement virtuel (recommandé):**

   ```bash
   python -m venv env
   ```

3. **Activer l'environnement virtuel:**

   - Sur Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - Sur macOS et Linux:
     ```bash
     source env/bin/activate
     ```

4. **Installer les dépendances:**
   ```bash
   pip install -r requirements.txt
   ```
   _(Un fichier `requirements.txt` sera créé contenant les dépendances nécessaires comme `Flask` et les bibliothèques de scraping)_

## Utilisation

1. **Exécuter l'application Flask:**

   ```bash
   python main.py
   ```

2. **Accéder au site web:**
   Ouvrez votre navigateur et accédez à `http://127.0.0.1:5000/` (ou l'adresse et le port indiqués par Flask).
