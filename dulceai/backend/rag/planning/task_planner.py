"""
Planificador de tareas del agente
Implementa esquemas de planificación
"""

import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class TaskPlanner:
    """
    Planificador de tareas jerárquico
    Descompone objetivos en tareas ejecutables
    """
    
    def __init__(self):
        """Inicializar planificador"""
        self.task_steps = []
        logger.info("📋 Planificador de tareas inicializado")
    
    def plan_conversation(self, user_message: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Planificar respuesta basado en mensaje y contexto
        
        Args:
            user_message: Mensaje del usuario
            context: Contexto de la conversación
            
        Returns:
            Lista de pasos planificados
        """
        steps = []
        message_lower = user_message.lower()
        
        # Detectar tipo de consulta y planificar
        if any(word in message_lower for word in ["hola", "hi", "buenos"]):
            steps.append({
                "action": "greet",
                "priority": 1,
                "description": "Saludar al usuario de manera amigable"
            })
            
            # Si no hay nombre en contexto, preguntar por nombre
            if not context.get("name"):
                steps.append({
                    "action": "ask_name",
                    "priority": 2,
                    "description": "Preguntar nombre del usuario"
                })
        
        elif any(word in message_lower for word in ["producto", "cupcake", "torta", "pastel", "galleta"]):
            steps.append({
                "action": "search_product",
                "priority": 1,
                "description": "Buscar información del producto"
            })
            steps.append({
                "action": "recommend",
                "priority": 2,
                "description": "Ofrecer recomendaciones relacionadas"
            })
        
        elif any(word in message_lower for word in ["precio", "cuesta", "valor", "cuánto"]):
            steps.append({
                "action": "provide_price",
                "priority": 1,
                "description": "Proporcionar información de precios"
            })
            steps.append({
                "action": "offer_alternatives",
                "priority": 2,
                "description": "Ofrecer alternativas si es necesario"
            })
        
        elif any(word in message_lower for word in ["pedido", "orden", "comprar", "quiero"]):
            steps.append({
                "action": "process_order",
                "priority": 1,
                "description": "Procesar pedido del cliente"
            })
            steps.append({
                "action": "confirm_contact",
                "priority": 2,
                "description": "Confirmar información de contacto"
            })
        
        elif any(word in message_lower for word in ["horario", "abierto", "tiempo"]):
            steps.append({
                "action": "provide_hours",
                "priority": 1,
                "description": "Proporcionar horarios de atención"
            })
        
        elif any(word in message_lower for word in ["contacto", "teléfono", "dirección"]):
            steps.append({
                "action": "provide_contact",
                "priority": 1,
                "description": "Proporcionar información de contacto"
            })
        
        else:
            # Consulta genérica
            steps.append({
                "action": "general_response",
                "priority": 1,
                "description": "Proporcionar respuesta general o aclaración"
            })
        
        # Agregar paso de personalización si hay contexto
        if context.get("name"):
            steps.insert(1, {
                "action": "personalize",
                "priority": 0,
                "description": f"Personalizar respuesta para {context.get('name')}"
            })
        
        logger.info(f"📋 Plan generado: {len(steps)} pasos")
        self.task_steps = steps
        
        return steps
    
    def get_next_step(self) -> Optional[Dict[str, Any]]:
        """
        Obtener siguiente paso planificado
        
        Returns:
            Siguiente paso o None si no hay más pasos
        """
        if self.task_steps:
            return self.task_steps.pop(0)
        return None
    
    def clear_plan(self):
        """Limpiar plan actual"""
        self.task_steps = []
        logger.debug("🗑️ Plan limpiado")



