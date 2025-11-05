# DulceAI - Integración de IA (Backward Compatible)
# Este archivo mantiene compatibilidad con el código existente
# El código real está ahora en rag/

import logging

# Intentar importar la nueva estructura modular
try:
    from rag.agent import DulceAIAgent
    from rag.config import AIConfig
    
    logger = logging.getLogger(__name__)
    logger.info("✅ Importando agente desde estructura modular RAG")
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.error(f"❌ Error importando agente modular: {e}")
    DulceAIAgent = None
    AIConfig = None

# Instancia global del agente
ai_system = None

def initialize_ai_system() -> bool:
    """
    Inicializar el sistema de IA global
    Mantiene compatibilidad con código existente
    """
    global ai_system
    
    if DulceAIAgent is None:
        return False
    
    ai_system = DulceAIAgent()
    return ai_system.initialize()

def process_chat_message(message: str, user_id: str = None) -> str:
    """
    Procesar mensaje de chat usando el agente
    Mantiene compatibilidad con código existente
    """
    global ai_system
    
    if ai_system is None:
        return "❌ Error: Sistema de IA no inicializado"
    
    return ai_system.process_message(message, user_id)

def get_ai_status() -> dict:
    """
    Obtener estado del sistema de IA
    Mantiene compatibilidad con código existente
    """
    global ai_system
    
    if ai_system is None:
        return {
            "initialized": False,
            "error": "Sistema no inicializado"
        }
    
    return ai_system.get_status()



