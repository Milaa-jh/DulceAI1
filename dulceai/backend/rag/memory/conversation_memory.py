"""
Sistema de memoria conversacional para el agente
Implementa memoria de contenido
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ConversationMemory:
    """
    Clase para gestionar memoria conversacional
    Implementa patrón Buffer para conversaciones cortas
    """
    
    def __init__(self, max_messages: int = 10):
        """
        Inicializar memoria conversacional
        
        Args:
            max_messages: Número máximo de mensajes a almacenar
        """
        self.messages: List[Dict[str, Any]] = []
        self.max_messages = max_messages
        logger.info(f"💾 Memoria conversacional inicializada (max: {max_messages})")
    
    def add_user_message(self, content: str, metadata: Optional[Dict] = None):
        """
        Agregar mensaje del usuario a la memoria
        
        Args:
            content: Contenido del mensaje
            metadata: Metadatos adicionales (opcional)
        """
        message = {
            "role": "user",
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        if metadata:
            message["metadata"] = metadata
        
        self.messages.append(message)
        self._trim_messages()
        logger.debug(f"➕ Mensaje de usuario agregado: {content[:50]}...")
    
    def add_ai_message(self, content: str, metadata: Optional[Dict] = None):
        """
        Agregar mensaje de la IA a la memoria
        
        Args:
            content: Contenido de la respuesta
            metadata: Metadatos adicionales (opcional)
        """
        message = {
            "role": "assistant",
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        if metadata:
            message["metadata"] = metadata
        
        self.messages.append(message)
        self._trim_messages()
        logger.debug(f"➕ Mensaje de IA agregado: {content[:50]}...")
    
    def _trim_messages(self):
        """Mantener solo los últimos N mensajes"""
        if len(self.messages) > self.max_messages:
            removed = self.messages[:-self.max_messages]
            self.messages = self.messages[-self.max_messages:]
            logger.debug(f"✂️ Mensajes antiguos removidos: {len(removed)}")
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Obtener historial de conversación
        
        Args:
            limit: Número máximo de mensajes a retornar
            
        Returns:
            Lista de mensajes ordenados cronológicamente
        """
        history = self.messages.copy()
        
        if limit:
            history = history[-limit:]
        
        return history
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Obtener resumen de la conversación
        Útil para recuperación de contexto semántico
        """
        return {
            "total_messages": len(self.messages),
            "start_time": self.messages[0]["timestamp"] if self.messages else None,
            "last_message": self.messages[-1]["timestamp"] if self.messages else None,
            "topics": self._extract_topics()
        }
    
    def _extract_topics(self) -> List[str]:
        """Extraer temas principales de la conversación"""
        topics = []
        
        # Palabras clave comunes
        keywords = ["pedido", "producto", "precio", "horario", "contacto", "cupcake", "torta", "pastel"]
        
        for msg in self.messages:
            content = msg.get("content", "").lower()
            for keyword in keywords:
                if keyword in content and keyword not in topics:
                    topics.append(keyword)
        
        return topics
    
    def clear(self):
        """Limpiar toda la memoria"""
        count = len(self.messages)
        self.messages = []
        logger.info(f"🗑️ Memoria limpiada ({count} mensajes eliminados)")
    
    def export(self) -> str:
        """Exportar memoria como JSON"""
        return json.dumps({
            "messages": self.messages,
            "summary": self.get_conversation_summary()
        }, indent=2)
    
    def import_from_json(self, json_data: str):
        """Importar memoria desde JSON"""
        data = json.loads(json_data)
        self.messages = data.get("messages", [])
        logger.info(f"📥 Memoria importada ({len(self.messages)} mensajes)")



