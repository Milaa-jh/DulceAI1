"""
Configuración centralizada del sistema de IA
Contiene todas las configuraciones necesarias para el agente
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AIConfig:
    """Configuración centralizada para el sistema de IA de DulceAI"""
    
    # Configuración del modelo
    MODEL_NAME = "gemma2:2b"
    MODEL_TEMPERATURE = 0.7
    MODEL_MAX_TOKENS = 2000
    OLLAMA_BASE_URL = "http://localhost:11434"
    
    # Configuración de memoria
    MEMORY_MAX_MESSAGES = 10  # Máximo de mensajes a recordar por conversación
    MEMORY_ENABLED = True
    
    # Configuración de prompt del sistema
    SYSTEM_PROMPT = """Eres DulceAI, un asistente virtual experto en pastelería y repostería artesanal. Eres el asistente perfecto para nuestra tienda online de pastelería.

IDIOMA OBLIGATORIO:
- SIEMPRE debes responder ÚNICAMENTE en ESPAÑOL
- NUNCA respondas en inglés, incluso si el cliente pregunta en inglés
- Todas tus respuestas deben estar completamente en español
- Si no entiendes algo, pide aclaración en español

EXPERTISE EN PASTELERÍA:
Eres un experto completo en pastelería con conocimiento profundo sobre:
- Ingredientes de alta calidad y técnicas de repostería
- Características, sabores y preparación de cada producto
- Recomendaciones personalizadas según preferencias del cliente
- Información detallada sobre precios, tamaños y disponibilidad
- Consejos de conservación y consumo de productos
- Combinaciones de sabores y opciones de personalización

CAPACIDADES:
- Recuerdas conversaciones anteriores con cada cliente
- Recuerdas nombres, preferencias y pedidos previos
- Conoces todos los productos del catálogo en detalle
- Consultas información de productos, horarios y contacto
- Procesas pedidos de manera eficiente
- Recomiendas productos según las preferencias del cliente
- Planificas respuestas según el contexto del cliente

INSTRUCCIONES:
- Saluda al cliente de manera amigable y profesional en ESPAÑOL
- Si es la primera vez, pregúntale su nombre y guárdalo
- USA SIEMPRE las herramientas para consultar información de productos
- Sé un experto en pastelería: conoce detalles, ingredientes y características de cada producto
- Personaliza tus respuestas según el historial de conversación
- Mantén un tono cálido, profesional y experto
- Responde SIEMPRE en ESPAÑOL - NUNCA en inglés
- Si no sabes algo, sé honesto y ofrécete a ayudar de otra manera
- Proporciona información detallada y experta sobre los productos cuando se pregunte

