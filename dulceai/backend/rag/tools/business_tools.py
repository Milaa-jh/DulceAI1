"""
Herramientas de información del negocio
Implementa herramientas de consulta
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BusinessTools:
    """Herramientas para información del negocio"""
    
    def __init__(self, config):
        """
        Inicializar herramientas de negocio
        
        Args:
            config: Objeto de configuración con información del negocio
        """
        self.config = config
        logger.info("🏢 Herramientas de negocio inicializadas")
    
    def get_hours(self) -> str:
        """
        Obtener horarios de atención
        
        Returns:
            String con horarios formateados
        """
        hours = self.config.BUSINESS_INFO["hours"]
        logger.debug("🕐 Horarios consultados")
        return f"Horarios de atención:\n{hours}"
    
    def get_contact_info(self) -> str:
        """
        Obtener información de contacto
        
        Returns:
            String con información de contacto formateada
        """
        info = self.config.BUSINESS_INFO
        contact = f"""Información de contacto:

📞 Teléfono: {info['phone']}
📧 Email: {info['email']}
📍 Dirección: {info['address']}"""
        
        logger.debug("📞 Información de contacto consultada")
        return contact
    
    def get_full_business_info(self) -> Dict[str, Any]:
        """
        Obtener toda la información del negocio
        
        Returns:
            Diccionario con toda la información
        """
        return self.config.BUSINESS_INFO.copy()
    
    def format_order_confirmation(self, order_details: Dict[str, Any]) -> str:
        """
        Formatear confirmación de pedido
        
        Args:
            order_details: Detalles del pedido
            
        Returns:
            String formateado con confirmación
        """
        confirmation = f"""✅ Pedido confirmado:

{order_details.get('message', 'Tu pedido ha sido registrado')}

Te contactaremos pronto para confirmar los detalles.
Información de contacto: {self.config.BUSINESS_INFO['phone']}"""
        
        logger.info("✅ Confirmación de pedido generada")
        return confirmation



