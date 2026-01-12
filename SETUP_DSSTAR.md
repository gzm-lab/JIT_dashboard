# JIT_BI - Configuration DS-STAR

## 🚀 Quick Start

### 1. Configuration de DS-STAR

Avant de lancer l'application, tu dois configurer DS-STAR :

#### a) Créer ton fichier `.env`

```bash
cd agent
cp .env.template .env
```

Puis édite `agent/.env` et ajoute ta clé API :

```bash
# Pour Gemini (par défaut)
GEMINI_API_KEY=ta-clé-api-ici

# OU pour OpenAI
OPENAI_API_KEY=ta-clé-api-ici

# OU pour Ollama (local)
OLLAMA_HOST=http://localhost:11434
```

#### b) Configurer `config.yaml`

Édite `agent/config.yaml` et personnalise :

```yaml
model_name: 'gemini-1.5-flash'  # ou 'gpt-4', 'ollama/llama3'
max_refinement_rounds: 5
auto_debug: true
```

### 2. Ajouter tes données

Place tes fichiers de données dans `agent/data/` :
- Formats supportés: CSV, XLSX, XLS, JSON
- Exemple déjà fourni: `test.csv`

### 3. Lancer l'application

```bash
docker-compose up --build
```

Accède à http://localhost:8080

## 🎯 Fonctionnement

1. **Sans configuration** : Mode démo avec `test.csv`
2. **Avec configuration** : DS-STAR analyse tes données et génère du code automatiquement

## 📁 Structure

```
JIT_BI/
├── agent/
│   ├── config.yaml          # ⚙️ Configuration DS-STAR
│   ├── .env                 # 🔐 Clés API (à créer)
│   ├── data/                # 📊 Tes données
│   ├── runs/                # 📁 Historique DS-STAR
│   ├── dsstar.py            # 🤖 Agent DS-STAR
│   ├── provider.py          # 🔌 Providers AI
│   └── prompt.yaml          # 💬 Prompts agents
├── app/                     # 🌐 Application Flask
└── output/                  # 📈 Visualisations générées
```

## 🔧 Modes de fonctionnement

### Mode Démo (sans config)
- Utilise `test.csv`
- Génère des graphiques simples
- Parfait pour tester l'interface

### Mode DS-STAR (avec config)
- Analyse intelligente des données
- Génération de code automatique
- Visualisations personnalisées selon ta question

## 📚 Documentation DS-STAR

Voir : https://github.com/JulesLscx/DS-Star

## ⚡ Commandes utiles

```bash
# Rebuild complet
docker-compose down && docker-compose up --build

# Voir les logs
docker-compose logs -f

# Nettoyer les runs DS-STAR
rm -rf agent/runs/*

# Nettoyer les visualisations
rm -rf output/*.png
```

## 🐛 Troubleshooting

**L'agent ne démarre pas** :
- Vérifie que `agent/.env` existe et contient ta clé API
- Vérifie `agent/config.yaml` (model_name doit être défini)

**Erreur avec DS-STAR** :
- L'application bascule automatiquement en mode démo
- Vérifie les logs avec `docker-compose logs`

**Visualisation non générée** :
- Vérifie que tes fichiers sont dans `agent/data/`
- Vérifie les formats supportés (CSV, XLSX, JSON)
