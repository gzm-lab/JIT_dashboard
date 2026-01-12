"""
Wrapper pour l'agent DS-STAR de génération de code de visualisation.
Ce fichier sert d'interface entre Flask et DS-STAR.
"""
import os
import sys
import yaml
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

# Ajouter le dossier agent au path
sys.path.insert(0, os.path.dirname(__file__))

# Charger les variables d'environnement
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Importer DS-STAR
from dsstar import DS_STAR_Agent, DSConfig


class AgentWrapper:
    """
    Classe wrapper pour interfacer avec l'agent DS-STAR.
    """
    
    def __init__(self):
        """
        Initialise l'agent DS-STAR avec la configuration.
        """
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        self.data_path = os.path.join(os.path.dirname(__file__), 'data')
        self.agent = None
        
        # Charger la configuration
        self._load_config()
    
    def _load_config(self):
        """Charge la configuration depuis config.yaml"""
        try:
            with open(self.config_path, 'r') as f:
                config_dict = yaml.safe_load(f)
            
            # Créer la configuration DS-STAR
            self.ds_config = DSConfig(**config_dict)
            
            # Initialiser l'agent
            self.agent = DS_STAR_Agent(self.ds_config)
            
            print(f"✓ Agent DS-STAR initialisé avec le modèle: {self.ds_config.model_name}")
            
        except FileNotFoundError:
            print(f"⚠️  Fichier config.yaml non trouvé à {self.config_path}")
            print("   Utilisation du mode démo...")
            self.agent = None
        except Exception as e:
            print(f"⚠️  Erreur lors du chargement de la config: {e}")
            print("   Utilisation du mode démo...")
            self.agent = None
    
    def generate_visualization_code(self, question: str, data_files: Optional[list] = None) -> str:
        """
        Génère du code Python pour créer une visualisation basée sur la question.
        
        Args:
            question: La question posée par l'utilisateur
            data_files: Liste des fichiers de données à utiliser (optionnel)
            
        Returns:
            str: Code Python à exécuter pour générer la visualisation
        """
        
        # Si l'agent n'est pas configuré, utiliser le mode démo
        if self.agent is None:
            print("Mode démo actif (agent non configuré)")
            return self._generate_demo_code(question)
        
        try:
            # Si aucun fichier n'est spécifié, utiliser tous les fichiers du dossier data
            if data_files is None:
                data_files = self._get_data_files()
            
            if not data_files:
                print("⚠️  Aucun fichier de données trouvé")
                return self._generate_demo_code(question)
            
            # Lancer le pipeline DS-STAR
            print(f"🚀 Lancement de DS-STAR avec {len(data_files)} fichier(s)")
            result = self.agent.run_pipeline(query=question, data_files=data_files)
            
            # Extraire le code de la dernière étape
            steps = self.agent.storage.list_steps()
            if steps:
                last_step = steps[-1]
                step_data = self.agent.storage.get_step(last_step['step_id'])
                if step_data and step_data.get('code'):
                    code = step_data['code']
                    
                    # Adapter le code pour sauvegarder dans output_path
                    adapted_code = self._adapt_code_for_output(code)
                    return adapted_code
            
            print("⚠️  Aucun code généré par DS-STAR")
            return self._generate_demo_code(question)
            
        except Exception as e:
            print(f"❌ Erreur avec DS-STAR: {e}")
            print("   Basculement vers le mode démo...")
            return self._generate_demo_code(question)
    
    def _get_data_files(self) -> list:
        """Récupère la liste des fichiers de données disponibles"""
        data_dir = Path(self.data_path)
        if not data_dir.exists():
            return []
        
        # Trouver tous les fichiers CSV, XLSX, etc.
        extensions = ['.csv', '.xlsx', '.xls', '.json']
        files = []
        for ext in extensions:
            files.extend([f.name for f in data_dir.glob(f'*{ext}')])
        
        return files
    
    def _adapt_code_for_output(self, code: str) -> str:
        """
        Adapte le code généré pour sauvegarder dans output_path.
        """
        # Ajouter la sauvegarde si elle n'existe pas déjà
        if 'plt.savefig' not in code and 'savefig' not in code:
            code += "\n\n# Sauvegarder la visualisation\nplt.savefig(output_path, dpi=100, bbox_inches='tight')\nplt.close()\n"
        elif 'plt.savefig' in code:
            # Remplacer les chemins de sauvegarde existants par output_path
            code = code.replace("plt.savefig('", "plt.savefig(output_path if 'output_path' in dir() else '")
            code = code.replace('plt.savefig("', 'plt.savefig(output_path if "output_path" in dir() else "')
        
        return code
    
    def _generate_demo_code(self, question: str) -> str:
        """
        Génère un code de démonstration simple à partir du CSV test.csv.
        Utilisé quand DS-STAR n'est pas configuré.
        """
        return """
import matplotlib.pyplot as plt
import pandas as pd
import os

# Charger les données du CSV
data_path = os.path.join('/app', 'agent', 'data', 'test.csv')
df = pd.read_csv(data_path)

# Convertir la colonne date en datetime
df['date'] = pd.to_datetime(df['date'])

# Créer la figure
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['nombre'], 'b-o', linewidth=2, markersize=8)
plt.title(f'Évolution du nombre au fil du temps', fontsize=14, pad=20)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Nombre', fontsize=12)
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

# Sauvegarder
plt.savefig(output_path, dpi=100, bbox_inches='tight')
plt.close()
"""
