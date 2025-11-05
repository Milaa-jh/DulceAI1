// DulceAI - Chatbot JavaScript con integración real de IA

// Variables globales del chatbot
let chatOpen = false;
let messageHistory = [];
let aiStatus = null;

// Configuración del backend
const BACKEND_URL = 'http://localhost:8000';

// Inicialización del chatbot cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initializeChatbot();
    checkAISystemStatus();
});

// Función principal de inicialización del chatbot
function initializeChatbot() {
    const chatIcon = document.getElementById('chatbot-icon');
    const chatWindow = document.getElementById('chatbot-window');
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    if (!chatIcon || !chatWindow || !sendBtn || !userInput || !chatMessages) {
        console.error('Elementos del chatbot no encontrados');
        return;
    }

    // Event listener para abrir/cerrar el chat
    chatIcon.addEventListener('click', toggleChat);
    
    // Event listener para enviar mensaje
    sendBtn.addEventListener('click', sendMessage);
    
    // Event listener para enviar con Enter
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Animación inicial del ícono del chatbot
    gsap.fromTo(chatIcon, {
        scale: 0,
        rotation: -180
    }, {
        scale: 1,
        rotation: 0,
        duration: 1,
        ease: 'back.out(1.7)',
        delay: 2
    });

    // Agregar mensaje de bienvenida
    addWelcomeMessage();
}

// Función para verificar el estado del sistema de IA
async function checkAISystemStatus() {
    try {
        console.log('🔍 Verificando estado del sistema de IA...');
        const response = await fetch(`${BACKEND_URL}/api/ai/status`);
        const status = await response.json();
        
        aiStatus = status;
        console.log('📊 Estado del sistema de IA:', status);
        
        // Solo permitir chat si la IA está disponible Y inicializada
        if (status.ai_available && status.initialized && status.dependencies_available) {
            console.log('✅ Sistema de IA completamente operativo');
            updateChatbotStatus('active');
            enableChat();
        } else {
            console.log('❌ Sistema de IA no disponible o no inicializado');
            updateChatbotStatus('unavailable');
            disableChat('Sistema de IA no disponible. El chatbot está deshabilitado.');
        }
        
    } catch (error) {
        console.error('❌ Error verificando estado de IA:', error);
        updateChatbotStatus('connection_error', error.message);
        disableChat('No se pudo verificar el estado del sistema de IA.');
    }
}

// Función para actualizar el estado visual del chatbot
function updateChatbotStatus(status, error = null) {
    const chatIcon = document.getElementById('chatbot-icon');
    const chatHeader = document.querySelector('.chat-header');
    
    if (!chatIcon || !chatHeader) return;
    
    switch (status) {
        case 'active':
            chatIcon.innerHTML = '🤖';
            chatHeader.textContent = 'DulceAI Asistente (IA Activa)';
            chatHeader.style.background = 'linear-gradient(135deg, #10b981, #059669)';
            break;
        case 'error':
            chatIcon.innerHTML = '⚠️';
            chatHeader.textContent = 'DulceAI Asistente (Error IA)';
            chatHeader.style.background = 'linear-gradient(135deg, #f59e0b, #d97706)';
            console.error('❌ Error del sistema de IA:', error);
            break;
        case 'unavailable':
            chatIcon.innerHTML = '💬';
            chatHeader.textContent = 'DulceAI Asistente';
            chatHeader.style.background = 'linear-gradient(135deg, #ec4899, #be185d)';
            break;
        case 'connection_error':
            chatIcon.innerHTML = '🔌';
            chatHeader.textContent = 'DulceAI Asistente (Sin Conexión)';
            chatHeader.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
            console.error('❌ Error de conexión:', error);
            break;
    }
}

// Función para abrir/cerrar el chat
function toggleChat() {
    const chatWindow = document.getElementById('chatbot-window');
    const chatIcon = document.getElementById('chatbot-icon');
    
    if (!chatWindow || !chatIcon) return;

    chatOpen = !chatOpen;

    if (chatOpen) {
        // Abrir chat
        chatWindow.classList.remove('hidden');
        
        // Animación de apertura
        gsap.fromTo(chatWindow, {
            scaleY: 0,
            scaleX: 0.8,
            opacity: 0,
            y: 20
        }, {
            scaleY: 1,
            scaleX: 1,
            opacity: 1,
            y: 0,
            duration: 0.4,
            ease: 'back.out(1.7)'
        });

        // Animación del ícono
        gsap.to(chatIcon, {
            rotation: 180,
            duration: 0.3,
            ease: 'power2.out'
        });

        // Focus en el input
        setTimeout(() => {
            document.getElementById('user-input').focus();
        }, 400);

    } else {
        // Cerrar chat
        gsap.to(chatWindow, {
            scaleY: 0,
            scaleX: 0.8,
            opacity: 0,
            y: 20,
            duration: 0.3,
            ease: 'power2.in',
            onComplete: () => {
                chatWindow.classList.add('hidden');
            }
        });

        // Animación del ícono
        gsap.to(chatIcon, {
            rotation: 0,
            duration: 0.3,
            ease: 'power2.out'
        });
    }
}