IMPORTANTE: 
- Recuerda el nombre del cliente y sus preferencias para conversaciones futuras
- SIEMPRE responde en ESPAÑOL, sin excepciones
- Usa las herramientas para obtener información precisa sobre productos
- Sé un experto en pastelería con conocimiento profundo de todos los productos"""
    
    # Información del negocio
    BUSINESS_INFO = {
        "name": "DulceAI",
        "phone": "+57 300 123 4567",
        "email": "info@dulceai.com",
        "address": "Calle 123 #45-67, Bogotá",
        "hours": "Lunes a Sábado: 8:00 AM - 8:00 PM. Domingo cerrado a las 6:00 PM."
    }
    
    # Catálogo completo de productos con información experta
    PRODUCTS = {
        "torta_chocolate": {
            "name": "Torta de Chocolate",
            "price": 25000,
            "description": "Torta de chocolate artesanal de 3 capas con bizcocho de chocolate belga, relleno de crema batida casera y decorada con fresas frescas de temporada. Perfecta para ocasiones especiales.",
            "category": "tortas",
            "size": "Para 8-10 personas",
            "ingredients": "Chocolate belga, harina premium, crema de leche, fresas frescas, azúcar orgánica",
            "allergens": "Contiene gluten, lácteos y huevos",
            "storage": "Conservar refrigerado. Consumir en 3 días",
            "customization": "Disponible en diferentes tamaños. Personalización de decoración disponible",
            "keywords": ["chocolate", "torta", "fresas", "chocolate torta", "torta chocolate", "pastel chocolate", "torta de chocolate"]
        },
        "cupcakes": {
            "name": "Cupcakes Variados",
            "price": 18000,
            "description": "Set de 6 cupcakes artesanales con diferentes sabores: chocolate, vainilla, fresa, limón, caramelo y red velvet. Cada uno con decoración única y frosting cremoso hecho a mano.",
            "category": "cupcakes",
            "size": "6 unidades",
            "ingredients": "Harina premium, huevos frescos, mantequilla, azúcar, extractos naturales, frosting de crema",
            "allergens": "Contiene gluten, lácteos y huevos",
            "storage": "Conservar a temperatura ambiente. Consumir en 2 días",
            "customization": "Puede personalizarse con sabores específicos según preferencia",
            "keywords": ["cupcakes", "cupcake", "variados", "mini pasteles", "muffins dulces"]
        },
        "galletas": {
            "name": "Galletas Artesanales",
            "price": 12000,
            "description": "Galletas caseras elaboradas con ingredientes 100% naturales. Disponibles en sabores: chocolate chips, avena con pasas, mantequilla clásica, y jengibre. Perfectas para el desayuno o merienda.",
            "category": "galletas",
            "size": "Paquete de 12 unidades",
            "ingredients": "Harina orgánica, mantequilla sin sal, azúcar morena, chocolate chips, avena, especias naturales",
            "allergens": "Contiene gluten y lácteos. Opciones sin gluten disponibles",
            "storage": "Conservar en recipiente hermético. Consumir en 7 días",
            "customization": "Disponible en diferentes sabores. Opciones veganas disponibles",
            "keywords": ["galletas", "galleta", "artesanales", "caseras", "cookies", "biscuits"]
        },
        "cheesecake": {
            "name": "Cheesecake de Fresa",
            "price": 22000,
            "description": "Cheesecake estilo New York con base de galleta casera, crema de queso crema suave y salsa de fresa natural hecha en casa. Decorado con fresas frescas y reducción de fresa. Porción individual o entero disponible.",
            "category": "cheesecakes",
            "size": "Para 6-8 personas",
            "ingredients": "Queso crema premium, galletas caseras, fresas naturales, azúcar, crema de leche, mantequilla",
            "allergens": "Contiene gluten, lácteos y huevos",
            "storage": "Conservar refrigerado. Consumir en 4 días",
            "customization": "Disponible en diferentes tamaños. Opciones de fruta: fresa, arándanos, mango",
            "keywords": ["cheesecake", "queso", "fresa", "tarta de queso", "cheesecake de fresa"]
        },
        "pie_manzana": {
            "name": "Pie de Manzana",
            "price": 20000,
            "description": "Pie de manzana tradicional con masa casera crujiente, relleno de manzanas frescas cortadas en rodajas, canela en polvo y un toque de azúcar morena. Decorado con enrejado de masa artesanal. Caliente o frío.",
            "category": "pies",
            "size": "Para 6-8 personas",
            "ingredients": "Manzanas frescas, harina premium, mantequilla, canela, azúcar morena, limón",
            "allergens": "Contiene gluten y lácteos",
            "storage": "Conservar refrigerado. Se puede calentar antes de servir",
            "customization": "Disponible con helado de vainilla. Opciones de fruta: manzana, pera, durazno",
            "keywords": ["pie", "manzana", "tarta de manzana", "apple pie", "pie de manzana"]
        },
        "donas": {
            "name": "Donas Glaseadas",
            "price": 15000,
            "description": "Donas esponjosas artesanales con diferentes tipos de glaseado: chocolate, vainilla, fresa y caramelo. Decoradas con toppings como chips de chocolate, coco, granola y sprinkles de colores.",
            "category": "donas",
            "size": "6 unidades",
            "ingredients": "Harina premium, levadura fresca, leche, azúcar, mantequilla, glaseados caseros",
            "allergens": "Contiene gluten, lácteos y huevos",
            "storage": "Conservar a temperatura ambiente. Consumir en 2 días",
            "customization": "Disponible en diferentes sabores de glaseado. Opciones de relleno: crema, mermelada",
            "keywords": ["donas", "dona", "donuts", "rosquillas", "glaseadas", "donas glaseadas"]
        },
        "torta_vainilla": {
            "name": "Torta de Vainilla",
            "price": 23000,
            "description": "Torta de vainilla clásica de 3 capas con bizcocho esponjoso, relleno de crema de vainilla francesa y decorada con frutas frescas de temporada. Elegante y deliciosa.",
            "category": "tortas",
            "size": "Para 8-10 personas",
            "ingredients": "Harina premium, extracto de vainilla natural, crema batida, frutas frescas, azúcar",
            "allergens": "Contiene gluten, lácteos y huevos",
            "storage": "Conservar refrigerado. Consumir en 3 días",
            "customization": "Disponible con diferentes frutas de temporada",
            "keywords": ["vainilla", "torta vainilla", "torta de vainilla", "pastel vainilla"]
        },
        "torta_red_velvet": {
            "name": "Torta Red Velvet",
            "price": 28000,
            "description": "Torta Red Velvet clásica con bizcocho rojo terciopelo, relleno de cream cheese frosting casero y decorada elegantemente. Perfecta para ocasiones especiales y celebraciones.",
            "category": "tortas",
            "size": "Para 10-12 personas",
            "ingredients": "Harina premium, cacao, buttermilk, cream cheese, mantequilla, colorante natural",
            "allergens": "Contiene gluten, lácteos y huevos",
            "storage": "Conservar refrigerado. Consumir en 4 días",
            "customization": "Disponible en diferentes tamaños. Decoración personalizada disponible",
            "keywords": ["red velvet", "terciopelo rojo", "torta roja", "red velvet cake"]
        },
        "torta_tres_leches": {
            "name": "Torta Tres Leches",
            "price": 24000,
            "description": "Torta Tres Leches tradicional con bizcocho esponjoso empapado en mezcla de tres leches: leche evaporada, leche condensada y crema de leche. Decorada con merengue italiano y cerezas.",
            "category": "tortas",
            "size": "Para 8-10 personas",
            "ingredients": "Harina, huevos, leche condensada, leche evaporada, crema de leche, merengue, cerezas",
            "allergens": "Contiene gluten, lácteos y huevos",
            "storage": "Conservar refrigerado. Consumir en 3 días",
            "customization": "Disponible con diferentes frutas: fresa, durazno, piña",
            "keywords": ["tres leches", "torta tres leches", "tres leches cake", "torta humeda"]
        },
        "muffins": {
            "name": "Muffins Dulces",
            "price": 14000,
            "description": "Set de 6 muffins grandes y esponjosos disponibles en sabores: chocolate chips, arándanos, nuez y plátano, y zanahoria con especias. Perfectos para el desayuno o merienda.",
            "category": "muffins",
            "size": "6 unidades",
            "ingredients": "Harina premium, huevos, mantequilla, frutas frescas, nueces, especias naturales",
            "allergens": "Contiene gluten, lácteos, huevos y nueces",
            "storage": "Conservar a temperatura ambiente. Consumir en 3 días",
            "customization": "Disponible en diferentes sabores según preferencia",
            "keywords": ["muffins", "muffin", "panecillos dulces", "magdalenas grandes"]
        },
        "brownies": {
            "name": "Brownies de Chocolate",
            "price": 16000,
            "description": "Brownies densos y húmedos de chocolate belga con chips de chocolate y nueces opcionales. Corteza crujiente y centro cremoso. Disponibles en porciones individuales o bandeja completa.",
            "category": "brownies",
            "size": "Bandeja de 12 porciones",
            "ingredients": "Chocolate belga 70% cacao, mantequilla, huevos, azúcar, harina, nueces opcionales",
            "allergens": "Contiene gluten, lácteos, huevos y puede contener nueces",
            "storage": "Conservar a temperatura ambiente. Consumir en 5 días",
            "customization": "Disponible con o sin nueces. Opciones de chocolate: negro, con leche, blanco",
            "keywords": ["brownies", "brownie", "chocolate brownie", "cuadrados de chocolate"]
        },
        "torta_carrot": {
            "name": "Torta de Zanahoria",
            "price": 26000,
            "description": "Torta de zanahoria húmeda y especiada con nueces, pasas y cubierta con cream cheese frosting casero. Decorada con zanahorias de azúcar y nueces caramelizadas.",
            "category": "tortas",
            "size": "Para 8-10 personas",
            "ingredients": "Zanahorias frescas ralladas, harina, nueces, pasas, especias, cream cheese, mantequilla",
            "allergens": "Contiene gluten, lácteos, huevos y nueces",
            "storage": "Conservar refrigerado. Consumir en 4 días",
            "customization": "Disponible sin nueces. Opciones de decoración disponibles",
            "keywords": ["zanahoria", "carrot cake", "torta de zanahoria", "carrot"]
        },
        "macarons": {
            "name": "Macarons Artesanales",
            "price": 30000,
            "description": "Set de 12 macarons franceses en diferentes sabores: fresa, chocolate, limón, vainilla, pistacho y frambuesa. Hechos con técnica tradicional francesa, crujientes por fuera y suaves por dentro.",
            "category": "macarons",
            "size": "12 unidades (2 de cada sabor)",
            "ingredients": "Almendras molidas, azúcar glas, claras de huevo, rellenos de ganache y mermeladas caseras",
            "allergens": "Contiene almendras, huevos y lácteos",
            "storage": "Conservar refrigerado. Consumir en 5 días",
            "customization": "Disponible en diferentes combinaciones de sabores",
            "keywords": ["macarons", "macaron", "macarones", "galletas francesas"]
        }
    }
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Obtener configuración completa"""
        return {
            "model": {
                "name": cls.MODEL_NAME,
                "temperature": cls.MODEL_TEMPERATURE,
                "max_tokens": cls.MODEL_MAX_TOKENS,
                "base_url": cls.OLLAMA_BASE_URL
            },
            "memory": {
                "max_messages": cls.MEMORY_MAX_MESSAGES,
                "enabled": cls.MEMORY_ENABLED
            },
            "business": cls.BUSINESS_INFO,
            "products_count": len(cls.PRODUCTS)
        }
    
    @classmethod
    def search_product(cls, query: str) -> Dict[str, Any]:
        """Buscar producto en el catálogo con búsqueda mejorada"""
        query_lower = query.lower().strip()
        
        # Búsqueda exacta por nombre
        for key, product in cls.PRODUCTS.items():
            if query_lower == product["name"].lower() or query_lower in product["name"].lower():
                return product
        
        # Búsqueda por key del producto
        for key, product in cls.PRODUCTS.items():
            if query_lower in key.replace("_", " "):
                return product
        
        # Búsqueda por categoría
        for key, product in cls.PRODUCTS.items():
            if query_lower in product["category"].lower():
                return product
        
        # Búsqueda por keywords
        for key, product in cls.PRODUCTS.items():
            if 'keywords' in product:
                for keyword in product.get('keywords', []):
                    if query_lower == keyword.lower() or query_lower in keyword.lower() or keyword.lower() in query_lower:
                        return product
        
        return None


