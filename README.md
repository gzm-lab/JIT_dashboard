# 📊 JIT Dashboard — BI Conversationnelle par IA

Un tableau de bord **Business Intelligence** piloté par le langage naturel. Pose une question sur tes données en français (ou anglais), l'agent IA génère et exécute automatiquement le code de visualisation, et renvoie un graphique prêt à l'emploi.

Propulsé par **DS-STAR** — un pipeline multi-agents LLM (Gemini, OpenAI ou Ollama local) qui analyse, planifie, code, vérifie et débogue de façon autonome.

## ✨ Fonctionnalités

- 💬 **Interface conversationnelle** — pose tes questions en langage naturel
- 🤖 **Pipeline multi-agents DS-STAR** — 7 agents spécialisés (Analyzer, Planner, Coder, Verifier, Router, Debugger, Finalyzer)
- 📈 **Visualisations automatiques** — matplotlib, plotly, seaborn
- 📂 **Multi-formats** — CSV, Excel (.xlsx), JSON
- 🔄 **Auto-debug** — l'agent corrige ses propres erreurs de code (jusqu'à 3 tentatives)
- 🐳 **Dockerisé** — déploiement en une commande

## 🧠 Architecture

```
Utilisateur (question)
        ↓
   Flask API (/ask)
        ↓
  AgentWrapper
        ↓
  ┌─────────────────────────────────────┐
  │        DS-STAR Pipeline             │
  │                                     │
  │  ANALYZER → analyse les données     │
  │  PLANNER  → planifie les étapes     │
  │  CODER    → génère le code Python   │
  │  VERIFIER → vérifie le résultat     │
  │  ROUTER   → ajuste le plan          │
  │  DEBUGGER → corrige les erreurs     │
  │  FINALYZER→ produit l'output final  │
  └─────────────────────────────────────┘
        ↓
  exec() → image PNG générée
        ↓
  URL renvoyée → affichage dans le navigateur
```

## 🚀 Quick Start

### Option 1 — Docker (recommandé)

```bash
git clone https://github.com/gzm-lab/JIT_dashboard.git
cd JIT_dashboard

# Configure les variables d'environnement
cp agent/.env.template agent/.env
# Édite agent/.env avec ta clé API (Gemini, OpenAI, ou config Ollama)

docker compose up -d
```

L'interface est disponible sur **http://localhost:5000**

### Option 2 — Local

```bash
git clone https://github.com/gzm-lab/JIT_dashboard.git
cd JIT_dashboard

pip install -r requirements.txt

# Configure
cp agent/.env.template agent/.env
# Édite agent/.env

# Lance
python app/main.py
```

## ⚙️ Configuration

Édite `agent/.env` et `agent/config.yaml` :

```env
# Choix du provider LLM
GOOGLE_API_KEY=ta_cle_gemini      # Pour Gemini (défaut)
OPENAI_API_KEY=ta_cle_openai      # Pour GPT-4
# Ollama : aucune clé requise, configure OLLAMA_HOST dans config.yaml
```

```yaml
# agent/config.yaml
model: gemini-1.5-flash   # ou gpt-4, ollama/llama3

settings:
  max_refinement_rounds: 5
  auto_debug: true
  debug_attempts: 3
  execution_timeout: 60
```

### Providers LLM supportés

| Provider | Modèle | Variable |
|---|---|---|
| Google Gemini | `gemini-1.5-flash` (défaut) | `GOOGLE_API_KEY` |
| OpenAI | `gpt-4`, `gpt-4o` | `OPENAI_API_KEY` |
| Ollama (local) | `ollama/llama3`, etc. | aucune |

## 📡 API

| Méthode | Route | Description |
|---|---|---|
| `GET` | `/` | Interface web principale |
| `POST` | `/ask` | Envoie une question → reçoit l'URL du graphique |
| `GET` | `/output/<filename>` | Télécharge/affiche une image générée |
| `GET` | `/health` | Vérification de santé |

**Exemple `/ask` :**

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Montre-moi les ventes par mois sous forme de graphique à barres"}'

# Réponse
{"image_url": "/output/chart_abc123.png"}
```

## 📂 Structure

```
JIT_dashboard/
├── app/
│   ├── main.py              # Flask — API et serveur web
│   └── templates/index.html # Interface chat
├── agent/
│   ├── dsstar.py            # Pipeline DS-STAR multi-agents (cœur du projet)
│   ├── agent_wrapper.py     # Bridge Flask ↔ DS-STAR
│   ├── config.yaml          # Configuration LLM et pipeline
│   ├── prompt.yaml          # Prompts des agents
│   ├── provider.py          # Abstraction des providers LLM
│   └── data/                # Dossier de données (CSV, XLSX, JSON)
│       └── test.csv         # Exemple de données
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── SETUP_DSSTAR.md          # Guide de configuration DS-STAR
└── architecture.md          # Documentation d'architecture détaillée
```

## 📊 Ajouter ses données

Dépose tes fichiers de données dans `agent/data/` :

```bash
cp mes_donnees.csv agent/data/
cp rapport_ventes.xlsx agent/data/
```

L'agent détecte automatiquement tous les fichiers CSV, XLSX et JSON présents dans ce dossier.

## 🛠️ Stack technique

| Composant | Technologie |
|---|---|
| Backend | Python + Flask |
| LLM | Gemini 1.5 Flash / GPT-4 / Ollama |
| Visualisation | matplotlib, plotly, seaborn |
| Data | pandas, numpy, openpyxl |
| Conteneurisation | Docker + Docker Compose |
