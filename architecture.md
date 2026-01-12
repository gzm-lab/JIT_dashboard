# Architecture du Projet JIT_BI

## Vue d'ensemble
Application web simple permettant d'interagir avec un agent via un chat pour générer et afficher des visualisations de données.

## Stack Technique

### Backend
- **Framework** : Flask (léger et simple)
- **Langage** : Python 3.11+
- **Exécution** : Confiance totale, exécution directe du code généré

### Frontend
- **Technologies** : HTML/CSS/JavaScript vanilla
- **Interface** : Page unique avec chat input + zone d'affichage

### Visualisations
- **Librairies** : Flexible (matplotlib, plotly, seaborn, etc.)
- **Format** : Images (PNG/SVG) générées côté backend

### Infrastructure
- **Containerisation** : Docker + docker-compose
- **Stockage des données** : Dossier local `agent/data/`
- **Persistance** : Aucune (pas d'historique)

## Structure du Projet

```
JIT_BI/
├── docker-compose.yml       # Orchestration Docker
├── Dockerfile              # Image Docker de l'application
├── requirements.txt        # Dépendances Python
├── app/
│   ├── __init__.py
│   ├── main.py            # Application Flask principale
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css  # Styles de l'interface
│   │   └── js/
│   │       └── main.js    # Logique frontend (chat, affichage)
│   └── templates/
│       └── index.html     # Interface utilisateur unique
├── agent/
│   ├── __init__.py
│   ├── agent_core.py      # Agent existant (génération de code)
│   └── data/              # Données utilisées par l'agent
└── output/                 # Visualisations générées (temporaire)
```

## Flux de Fonctionnement

1. **Input Utilisateur**
   - L'utilisateur saisit une question dans le chat
   - Envoi via requête POST au backend

2. **Traitement Backend**
   - Flask reçoit la question via `POST /ask`
   - Appel à l'agent avec la question

3. **Génération de Code**
   - L'agent génère du code Python de visualisation
   - Le code accède aux données dans `agent/data/`

4. **Exécution**
   - Exécution directe du code avec `exec()` (environnement de confiance)
   - Génération d'une image dans le dossier `output/`

5. **Affichage**
   - Retour de l'URL de l'image au frontend
   - Affichage de la visualisation dans la zone dédiée

## Endpoints API

### `GET /`
- Page principale de l'application
- Retourne `index.html` avec l'interface chat

### `POST /ask`
- Reçoit la question de l'utilisateur
- **Body** : `{ "question": "..." }`
- **Response** : `{ "image_url": "/output/viz_xxxxx.png", "status": "success" }`

### `GET /output/<filename>`
- Sert les images de visualisation générées
- Fichiers statiques depuis le dossier `output/`

## Sécurité

- **Exécution de code** : Confiance totale, pas de sandbox
- **Environnement** : Privé, utilisateurs de confiance
- **Validation** : Aucune validation du code généré

## Gestion des Données

- **Stockage** : Fichiers dans `agent/data/`
- **Accès** : L'agent lit directement depuis ce dossier
- **Persistance** : Aucune base de données
- **Historique** : Pas de conservation des conversations
- **Visualisations** : Fichiers temporaires, peuvent être écrasés

## Déploiement

### Docker
- Image unique contenant Flask + Agent + Dépendances
- Volumes pour `agent/data/` et `output/`
- Port exposé : 5000 (Flask)

### Commandes
```bash
# Build
docker-compose build

# Run
docker-compose up

# Accès
http://localhost:5000
```

## Technologies et Dépendances

### Backend
- Flask
- Librairies de visualisation (matplotlib, plotly, seaborn, etc.)
- Dépendances de l'agent

### Frontend
- Pas de dépendances externes
- JavaScript vanilla
- CSS pur

## Évolutions Futures Possibles

- Ajout d'un historique de conversation (session)
- Support de multiples types de visualisations
- Export des visualisations
- Interface d'administration
- Authentification utilisateur
