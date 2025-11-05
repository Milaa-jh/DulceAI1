"""
Agente principal de DulceAI
Orquesta memoria, herramientas y planificación
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Importar configuraciones
from .config import AIConfig

# Importar módulos de arquitectura
from .memory.conversation_memory import ConversationMemory
from .memory.user_context import UserContext
from .tools.product_tools import ProductTools
from .tools.business_tools import BusinessTools
from .planning.task_planner import TaskPlanner
from .planning.decision_maker import DecisionMaker

# Importar dependencias de LangChain
DEPENDENCIES_AVAILABLE = False
ChatOllama = None
HumanMessage = None
AIMessage = None

try:
    # Intentar importar ChatOllama primero
    from langchain_ollama import ChatOllama
    
    # Intentar importar mensajes con múltiples fallbacks
    # IMPORTANTE: Importar directamente las clases sin acceder a atributos dinámicos
    try:
        # Usar importación directa para evitar problemas con __getattr__
        from langchain_core.messages.human import HumanMessage
        from langchain_core.messages.ai import AIMessage
        logger.info("✅ Importado desde langchain_core.messages (submódulos)")
    except ImportError as e1:
        logger.warning(f"⚠️ No se pudo importar desde submódulos: {e1}")
        try:
            # Intentar importación desde el módulo principal usando __getattr__
            import langchain_core.messages as lcm
            # Acceder a las clases directamente (esto activará __getattr__)
            HumanMessage = lcm.HumanMessage
            AIMessage = lcm.AIMessage
            logger.info("✅ Importado desde langchain_core.messages")
        except (ImportError, AttributeError, Exception) as e2:
            logger.warning(f"⚠️ No se pudo importar desde langchain_core.messages: {e2}")
            try:
                from langchain.schema.messages import HumanMessage, AIMessage
                logger.info("✅ Importado desde langchain.schema.messages")
            except ImportError as e3:
                logger.warning(f"⚠️ No se pudo importar desde langchain.schema.messages: {e3}")
                try:
                    from langchain.schema import HumanMessage, AIMessage
                    logger.info("✅ Importado desde langchain.schema")
                except ImportError as e4:
                    logger.error(f"❌ No se pudieron importar mensajes: {e4}")
                    HumanMessage = AIMessage = None
    
    # Verificar que todas las dependencias críticas estén disponibles
    if ChatOllama and HumanMessage and AIMessage:
        DEPENDENCIES_AVAILABLE = True
        logger.info("✅ Todas las dependencias de LangChain están disponibles")
    else:
        logger.warning("⚠️ Algunas dependencias de LangChain no están disponibles")
        DEPENDENCIES_AVAILABLE = False
        
except ImportError as e:
    logger.error(f"❌ Error importando dependencias de LangChain: {e}")
    DEPENDENCIES_AVAILABLE = False
except Exception as e:
    logger.error(f"❌ Error inesperado importando dependencias: {e}")
    import traceback
    logger.error(f"   Traceback: {traceback.format_exc()}")
    DEPENDENCIES_AVAILABLE = False

class DulceAIAgent:
    """
    Agente inteligente completo de DulceAI
    Implementa arquitectura completa:
    - Herramientas de consulta, escritura y razonamiento
    - Memoria de contenido y recuperación de contexto semántico
    - Planificación y toma de decisiones adaptativas
    """
    
    def __init__(self):
        """Inicializar agente completo"""
        self.llm = None
        self.config = AIConfig()
        self.is_initialized = False
        self.error_status = None
        
        # Módulos del agente
        self.memories: Dict[str, ConversationMemory] = {}
        self.user_contexts: Dict[str, UserContext] = {}
        self.product_tools: Optional[ProductTools] = None
        self.business_tools: Optional[BusinessTools] = None
        self.planner: Optional[TaskPlanner] = None
        self.decision_maker: Optional[DecisionMaker] = None
        
        logger.info("🤖 DulceAI Agent inicializado")
    
    def initialize(self) -> bool:
        """
        Inicializar todos los componentes del agente
        
        Returns:
            True si se inicializó correctamente, False si hubo errores
        """
        if not DEPENDENCIES_AVAILABLE:
            logger.error("❌ Dependencias no disponibles")
            return False
        
        try:
            logger.info("🚀 Inicializando agente DulceAI con arquitectura completa...")
            
            # Inicializar LLM
            logger.info(f"📡 Conectando con Ollama ({self.config.MODEL_NAME})...")
            self.llm = ChatOllama(
                model=self.config.MODEL_NAME,
                base_url=self.config.OLLAMA_BASE_URL,
                temperature=self.config.MODEL_TEMPERATURE
            )
            
            # Verificar conexión
            try:
                test_response = self.llm.invoke([HumanMessage(content="Hola")])
                logger.info("✅ Conexión con Ollama establecida")
                logger.info(f"📝 Respuesta de prueba: {test_response.content[:50]}...")
            except Exception as e:
                logger.error(f"❌ Error conectando con Ollama: {e}")
                self.error_status = f"OLLAMA_ERROR: {str(e)}"
                return False
            
            # Inicializar herramientas
            self.product_tools = ProductTools(self.config)
            self.business_tools = BusinessTools(self.config)
            logger.info("🔧 Herramientas inicializadas")
            
            # Inicializar planificación
            self.planner = TaskPlanner()
            self.decision_maker = DecisionMaker()
            logger.info("📋 Planificación inicializada")
            
            self.is_initialized = True
            logger.info("✅ Agente DulceAI completamente inicializado")
            logger.info("📋 Tecnologías activas:")
            logger.info("   - Herramientas de consulta, escritura y razonamiento")
            logger.info("   - Memoria de contenido y recuperación de contexto")
            logger.info("   - Planificación y toma de decisiones")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error inicializando agente: {str(e)}")
            self.error_status = f"INIT_ERROR: {str(e)}"
            return False
    
    def process_message(self, message: str, user_id: str = None) -> str:
        """
        Procesar mensaje con arquitectura completa
        
        Args:
            message: Mensaje del usuario
            user_id: Identificador del usuario
            
        Returns:
            Respuesta generada por el agente
        """
        if not self.is_initialized:
            logger.warning("⚠️ Usando respuestas predefinidas")
            return self._get_fallback_response(message)
        
        try:
            user_id = user_id or "anonymous"
            
            # Obtener o crear memoria y contexto del usuario
            memory = self._get_user_memory(user_id)
            user_context = self._get_user_context(user_id)
            
            # Actualizar última visita
            user_context.update_last_visit()
            
            # Extraer información importante del mensaje
            extracted_info = self.decision_maker.extract_important_info(message)
            
            # Actualizar contexto si es necesario
            if "name" in extracted_info:
                user_context.update_name(extracted_info["name"])
            
            if "mentioned_products" in extracted_info:
                for product in extracted_info["mentioned_products"]:
                    user_context.add_recent_product(product)
            
            # Planificar respuesta
            context = user_context.get_context_summary()
            plan = self.planner.plan_conversation(message, context)
            
            logger.info(f"📋 Plan: {len(plan)} pasos, Contexto: {len(memory.get_history())} msgs")
            
            # Decidir estilo de respuesta
            response_style = self.decision_maker.decide_response_style(context)
            
            # Construir prompt del sistema
            system_prompt = self._build_system_prompt(user_context, response_style)
            
            # Construir historial de conversación
            chat_history = self._build_chat_history(memory, user_context)
            
            # Determinar si usar herramientas
            available_tools = ["BuscarProducto", "ConsultarHorario", "ConsultarContacto", "ProcesarPedido"]
            tool_to_use = self.decision_maker.should_use_tool(message, available_tools)
            
            # Ejecutar herramienta si es necesario
            tool_result = ""
            if tool_to_use:
                tool_result = self._execute_tool(tool_to_use, message, extracted_info)
            
            # Construir mensaje completo
            full_message = self._build_full_message(message, tool_result, user_context)
            
            # Invocar LLM
            logger.info(f"🤖 Procesando con LLM ({len(chat_history)} msgs en historial)...")
            response = self.llm.invoke(chat_history + [HumanMessage(content=full_message)])
            
            # Extraer contenido de respuesta (compatible con diferentes versiones)
            response_content = getattr(response, 'content', None) or getattr(response, 'text', None) or str(response)
            
            # Guardar en memoria
            memory.add_user_message(message)
            memory.add_ai_message(response_content)
            
            logger.info("✅ Respuesta generada y guardada")
            
            return response_content.strip()
            
        except Exception as e:
            logger.error(f"❌ Error procesando mensaje: {str(e)}")
            return self._get_fallback_response(message)
    
    def _get_user_memory(self, user_id: str) -> ConversationMemory:
        """Obtener o crear memoria para usuario"""
        if user_id not in self.memories:
            self.memories[user_id] = ConversationMemory(
                max_messages=self.config.MEMORY_MAX_MESSAGES
            )
            logger.debug(f"💾 Nueva memoria creada para: {user_id}")
        return self.memories[user_id]
    
    def _get_user_context(self, user_id: str) -> UserContext:
        """Obtener o crear contexto para usuario"""
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = UserContext(user_id)
            logger.debug(f"👤 Nuevo contexto creado para: {user_id}")
        return self.user_contexts[user_id]
    
    def _build_system_prompt(self, user_context: UserContext, style: str) -> str:
        """Construir prompt del sistema personalizado"""
        base_prompt = self.config.SYSTEM_PROMPT
        
        # Agregar contexto personalizado
        personalized = user_context.build_personalized_prompt()
        if personalized:
            base_prompt += f"\n\nCONTEXTO DEL USUARIO:\n{personalized}"
        
        # Agregar estilo de respuesta
        if style == "detailed":
            base_prompt += "\n\nINSTRUCCIÓN: Sé detallado y completo en tu respuesta."
        elif style == "brief":
            base_prompt += "\n\nINSTRUCCIÓN: Sé conciso pero útil."
        elif style == "personalized":
            base_prompt += "\n\nINSTRUCCIÓN: Personaliza tu respuesta usando el nombre del usuario."
        
        return base_prompt
    
    def _build_chat_history(self, memory: ConversationMemory, user_context: UserContext) -> List:
        """Construir historial de conversación para el LLM"""
        history = []
        
        # Agregar mensajes previos (máx 8 para no sobrepasar tokens)
        for msg in memory.get_history(limit=8):
            role = msg["role"]
            content = msg["content"]
            
            if role == "user":
                history.append(HumanMessage(content=content))
            elif role == "assistant":
                history.append(AIMessage(content=content))
        
        return history
    
    def _execute_tool(self, tool_name: str, message: str, info: Dict) -> str:
        """Ejecutar herramienta específica"""
        logger.info(f"🛠️ Ejecutando herramienta: {tool_name}")
        
        if tool_name == "BuscarProducto":
            # Buscar producto mencionado
            products_mentioned = info.get("mentioned_products", [])
            if products_mentioned:
                result = self.product_tools.search_product(products_mentioned[0])
            else:
                result = self.product_tools.search_product(message)
            return result.get("message", "")
        
        elif tool_name == "ConsultarHorario":
            return self.business_tools.get_hours()
        
        elif tool_name == "ConsultarContacto":
            return self.business_tools.get_contact_info()
        
        elif tool_name == "ProcesarPedido":
            return self.business_tools.format_order_confirmation({"message": f"Pedido: {message}"})
        
        return ""
    
    def _build_full_message(self, message: str, tool_result: str, user_context: UserContext) -> str:
        """Construir mensaje completo con contexto de herramientas"""
        full_message = message
        
        if tool_result:
            full_message += f"\n\nINFORMACIÓN DISPONIBLE:\n{tool_result}\n\nUsa esta información para responder."
        
        return full_message
    
    def _get_fallback_response(self, message: str) -> str:
        """Respuestas de fallback cuando la IA no está disponible"""
        import random
        
        responses = {
            "hola": "¡Hola! 😊 Soy DulceAI. ¿En qué puedo ayudarte?",
            "producto": "Tenemos varios productos. ¿Buscas algo específico?",
            "precio": "Los precios varían. ¿Qué producto te interesa?",
            "pedido": "¡Genial! ¿Qué te gustaría pedir?",
            "horario": "Lunes a Sábado: 8:00 AM - 8:00 PM",
            "contacto": "Contacto: +57 300 123 4567"
        }
        
        message_lower = message.lower()
        for key, response in responses.items():
            if key in message_lower:
                return response
        
        return "Interesante consulta. ¿Podrías ser más específico?"
    
    def get_status(self) -> Dict[str, Any]:
        """Obtener estado completo del agente"""
        return {
            "initialized": self.is_initialized,
            "model_name": self.config.MODEL_NAME,
            "ollama_url": self.config.OLLAMA_BASE_URL,
            "memory_enabled": self.config.MEMORY_ENABLED,
            "active_users": len(self.memories),
            "tools_available": [
                "BuscarProducto",
                "ConsultarHorario",
                "ConsultarContacto",
                "ProcesarPedido"
            ],
            "error_status": self.error_status,
            "dependencies_available": DEPENDENCIES_AVAILABLE,
            "architecture": "Agentes LLM con Memoria y Planificación",
            "timestamp": str(datetime.now().isoformat())
        }

