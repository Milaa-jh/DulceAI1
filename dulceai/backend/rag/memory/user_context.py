"""
Gestión de contexto del usuario
Implementa recuperación de contexto semántico
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class UserContext:
    """
    Clase para gestionar contexto semántico del usuario
    Almacena información personal y preferencias
    """
    
    def __init__(self, user_id: str):
        """
        Inicializar contexto de usuario
        
        Args:
            user_id: Identificador único del usuario
        """
        self.user_id = user_id
        self.name: Optional[str] = None
        self.preferences: List[str] = []
        self.recent_products: List[str] = []
        self.orders_history: List[Dict[str, Any]] = []
        self.last_visit: Optional[str] = None
        self.registration_date: str = datetime.now().isoformat()
        
        logger.info(f"👤 Contexto creado para usuario: {user_id}")
    
    def update_name(self, name: str):
        """Actualizar nombre del usuario"""
        self.name = name
        logger.info(f"👤 Nombre actualizado: {name}")
    
    def add_preference(self, preference: str):
        """Agregar preferencia del usuario"""
        if preference not in self.preferences:
            self.preferences.append(preference)
            logger.info(f"❤️ Preferencia agregada: {preference}")
    
    def add_recent_product(self, product: str):
        """Agregar producto recientemente consultado"""
        if product not in self.recent_products:
            self.recent_products.insert(0, product)
            # Mantener solo últimos 5 productos
            if len(self.recent_products) > 5:
                self.recent_products = self.recent_products[:5]
            logger.info(f"🛍️ Producto reciente: {product}")
    
    def add_order(self, order_details: Dict[str, Any]):
        """Agregar pedido al historial"""
        order = {
            **order_details,
            "timestamp": datetime.now().isoformat(),
            "user_id": self.user_id
        }
        self.orders_history.append(order)
        logger.info(f"📋 Pedido agregado al historial")
    
    def update_last_visit(self):
        """Actualizar última visita"""
        self.last_visit = datetime.now().isoformat()
        logger.debug("🕒 Última visita actualizada")
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Obtener resumen del contexto del usuario"""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "preferences": self.preferences,
            "recent_products": self.recent_products,
            "total_orders": len(self.orders_history),
            "last_visit": self.last_visit,
            "registration_date": self.registration_date
        }
    
    def build_personalized_prompt(self) -> str:
        """
        Construir prompt personalizado basado en el contexto
        Implementa recuperación de contexto semántico
        """
        prompt_parts = []
        
        if self.name:
            prompt_parts.append(f"El cliente se llama {self.name}.")
        
        if self.preferences:
            prompt_parts.append(f"Le interesa: {', '.join(self.preferences)}.")
        
        if self.recent_products:
            prompt_parts.append(f"Recientemente consultó: {', '.join(self.recent_products)}.")
        
        if self.orders_history:
            prompt_parts.append(f"Tiene {len(self.orders_history)} pedidos anteriores.")
        
        return " ".join(prompt_parts) if prompt_parts else ""