// Función para habilitar el chat
function enableChat() {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    
    if (userInput) {
        userInput.disabled = false;
        userInput.placeholder = 'Escribe tu mensaje...';
        userInput.style.opacity = '1';
        userInput.style.cursor = 'text';
    }
    
    if (sendBtn) {
        sendBtn.disabled = false;
        sendBtn.style.opacity = '1';
        sendBtn.style.cursor = 'pointer';
    }
}

// Función para deshabilitar el chat
function disableChat(reason = 'Sistema de IA no disponible') {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    
    if (userInput) {
        userInput.disabled = true;
        userInput.placeholder = reason;
        userInput.value = '';
        userInput.style.opacity = '0.5';
        userInput.style.cursor = 'not-allowed';
    }
    
    if (sendBtn) {
        sendBtn.disabled = true;
        sendBtn.style.opacity = '0.5';
        sendBtn.style.cursor = 'not-allowed';
    }
}

// Función para enviar mensaje
async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Verificar que la IA esté disponible antes de enviar
    if (!aiStatus || !aiStatus.initialized || !aiStatus.dependencies_available) {
        addMessage('El sistema de IA no está disponible. El chatbot está deshabilitado.', 'bot');
        return;
    }

    // Agregar mensaje del usuario
    addMessage(message, 'user');
    
    // Limpiar input
    userInput.value = '';
    
    // Mostrar indicador de escritura
    const typingIndicator = showTypingIndicator();
    
    try {
        // Enviar mensaje al backend con IA
        console.log('📤 Enviando mensaje al backend:', message);
        
        const response = await fetch(`${BACKEND_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                user_id: 'user_' + Date.now(),
                timestamp: new Date().toISOString()
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: response.statusText }));
            
            // Si es 503, la IA no está disponible - deshabilitar chat
            if (response.status === 503) {
                disableChat('Sistema de IA no disponible');
                throw new Error(`503: ${errorData.detail || 'Sistema de IA no disponible'}`);
            }
            
            throw new Error(`HTTP ${response.status}: ${errorData.detail || response.statusText}`);
        }
        
        const data = await response.json();
        
        // Remover indicador de escritura
        removeTypingIndicator(typingIndicator);
        
        // Agregar respuesta del bot
        addMessage(data.response, 'bot');
        
        console.log('✅ Respuesta recibida del backend:', data.response);
        
    } catch (error) {
        console.error('❌ Error enviando mensaje:', error);
        
        // Remover indicador de escritura
        removeTypingIndicator(typingIndicator);
        
        // Mostrar mensaje de error
        let errorMessage = 'Lo siento, hubo un error procesando tu mensaje.';
        
        if (error.message.includes('503')) {
            errorMessage = 'Sistema de IA no disponible. El chatbot está deshabilitado.';
            disableChat('Sistema de IA no disponible');
            // Re-verificar estado después de un momento
            setTimeout(checkAISystemStatus, 5000);
        } else if (error.message.includes('500')) {
            errorMessage = 'Error interno del servidor. Verifica la consola para más detalles.';
        } else if (error.message.includes('Failed to fetch')) {
            errorMessage = 'No se pudo conectar con el servidor. Verifica que el backend esté ejecutándose.';
        }
        
        addMessage(errorMessage, 'bot');
        
        // Mostrar error detallado en consola para debugging
        console.error('🔍 Detalles del error:', {
            message: message,
            error: error.message,
            stack: error.stack,
            timestamp: new Date().toISOString()
        });
    }
}

// Función para agregar mensaje al chat
function addMessage(content, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    
    messageDiv.className = `chat-message ${sender}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    
    // Animación de entrada del mensaje
    gsap.fromTo(messageDiv, {
        opacity: 0,
        y: 20,
        scale: 0.9
    }, {
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 0.3,
        ease: 'power2.out'
    });
    
    // Scroll automático al final
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Guardar en historial
    messageHistory.push({
        content: content,
        sender: sender,
        timestamp: new Date()
    });
}

// Función para agregar mensaje de bienvenida
function addWelcomeMessage() {
    // Solo mostrar mensaje de bienvenida si la IA está disponible
    if (aiStatus && aiStatus.initialized && aiStatus.dependencies_available) {
        const welcomeMessages = [
            "¡Hola! Soy tu asistente virtual de DulceAI. ¿En qué puedo ayudarte hoy?",
            "¡Bienvenido a DulceAI! Estoy aquí para ayudarte con cualquier consulta sobre nuestros productos.",
            "Hola 👋 Soy el asistente de DulceAI. ¿Te gustaría conocer nuestros deliciosos pasteles?"
        ];
        
        const randomMessage = welcomeMessages[Math.floor(Math.random() * welcomeMessages.length)];
        addMessage(randomMessage, 'bot');
    } else {
        addMessage('Sistema de IA no disponible. El chatbot está deshabilitado.', 'bot');
    }
}

// Función para generar respuesta del bot (placeholder para IA)
function generateBotResponse(userMessage) {
    const message = userMessage.toLowerCase();
    
    // Respuestas predefinidas (placeholder para futura integración con LangChain + Ollama)
    if (message.includes('hola') || message.includes('hi') || message.includes('buenos')) {
        return "¡Hola! 😊 Me alegra saludarte. ¿En qué puedo ayudarte hoy?";
    }
    
    if (message.includes('precio') || message.includes('cuesta') || message.includes('valor')) {
        return "Los precios varían según el producto. Te recomiendo revisar nuestra sección de productos donde encontrarás todos los precios actualizados. ¿Hay algún producto específico que te interese?";
    }
    
    if (message.includes('pastel') || message.includes('torta') || message.includes('cake')) {
        return "¡Excelente elección! 🎂 Tenemos una gran variedad de pasteles. ¿Te gustaría conocer nuestros productos más populares o tienes algún sabor específico en mente?";
    }
    
    if (message.includes('cupcake') || message.includes('muffin')) {
        return "¡Los cupcakes son una de nuestras especialidades! 🧁 Tenemos diferentes sabores y decoraciones. ¿Te gustaría saber más sobre nuestros sets de cupcakes?";
    }
    
    if (message.includes('galleta') || message.includes('cookie')) {
        return "Nuestras galletas artesanales son deliciosas! 🍪 Están hechas con ingredientes naturales. ¿Te interesa conocer nuestros sabores disponibles?";
    }
    
    if (message.includes('cheesecake')) {
        return "¡El cheesecake de fresa es uno de nuestros productos estrella! 🍰 Está hecho con ingredientes frescos y una base de galleta casera. ¿Te gustaría más información?";
    }
    
    if (message.includes('pedido') || message.includes('orden') || message.includes('comprar')) {
        return "¡Perfecto! Para hacer un pedido, puedes agregar los productos que te gusten al carrito desde nuestra página de productos. ¿Necesitas ayuda con algún producto específico?";
    }
    
    if (message.includes('entrega') || message.includes('domicilio') || message.includes('delivery')) {
        return "Ofrecemos servicio de entrega a domicilio. Los tiempos y costos varían según la ubicación. ¿Te gustaría que te contactemos para coordinar tu pedido?";
    }
    
    if (message.includes('horario') || message.includes('abierto') || message.includes('tiempo')) {
        return "Nuestro horario de atención es de lunes a sábado de 8:00 AM a 8:00 PM. Los domingos cerramos a las 6:00 PM. ¿Hay algo más en lo que pueda ayudarte?";
    }
    
    if (message.includes('contacto') || message.includes('telefono') || message.includes('direccion')) {
        return "Puedes contactarnos por teléfono al +57 300 123 4567 o por email a info@dulceai.com. También puedes visitarnos en Calle 123 #45-67, Bogotá. ¿Te gustaría más información?";
    }
    
    if (message.includes('gracias') || message.includes('thanks')) {
        return "¡De nada! 😊 Fue un placer ayudarte. ¿Hay algo más en lo que pueda asistirte?";
    }
    
    if (message.includes('adios') || message.includes('bye') || message.includes('chao')) {
        return "¡Hasta luego! 👋 Espero verte pronto disfrutando de nuestros deliciosos productos. ¡Que tengas un excelente día!";
    }
    
    // Respuesta por defecto
    const defaultResponses = [
        "Interesante pregunta. Déjame ayudarte con eso. ¿Podrías ser más específico sobre lo que necesitas?",
        "Entiendo tu consulta. Aunque soy un asistente virtual, puedo ayudarte con información sobre nuestros productos y servicios. ¿Hay algo específico que te gustaría saber?",
        "¡Excelente pregunta! Me gustaría ayudarte mejor. ¿Podrías contarme más detalles sobre lo que necesitas?",
        "Comprendo tu interés. Para darte la mejor respuesta, ¿podrías ser más específico sobre tu consulta?",
        "¡Me encanta ayudarte! Aunque soy un asistente virtual, estoy aquí para responder tus preguntas sobre DulceAI. ¿Qué más te gustaría saber?"
    ];
    
    return defaultResponses[Math.floor(Math.random() * defaultResponses.length)];
}

// Función para mostrar indicador de escritura
function showTypingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    
    typingDiv.className = 'chat-message bot typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-content">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return typingDiv;
}

