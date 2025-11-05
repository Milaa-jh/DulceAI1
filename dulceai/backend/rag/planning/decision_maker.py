"""
Sistema de toma de decisiones del agente
Implementa estrategias adaptativas
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class DecisionMaker:
    """
    Toma de decisiones adaptativa
    Ajusta comportamiento según condiciones del entorno
    """
    
    def __init__(self):
        """Inicializar sistema de decisiones"""
        self.strategy = "balanced"  # balanced, thorough, quick
        logger.info("🧠 Sistema de decisiones inicializado")
    
    def decide_response_style(self, context: Dict[str, Any]) -> str:
        """
        Decidir estilo de respuesta según contexto
        
        Args:
            context: Contexto de la conversación
            
        Returns:
            Estilo de respuesta: 'detailed', 'brief', 'personalized'
        """
        # Si es primera vez, ser más detallado
        if context.get("message_count", 0) <= 2:
            logger.debug("🎯 Estilo: detailed (primera vez)")
            return "detailed"
        
        # Si hay nombre, personalizar
        if context.get("name"):
            logger.debug("🎯 Estilo: personalized (con nombre)")
            return "personalized"
        
        # Por defecto, breve
        logger.debug("🎯 Estilo: brief (default)")
        return "brief"
    
    def should_use_tool(self, message: str, available_tools: List[str]) -> Optional[str]:
        """
        Decidir si usar una herramienta específica
        
        Args:
            message: Mensaje del usuario
            available_tools: Lista de herramientas disponibles
            
        Returns:
            Nombre de la herramienta a usar o None
        """
        message_lower = message.lower()
        
        tool_keywords = {
            "BuscarProducto": ["producto", "cupcake", "torta", "pastel", "galleta", "cheesecake", "pie", "dona"],
            "ConsultarHorario": ["horario", "abierto", "cierra", "disponible", "tiempo"],
            "ConsultarContacto": ["contacto", "teléfono", "telefono", "dirección", "direccion", "email"],
            "ProcesarPedido": ["pedido", "orden", "comprar", "quiero", "necesito"]
        }
        
        for tool_name, keywords in tool_keywords.items():
            if tool_name in available_tools:
                if any(keyword in message_lower for keyword in keywords):
                    logger.info(f"🛠️ Herramienta seleccionada: {tool_name}")
                    return tool_name
        
        logger.debug("🛠️ No se requiere herramienta específica")
        return None
    
    def should_save_context(self, message: str) -> bool:
        """
        Decidir si guardar información en el contexto
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            True si debe guardarse, False si no
        """
        save_keywords = [
            "mi nombre es", "me llamo", "soy",
            "me gusta", "prefiero", "me interesa"
        ]
        
        message_lower = message.lower()
        should_save = any(keyword in message_lower for keyword in save_keywords)
        
        if should_save:
            logger.debug("💾 Decisión: Guardar en contexto")
        
        return should_save
    
    def extract_important_info(self, message: str) -> Dict[str, Any]:
        """
        Extraer información importante del mensaje
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            Diccionario con información extraída
        """
        info = {}
        message_lower = message.lower()
        
        # Extraer nombre
        if "mi nombre es" in message_lower:
            parts = message.split()
            for i, part in enumerate(parts):
                if part.lower() in ["nombre", "llamo"]:
                    if i + 2 < len(parts):
                        info["name"] = parts[i+2].capitalize()
                        break
        
        elif "me llamo" in message_lower:
            parts = message.split()
            for i, part in enumerate(parts):
                if part.lower() == "llamo":
                    if i + 1 < len(parts):
                        info["name"] = parts[i+1].capitalize()
                        break
        
        # Extraer productos mencionados
        product_keywords = ["cupcake", "torta", "pastel", "galleta", "cheesecake", "pie", "dona"]
        mentioned_products = [p for p in product_keywords if p in message_lower]
        
        if mentioned_products:
            info["mentioned_products"] = mentioned_products
        
        # Extraer intención
        if any(word in message_lower for word in ["precio", "cuesta", "valor"]):
            info["intent"] = "price_inquiry"
        elif any(word in message_lower for word in ["pedido", "comprar", "quiero"]):
            info["intent"] = "purchase"
        elif any(word in message_lower for word in ["horario", "abierto"]):
            info["intent"] = "hours_inquiry"
        elif any(word in message_lower for word in ["contacto", "teléfono"]):
            info["intent"] = "contact_inquiry"
        
        if info:
            logger.info(f"📊 Información extraída: {list(info.keys())}")
        
        return info



