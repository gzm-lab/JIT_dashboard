# Instructions pour télécharger les fichiers DS-STAR

Télécharge les fichiers suivants depuis le repo GitHub et place-les dans le dossier `agent/` :

1. **dsstar.py** (fichier principal)
   - URL: https://raw.githubusercontent.com/JulesLscx/DS-Star/main/dsstar.py
   - Destination: `/Users/gabriel/Desktop/JIT_BI/agent/dsstar.py`

2. **provider.py** (providers pour les modèles)
   - URL: https://raw.githubusercontent.com/JulesLscx/DS-Star/main/provider.py
   - Destination: `/Users/gabriel/Desktop/JIT_BI/agent/provider.py`

3. **prompt.yaml** (prompts pour les agents)
   - URL: https://raw.githubusercontent.com/JulesLscx/DS-Star/main/prompt.yaml
   - Destination: `/Users/gabriel/Desktop/JIT_BI/agent/prompt.yaml`

## Commandes rapides

```bash
cd /Users/gabriel/Desktop/JIT_BI/agent

# Télécharger dsstar.py
curl -o dsstar.py https://raw.githubusercontent.com/JulesLscx/DS-Star/main/dsstar.py

# Télécharger provider.py
curl -o provider.py https://raw.githubusercontent.com/JulesLscx/DS-Star/main/provider.py

# Télécharger prompt.yaml
curl -o prompt.yaml https://raw.githubusercontent.com/JulesLscx/DS-Star/main/prompt.yaml
```

Une fois téléchargés, configure tes clés API dans `.env` et `config.yaml`.