// Función para remover indicador de escritura
function removeTypingIndicator(typingDiv) {
    if (typingDiv && typingDiv.parentNode) {
        typingDiv.parentNode.removeChild(typingDiv);
    }
}

// Función para mejorar la experiencia del usuario
function enhanceUserExperience() {
    const userInput = document.getElementById('user-input');
    
    if (userInput) {
        // Auto-resize del textarea si fuera necesario
        userInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
        
        // Limpiar placeholder al hacer focus
        userInput.addEventListener('focus', function() {
            if (this.value === '') {
                this.placeholder = 'Escribe tu mensaje aquí...';
            }
        });
        
        // Restaurar placeholder al perder focus
        userInput.addEventListener('blur', function() {
            if (this.value === '') {
                this.placeholder = 'Escribe tu mensaje...';
            }
        });
    }
}

// Función para guardar historial de chat en localStorage
function saveChatHistory() {
    try {
        localStorage.setItem('dulceai_chat_history', JSON.stringify(messageHistory));
    } catch (error) {
        console.warn('No se pudo guardar el historial del chat:', error);
    }
}

// Función para cargar historial de chat desde localStorage
function loadChatHistory() {
    try {
        const savedHistory = localStorage.getItem('dulceai_chat_history');
        if (savedHistory) {
            messageHistory = JSON.parse(savedHistory);
            // Mostrar últimos mensajes si hay historial
            if (messageHistory.length > 0) {
                const chatMessages = document.getElementById('chat-messages');
                chatMessages.innerHTML = ''; // Limpiar mensaje de bienvenida
                
                // Mostrar últimos 5 mensajes
                const recentMessages = messageHistory.slice(-5);
                recentMessages.forEach(msg => {
                    addMessage(msg.content, msg.sender);
                });
            }
        }
    } catch (error) {
        console.warn('No se pudo cargar el historial del chat:', error);
    }
}

