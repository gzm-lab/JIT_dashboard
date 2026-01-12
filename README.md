# JIT_BI

Application web pour générer des visualisations de données via un agent conversationnel.

## Structure du Projet

```
JIT_BI/
├── app/                    # Application Flask
│   ├── main.py            # Point d'entrée Flask
│   ├── static/            # Assets statiques (CSS, JS)
│   └── templates/         # Templates HTML
├── agent/                 # Module agent
│   ├── agent_wrapper.py   # Interface avec l'agent
│   └── data/              # Données pour l'agent
├── output/                # Visualisations générées
├── Dockerfile            # Image Docker
├── docker-compose.yml    # Orchestration
└── requirements.txt      # Dépendances Python
```

## Backend Implémenté

### Endpoints API

- **GET /** : Page principale
- **POST /ask** : Envoie une question, retourne une visualisation
  - Body: `{ "question": "..." }`
  - Response: `{ "status": "success", "image_url": "/output/viz_xxx.png" }`
- **GET /output/<filename>** : Sert les images générées
- **GET /health** : Santé de l'application

### Agent Wrapper

Le fichier `agent/agent_wrapper.py` contient une classe `AgentWrapper` à adapter avec ton agent existant :

```python
def generate_visualization_code(self, question: str) -> str:
    # TODO: Remplacer par ton agent réel
    # code = self.agent.generate_code(question)
    # return code
```

Le code généré doit utiliser la variable `output_path` pour sauvegarder l'image.

## Installation et Lancement

### Avec Docker (recommandé)

```bash
# Build
docker-compose build

# Lancer
docker-compose up

# Accès
http://localhost:8080
```

### Sans Docker (développement)

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer
python app/main.py
```

## Prochaines Étapes

1. **Intégrer ton agent** : Modifier `agent/agent_wrapper.py`
2. **Ajouter tes données** : Placer les fichiers dans `agent/data/`
3. **Frontend** : Créer l'interface utilisateur (chat + visualisation)

## Configuration

- Port : 8080
- Output : `./output/`
- Data : `./agent/data/`
