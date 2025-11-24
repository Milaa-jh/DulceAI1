# DulceAI - Backend FastAPI
# Archivo principal de la aplicación backend con integración completa de IA

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
import time
from datetime import datetime
import logging

# Configurar logging PRIMERO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar sistema de monitoreo
try:
    from src.monitoring.metrics import get_metrics_collector
    from src.monitoring.logger import get_logger
    from src.monitoring.security import SecurityValidator, get_rate_limiter
    MONITORING_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Sistema de monitoreo no disponible: {e}")
    MONITORING_AVAILABLE = False

# Importar sistema de IA
try:
    from ia_placeholder import initialize_ai_system, process_chat_message, get_ai_status
    AI_AVAILABLE = True
    logger.info("✅ Sistema de IA disponible")
except ImportError as e:
    AI_AVAILABLE = False
    logger.error(f"❌ Sistema de IA no disponible: {e}")

# Inicializar IA al importar el módulo
if AI_AVAILABLE:
    try:
        initialize_ai_system()
        logger.info("✅ IA inicializada al importar")
    except Exception as e:
        logger.error(f"❌ Error inicializando IA: {e}")

# Crear instancia de FastAPI
app = FastAPI(
    title="DulceAI Backend",
    description="Backend para e-commerce de pastelería con IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None
    timestamp: Optional[datetime] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
    message_id: str

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: str
    category: str
    available: bool = True

class ContactMessage(BaseModel):
    name: str
    email: str
    message: str
    timestamp: Optional[datetime] = None

# Base de datos simulada (en producción usar PostgreSQL/MongoDB)
products_db = [
    Product(
        id=1,
        name="Torta de Chocolate",
        description="Deliciosa torta de chocolate con crema batida y fresas frescas",
        price=25000.0,
        image_url="/assets/mockups/torta-chocolate.jpg",
        category="tortas"
    ),
    Product(
        id=2,
        name="Cupcakes Variados",
        description="Set de 6 cupcakes con diferentes sabores y decoraciones únicas",
        price=18000.0,
        image_url="/assets/mockups/cupcakes.jpg",
        category="cupcakes"
    ),
    Product(
        id=3,
        name="Galletas Artesanales",
        description="Galletas caseras con ingredientes naturales y sabores únicos",
        price=12000.0,
        image_url="/assets/mockups/galletas.jpg",
        category="galletas"
    ),
    Product(
        id=4,
        name="Cheesecake de Fresa",
        description="Suave cheesecake con salsa de fresa casera y base de galleta",
        price=22000.0,
        image_url="/assets/mockups/cheesecake.jpg",
        category="cheesecakes"
    ),
    Product(
        id=5,
        name="Pie de Manzana",
        description="Tradicional pie de manzana con canela y crujiente masa",
        price=20000.0,
        image_url="/assets/mockups/pie-manzana.jpg",
        category="pies"
    ),
    Product(
        id=6,
        name="Donas Glaseadas",
        description="Donas esponjosas con diferentes tipos de glaseado y toppings",
        price=15000.0,
        image_url="/assets/mockups/donas.jpg",
        category="donas"
    )
]

# Almacenamiento temporal para mensajes de chat
chat_history = []

# Almacenamiento temporal para mensajes de contacto
contact_messages = []

# Rutas principales
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Página principal - redirige al frontend"""
    return """
    <html>
        <head>
            <title>DulceAI Backend</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .container { max-width: 600px; margin: 0 auto; }
                .logo { font-size: 3em; margin-bottom: 20px; }
                .status { color: #10b981; font-weight: bold; }
                .docs-link { margin-top: 30px; }
                a { color: #ec4899; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">🍰 DulceAI</div>
                <h1>Backend API Activo</h1>
                <p class="status">✅ Servidor funcionando correctamente</p>
                <p>Backend para e-commerce de pastelería con inteligencia artificial</p>
                <div class="docs-link">
                    <a href="/docs">📚 Ver Documentación API</a>
                </div>
                <div class="docs-link">
                    <a href="/redoc">📖 Documentación Alternativa</a>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Endpoint de salud del servidor"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "service": "DulceAI Backend",
        "version": "1.0.0"
    }

# Rutas de productos
@app.get("/api/products", response_model=List[Product])
async def get_products():
    """Obtener todos los productos disponibles"""
    return products_db

@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """Obtener un producto específico por ID"""
    product = next((p for p in products_db if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@app.get("/api/products/category/{category}")
async def get_products_by_category(category: str):
    """Obtener productos por categoría"""
    filtered_products = [p for p in products_db if p.category == category]
    return filtered_products

# Rutas de chat (integración completa con IA)
@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(message: ChatMessage):
    """
    Endpoint para chat con IA usando RAG completo
    Integra: LangChain + Ollama + ChromaDB + LangSmith + Observabilidad
    
    IMPORTANTE: Devuelve 503 si la IA no está disponible o no está inicializada
    """
    # Inicializar componentes de monitoreo
    trace_id = None
    start_time = time.time()
    status = "error"
    response_text = ""
    
    if MONITORING_AVAILABLE:
        metrics = get_metrics_collector()
        mon_logger = get_logger()
        security = SecurityValidator()
        rate_limiter = get_rate_limiter()
        
        # Generar trace_id
        trace_id = mon_logger.generate_trace_id()
        
        # Validar rate limit
        user_id = message.user_id or "anonymous"
        allowed, rate_msg = rate_limiter.check_rate_limit(user_id)
        if not allowed:
            mon_logger.log_security_check(trace_id, "rate_limit", "blocked", rate_msg)
            raise HTTPException(status_code=429, detail=rate_msg)
        
        mon_logger.log_security_check(trace_id, "rate_limit", "passed")
        
        # Validar input contra prompt injection
        valid, injection_msg = security.validate_input(message.message)
        if not valid:
            mon_logger.log_security_check(trace_id, "prompt_injection", "blocked", injection_msg)
            raise HTTPException(status_code=400, detail=f"Input rechazado: {injection_msg}")
        
        mon_logger.log_security_check(trace_id, "prompt_injection", "passed")
        
        # Sanitizar PII antes de loggear
        sanitized_query = security.sanitize_pii(message.message)
        
        # Iniciar registro de request
        metrics.start_request(trace_id, sanitized_query, user_id)
        mon_logger.log_request_start(trace_id, sanitized_query, user_id)
    
    try:
        if not AI_AVAILABLE:
            raise HTTPException(
                status_code=503, 
                detail="Sistema de IA no disponible. Verifique las dependencias."
            )
        
        # Verificar estado de la IA antes de procesar
        ai_status = get_ai_status()
        if not ai_status.get("initialized", False):
            raise HTTPException(
                status_code=503,
                detail="Sistema de IA no está inicializado. El chatbot no está disponible."
            )
        
        # Procesar mensaje con RAG completo
        try:
            response_text = process_chat_message(message.message, message.user_id)
        except RuntimeError as e:
            # Si la IA no está disponible, devolver 503
            logger.error(f"❌ IA no disponible: {str(e)}")
            if MONITORING_AVAILABLE:
                mon_logger.log_error(trace_id, "agent", "RuntimeError", str(e))
                metrics.track_error("agent", "RuntimeError", str(e))
            raise HTTPException(
                status_code=503,
                detail=f"Sistema de IA no disponible: {str(e)}"
            )
        
        # Verificar si hay errores en la respuesta
        if response_text.startswith("❌ Error del sistema:"):
            error_detail = response_text.replace("❌ Error del sistema: ", "")
            if MONITORING_AVAILABLE:
                mon_logger.log_error(trace_id, "agent", "SystemError", error_detail)
                metrics.track_error("agent", "SystemError", error_detail)
            raise HTTPException(
                status_code=500,
                detail=f"Error del sistema de IA: {error_detail}"
            )
        
        # Crear respuesta exitosa
        response = ChatResponse(
            response=response_text,
            timestamp=datetime.now(),
            message_id=f"msg_{len(chat_history)}_{datetime.now().timestamp()}"
        )
        
        # Guardar en historial
        chat_history.append({
            "user_message": message.message,
            "ai_response": response_text,
            "timestamp": datetime.now(),
            "user_id": message.user_id
        })
        
        status = "success"
        logger.info(f"✅ Mensaje procesado exitosamente: {message.message[:50]}...")
        
        # Finalizar registro de request
        if MONITORING_AVAILABLE:
            latency = time.time() - start_time
            metrics.end_request(response_text, status)
            mon_logger.log_request_end(trace_id, response_text, latency, status)
        
        return response
        
    except HTTPException:
        if MONITORING_AVAILABLE:
            metrics.end_request(response_text or "", "error")
        raise
    except Exception as e:
        logger.error(f"❌ Error procesando mensaje de chat: {str(e)}")
        if MONITORING_AVAILABLE:
            mon_logger.log_error(trace_id, "api", "Exception", str(e))
            metrics.track_error("api", "Exception", str(e))
            metrics.end_request("", "error")
        raise HTTPException(status_code=503, detail=f"Sistema de IA no disponible: {str(e)}")

@app.get("/api/ai/status")
async def get_ai_system_status():
    """
    Obtener estado detallado del sistema de IA
    """
    try:
        if not AI_AVAILABLE:
            return {
                "ai_available": False,
                "error": "Sistema de IA no disponible",
                "timestamp": datetime.now()
            }
        
        status = get_ai_status()
        status["ai_available"] = True
        return status
        
    except Exception as e:
        logger.error(f"❌ Error obteniendo estado de IA: {str(e)}")
        return {
            "ai_available": False,
            "error": str(e),
            "timestamp": datetime.now()
        }

@app.get("/api/chat/history")
async def get_chat_history(limit: int = 50):
    """Obtener historial de chat"""
    return chat_history[-limit:]

# Rutas de contacto
@app.post("/api/contact")
async def send_contact_message(contact: ContactMessage):
    """Enviar mensaje de contacto"""
    try:
        contact.timestamp = datetime.now()
        contact_messages.append(contact.dict())
        
        logger.info(f"Contact message received from: {contact.email}")
        
        return {
            "status": "success",
            "message": "Mensaje enviado correctamente",
            "timestamp": contact.timestamp
        }
        
    except Exception as e:
        logger.error(f"Error processing contact message: {str(e)}")
        raise HTTPException(status_code=500, detail="Error procesando mensaje de contacto")

@app.get("/api/contact/messages")
async def get_contact_messages(limit: int = 100):
    """Obtener mensajes de contacto (solo para administradores)"""
    return contact_messages[-limit:]

# Función para simular respuesta de IA (placeholder)
async def simulate_ai_response(user_message: str) -> str:
    """
    Simular respuesta de IA
    TODO: Reemplazar con integración real de Ollama + LangChain
    """
    message_lower = user_message.lower()
    
    # Respuestas predefinidas (placeholder)
    responses = {
        "hola": "¡Hola! Soy el asistente virtual de DulceAI. ¿En qué puedo ayudarte?",
        "precio": "Los precios varían según el producto. Puedes revisar nuestra sección de productos para ver todos los precios.",
        "pastel": "¡Excelente elección! Tenemos una gran variedad de pasteles. ¿Te gustaría conocer nuestros productos más populares?",
        "cupcake": "¡Los cupcakes son una de nuestras especialidades! Tenemos diferentes sabores y decoraciones.",
        "galleta": "Nuestras galletas artesanales son deliciosas! Están hechas con ingredientes naturales.",
        "cheesecake": "¡El cheesecake de fresa es uno de nuestros productos estrella! Está hecho con ingredientes frescos.",
        "pedido": "¡Perfecto! Para hacer un pedido, puedes agregar los productos que te gusten al carrito.",
        "entrega": "Ofrecemos servicio de entrega a domicilio. Los tiempos y costos varían según la ubicación.",
        "horario": "Nuestro horario de atención es de lunes a sábado de 8:00 AM a 8:00 PM.",
        "contacto": "Puedes contactarnos por teléfono al +57 300 123 4567 o por email a info@dulceai.com.",
        "gracias": "¡De nada! Fue un placer ayudarte. ¿Hay algo más en lo que pueda asistirte?",
        "adios": "¡Hasta luego! Espero verte pronto disfrutando de nuestros deliciosos productos."
    }
    
    # Buscar respuesta apropiada
    for keyword, response in responses.items():
        if keyword in message_lower:
            return response
    
    # Respuesta por defecto
    default_responses = [
        "Interesante pregunta. Déjame ayudarte con eso. ¿Podrías ser más específico?",
        "Entiendo tu consulta. Puedo ayudarte con información sobre nuestros productos y servicios.",
        "¡Excelente pregunta! Me gustaría ayudarte mejor. ¿Podrías contarme más detalles?",
        "Comprendo tu interés. Para darte la mejor respuesta, ¿podrías ser más específico?",
        "¡Me encanta ayudarte! Estoy aquí para responder tus preguntas sobre DulceAI."
    ]
    
    import random
    return random.choice(default_responses)

# Rutas de estadísticas (para administradores)
@app.get("/api/stats")
async def get_stats():
    """Obtener estadísticas del sistema"""
    return {
        "total_products": len(products_db),
        "total_chat_messages": len(chat_history),
        "total_contact_messages": len(contact_messages),
        "uptime": "Activo",
        "timestamp": datetime.now()
    }

# Configuración para servir archivos estáticos (frontend)
# En producción, usar nginx o CDN
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Manejo de errores
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint no encontrado", "status_code": 404}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Error interno del servidor", "status_code": 500}
    )

# Función principal para ejecutar el servidor
if __name__ == "__main__":
    logger.info("🍰 Iniciando servidor DulceAI Backend...")
    
    # Inicializar sistema de IA si está disponible
    if AI_AVAILABLE:
        logger.info("🤖 Inicializando sistema de IA...")
        ai_success = initialize_ai_system()
        
        if ai_success:
            logger.info("✅ Sistema de IA inicializado correctamente")
            logger.info("📋 Tecnologías activas:")
            logger.info("   - LangChain + Ollama (gemma2:2b)")
            logger.info("   - Prompt Engineering avanzado")
            logger.info("   - RAG con ChromaDB")
            logger.info("   - Evaluación con LangSmith")
        else:
            logger.error("❌ Error inicializando sistema de IA")
            logger.error("⚠️ El chatbot funcionará en modo limitado")
    else:
        logger.warning("⚠️ Sistema de IA no disponible")
        logger.warning("⚠️ Instale las dependencias para funcionalidad completa")
    
    logger.info("🚀 Servidor listo para recibir conexiones")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

