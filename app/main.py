import os
import uuid
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import sys

# Ajouter le dossier parent au path pour l'import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agent.agent_wrapper import AgentWrapper

app = Flask(__name__)
CORS(app)

# Configuration
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'output')
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Initialiser l'agent
agent = AgentWrapper()


@app.route('/')
def index():
    """Page principale avec l'interface chat"""
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    """
    Endpoint pour envoyer une question à l'agent
    Reçoit: { "question": "..." }
    Retourne: { "image_url": "/output/viz_xxxxx.png", "status": "success" }
    """
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({
                'status': 'error',
                'message': 'Question vide'
            }), 400
        
        # Générer un nom de fichier unique pour la visualisation
        filename = f"viz_{uuid.uuid4().hex[:8]}.png"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        # Appeler l'agent pour générer le code de visualisation
        code = agent.generate_visualization_code(question)
        
        # Exécuter le code généré
        # On passe le chemin de sortie au code via une variable globale
        exec_globals = {
            'output_path': output_path,
            '__name__': '__main__'
        }
        
        # Exécuter le code (confiance totale)
        exec(code, exec_globals)
        
        # Vérifier que le fichier a été créé
        if not os.path.exists(output_path):
            return jsonify({
                'status': 'error',
                'message': 'La visualisation n\'a pas été générée'
            }), 500
        
        # Retourner l'URL de l'image
        return jsonify({
            'status': 'success',
            'image_url': f'/output/{filename}'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/output/<filename>')
def serve_output(filename):
    """Servir les fichiers de visualisation générés"""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


@app.route('/health')
def health():
    """Endpoint de santé pour vérifier que l'application fonctionne"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    # Créer le dossier output s'il n'existe pas
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Lancer l'application
    app.run(host='0.0.0.0', port=8080, debug=True)