// Función para limpiar historial de chat
function clearChatHistory() {
    messageHistory = [];
    localStorage.removeItem('dulceai_chat_history');
    
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages) {
        chatMessages.innerHTML = '';
        addWelcomeMessage();
    }
}

// Función para exportar historial de chat
function exportChatHistory() {
    if (messageHistory.length === 0) {
        alert('No hay historial de chat para exportar');
        return;
    }
    
    const chatData = {
        timestamp: new Date().toISOString(),
        messages: messageHistory
    };
    
    const dataStr = JSON.stringify(chatData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `dulceai_chat_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
}

// Función para integrar con IA (placeholder para futura implementación)
function integrateWithAI(userMessage) {
    // TODO: Integrar con Ollama + LangChain + RAG
    // Esta función será reemplazada por la integración real con IA
    
    console.log('Integración con IA pendiente:', userMessage);
    
    // Placeholder para la respuesta de IA
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(generateBotResponse(userMessage));
        }, 1000);
    });
}

// Función para manejar errores del chatbot
function handleChatbotError(error) {
    console.error('Error en el chatbot:', error);
    
    const errorMessage = "Lo siento, hubo un error en el sistema. Por favor, intenta de nuevo.";
    addMessage(errorMessage, 'bot');
}

// Inicializar mejoras de experiencia de usuario
enhanceUserExperience();

// Cargar historial al inicializar
loadChatHistory();

// Guardar historial cada 30 segundos
setInterval(saveChatHistory, 30000);

// Exportar funciones para uso global
window.Chatbot = {
    toggleChat,
    sendMessage,
    clearChatHistory,
    exportChatHistory,
    integrateWithAI
};

// Manejar errores globales del chatbot
window.addEventListener('error', function(e) {
    if (e.message.includes('chatbot') || e.message.includes('chat')) {
        handleChatbotError(e);
    }
});

