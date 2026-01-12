// Elements DOM
const chatForm = document.getElementById('chat-form');
const questionInput = document.getElementById('question-input');
const chatMessages = document.getElementById('chat-messages');
const visualizationImg = document.getElementById('visualization');
const placeholder = document.getElementById('placeholder');
const loading = document.getElementById('loading');
const errorContainer = document.getElementById('error-container');
const errorText = document.getElementById('error-text');
const sendButton = chatForm.querySelector('.send-button');

// État de l'application
let isProcessing = false;

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    // Focus sur l'input au chargement
    questionInput.focus();
    
    // Ajouter un message de bienvenue
    addBotMessage("Bonjour ! Posez-moi une question pour générer une visualisation.");
});

// Gestion de la soumission du formulaire
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (isProcessing) return;
    
    const question = questionInput.value.trim();
    if (!question) return;
    
    // Désactiver l'input pendant le traitement
    isProcessing = true;
    questionInput.disabled = true;
    sendButton.disabled = true;
    
    // Ajouter le message de l'utilisateur
    addUserMessage(question);
    
    // Vider l'input
    questionInput.value = '';
    
    // Afficher le loading
    showLoading();
    
    try {
        // Envoyer la question à l'API
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question }),
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            // Afficher la visualisation
            displayVisualization(data.image_url);
            addBotMessage("Voici votre visualisation !");
        } else {
            throw new Error(data.message || 'Erreur lors de la génération');
        }
        
    } catch (error) {
        console.error('Erreur:', error);
        showError(error.message || 'Une erreur est survenue');
        addBotMessage("Désolé, je n'ai pas pu générer la visualisation.");
        hideLoading();
    } finally {
        // Réactiver l'input
        isProcessing = false;
        questionInput.disabled = false;
        sendButton.disabled = false;
        questionInput.focus();
    }
});

// Ajouter un message utilisateur
function addUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Ajouter un message bot
function addBotMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Faire défiler vers le bas
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Afficher le loading
function showLoading() {
    placeholder.style.display = 'none';
    visualizationImg.style.display = 'none';
    loading.style.display = 'block';
}

// Cacher le loading
function hideLoading() {
    loading.style.display = 'none';
}

// Afficher la visualisation
function displayVisualization(imageUrl) {
    hideLoading();
    placeholder.style.display = 'none';
    
    // Ajouter un timestamp pour éviter le cache
    const timestamp = new Date().getTime();
    visualizationImg.src = `${imageUrl}?t=${timestamp}`;
    visualizationImg.style.display = 'block';
    
    // Gérer les erreurs de chargement d'image
    visualizationImg.onerror = () => {
        showError('Impossible de charger la visualisation');
        visualizationImg.style.display = 'none';
        placeholder.style.display = 'block';
    };
}

// Afficher une erreur
function showError(message) {
    errorText.textContent = message;
    errorContainer.style.display = 'block';
    
    // Masquer automatiquement après 5 secondes
    setTimeout(() => {
        closeError();
    }, 5000);
}

// Fermer l'erreur
function closeError() {
    errorContainer.style.display = 'none';
}

// Gérer les touches du clavier
questionInput.addEventListener('keydown', (e) => {
    // Permettre Shift+Enter pour les sauts de ligne (si on veut)
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});
