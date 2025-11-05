"""
Herramientas de consulta de productos
Implementa herramientas de consulta
"""

import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class ProductTools:
    """Herramientas para gestión de productos y catálogo"""
    
    def __init__(self, config):
        """
        Inicializar herramientas de productos
        
        Args:
            config: Objeto de configuración con catálogo de productos
        """
        self.config = config
        logger.info("🛍️ Herramientas de productos inicializadas")
    
    def search_product(self, query: str) -> Dict[str, Any]:
        """
        Buscar producto en el catálogo con búsqueda mejorada por keywords
        
        Args:
            query: Término de búsqueda
            
        Returns:
            Información del producto o None
        """
        query_lower = query.lower().strip()
        
        # Primero buscar por nombre exacto o parcial
        result = self.config.search_product(query)
        
        # Si no se encuentra, buscar por keywords
        if not result:
            for key, product in self.config.PRODUCTS.items():
                # Buscar en keywords
                if 'keywords' in product:
                    for keyword in product.get('keywords', []):
                        if keyword.lower() in query_lower or query_lower in keyword.lower():
                            result = product
                            break
                    if result:
                        break
                
                # Buscar en descripción
                if not result and query_lower in product.get('description', '').lower():
                    result = product
                    break
        
        if result:
            logger.info(f"✅ Producto encontrado: {result['name']}")
            
            # Construir mensaje detallado con toda la información experta
            message_parts = [
                f"🍰 {result['name']}",
                f"💰 Precio: ${result['price']:,}",
                f"📝 {result['description']}"
            ]
            
            # Agregar información adicional si está disponible
            if 'size' in result:
                message_parts.append(f"📏 Tamaño: {result['size']}")
            if 'ingredients' in result:
                message_parts.append(f"🥄 Ingredientes: {result['ingredients']}")
            if 'allergens' in result:
                message_parts.append(f"⚠️ Alérgenos: {result['allergens']}")
            if 'storage' in result:
                message_parts.append(f"❄️ Conservación: {result['storage']}")
            if 'customization' in result:
                message_parts.append(f"✨ Personalización: {result['customization']}")
            
            return {
                "found": True,
                "product": result,
                "message": "\n".join(message_parts)
            }
        else:
            logger.warning(f"❌ Producto no encontrado: {query}")
            return {
                "found": False,
                "message": f"No encontré un producto específico con '{query}'. ¿Te gustaría ver nuestro catálogo completo? Tenemos tortas, cupcakes, galletas, cheesecakes, pies, donas, muffins, brownies y macarons."
            }
    
    def list_all_products(self) -> List[Dict[str, Any]]:
        """
        Listar todos los productos disponibles
        
        Returns:
            Lista de todos los productos
        """
        products = []
        for key, product in self.config.PRODUCTS.items():
            products.append(product)
        
        logger.info(f"📋 Listando {len(products)} productos")
        return products
    
    def get_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Obtener productos por categoría
        
        Args:
            category: Categoría a filtrar
            
        Returns:
            Lista de productos de la categoría
        """
        products = []
        for product in self.config.PRODUCTS.values():
            if category.lower() in product["category"].lower():
                products.append(product)
        
        logger.info(f"🏷️ {len(products)} productos en categoría: {category}")
        return products
    
    def recommend_products(self, preferences: List[str]) -> List[Dict[str, Any]]:
        """
        Recomendar productos basado en preferencias
        
        Args:
            preferences: Lista de preferencias del usuario
            
        Returns:
            Lista de productos recomendados
        """
        recommendations = []
        
        for preference in preferences:
            products = self.get_products_by_category(preference)
            recommendations.extend(products)
        
        # Eliminar duplicados
        seen = set()
        unique_recs = []
        for product in recommendations:
            name = product["name"]
            if name not in seen:
                seen.add(name)
                unique_recs.append(product)
        
        logger.info(f"💡 {len(unique_recs)} recomendaciones generadas")
        return unique_recs[:3]  # Retornar top 3



