# 🍰 DulceAI - E-commerce de Pastelería con IA

Un e-commerce moderno de pastelería con **Inteligencia Artificial completamente funcional** usando Ollama (gemma2:2b) y LangChain. Incluye animaciones GSAP, estilos Tailwind y un chatbot completamente operativo.

## 🎯 Características Principales

- **Frontend Moderno**: HTML5, CSS3, JavaScript con animaciones GSAP
- **Diseño Responsivo**: Tailwind CSS con paleta de colores pastel
- **Chatbot con IA Real**: Burbuja flotante con **Ollama gemma2:2b** completamente integrado
- **Backend Escalable**: FastAPI con IA funcional usando LangChain
- **Integración IA Completa**: LangChain + Ollama + ChatOllama operativo
- **Prompts Especializados**: Sistema de prompts para asistente de pastelería
- **Listo para RAG**: Arquitectura preparada para ChromaDB/FAISS
- **Evaluación IA**: Listo para integración con LangSmith

## 📂 Estructura del Proyecto

```
dulceai/
├── frontend/
│   ├── index.html          # Página principal
│   ├── styles.css          # Estilos personalizados
│   ├── main.js            # Animaciones GSAP
│   ├── chat.js            # Lógica del chatbot
│   ├── package.json       # Dependencias frontend
│   ├── tailwind.config.js # Configuración Tailwind
│   └── assets/
│       ├── mockups/       # Imágenes de productos
│       └── icons/         # Iconos del sitio
├── backend/
│   ├── app.py            # Servidor FastAPI
│   └── ia_placeholder.py # Integración IA (placeholder)
├── requirements.txt       # Dependencias Python
└── README.md            # Este archivo
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- **Python**: >= 3.8 (probado con 3.12)
- **Node.js**: >= 16.0.0
- **npm**: >= 8.0.0
- **Ollama**: >= 0.1.0 (debe estar instalado y ejecutándose con modelo gemma2:2b)

### 1. Clonar el Proyecto

```bash
git clone https://github.com/Milaa-jh/Dulceai.git
cd dulceai
```

### 2. Configurar Backend (Python)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar Tailwind CSS
npx tailwindcss init
```

### 4. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# API Keys (opcional para desarrollo)
OPENAI_API_KEY=tu_api_key_aqui
LANGSMITH_API_KEY=tu_api_key_aqui
LANGSMITH_PROJECT=dulceai

# Base de datos (opcional)
DATABASE_URL=postgresql://user:password@localhost/dulceai
REDIS_URL=redis://localhost:6379

# Configuración del servidor
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 🎮 Ejecución del Proyecto

### Desarrollo Local

#### Backend (Terminal 1)
```bash
# Activar entorno virtual
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Iniciar servidor FastAPI
cd backend
python app.py

# O usando uvicorn directamente:
# uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (Terminal 2)
```bash
cd frontend

# Servidor de desarrollo simple
python -m http.server 3000

# O usar Live Server en VS Code
```

### Acceso a la Aplicación

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Estado IA**: http://localhost:8000/api/ai/status

### 🤖 Probar el Chatbot con IA

1. Abre http://localhost:3000 en tu navegador
2. Haz clic en el ícono del chatbot (💬) en la esquina inferior derecha
3. Escribe un mensaje como:
   - "¿Qué productos tienen?"
   - "Quiero hacer un pedido de cupcakes para un cumpleaños"
   - "¿Cuánto cuesta una torta?"
4. El chatbot responderá usando **Ollama gemma2:2b** con IA real

## 🎨 Características del Frontend

### Secciones Principales

1. **Inicio (Home)**
   - Hero con título animado
   - Imagen mockup de vitrina pastelera
   - Botón "Explorar Pasteles" con hover interactivo

2. **Productos**
   - Grid con tarjetas de productos
   - Hover animado con GSAP
   - Botones "Agregar al carrito" funcionales

3. **Sobre Nosotros**
   - Información del equipo
   - Animaciones con ScrollTrigger

4. **Contacto**
   - Formulario funcional
   - Validación y animaciones de envío

5. **Chatbot Flotante**
   - Burbuja animada en esquina inferior derecha
   - Ventana expandible con GSAP
   - Preparado para integración con IA

### Animaciones GSAP

- **Entrada**: FadeIn, SlideUp, ScaleIn
- **ScrollTrigger**: Animaciones al hacer scroll
- **Hover**: Efectos interactivos en productos
- **Chatbot**: Apertura/cierre suave
- **Formularios**: Validación visual

### Paleta de Colores

```css
--pink-primary: #ec4899
--pink-light: #fce7f3
--pink-dark: #be185d
--blue-primary: #3b82f6
--blue-light: #dbeafe
--blue-dark: #1e40af
--cream: #fefce8
```

## 🧠 Integración de IA (Completamente Funcional)

### Arquitectura: Agentes LLM con Memoria, Herramientas y Planificación

Este proyecto implementa arquitectura completa:

#### Diagrama de Orquestación de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Chat)                           │
│                    (JavaScript + HTML/CSS)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/JSON
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND API (FastAPI)                         │
│                         app.py                                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              DULCEAI AGENT (ia_placeholder.py)                  │
│                    ┌──────────────────┐                         │
│                    │  LangChain Agent │                         │
│                    │ (Function Calling│                         │
│                    │      Real)       │                         │
│                    └────────┬─────────┘                         │
│                             │                                    │
│        ┌────────────────────┼────────────────────┐              │
│        │                    │                    │              │
│        ▼                    ▼                    ▼              │
│  ┌──────────┐      ┌──────────────┐      ┌─────────────┐       │
│  │ Memory   │      │  Planning   │      │   Tools     │       │
│  │          │      │             │      │             │       │
│  └──────────┘      └──────────────┘      └─────────────┘       │
│        │                    │                    │              │
│        │                    │                    │              │
│        ▼                    ▼                    ▼              │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  ConversationBufferMemory  │  TaskPlanner  │  Tools  │     │
│  │  UserContext               │  DecisionMaker│  Product│     │
│  │  (Recuperación Semántica)  │  (Adaptativo) │  Business│    │
│  └───────────────────────────────────────────────────────┘     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     LLM (Ollama - gemma2:2b)                    │
│                    http://localhost:11434                       │
└─────────────────────────────────────────────────────────────────┘
```

#### Componentes Implementados

**Herramientas de Consulta, Escritura y Razonamiento** ✅
- **Function Calling Real**: LangChain Agents con `initialize_agent` y `AgentType.ZERO_SHOT_REACT_DESCRIPTION`
- **Herramientas Implementadas**:
  - `BuscarProducto`: Consulta de productos en catálogo
  - `ConsultarHorario`: Información de horarios de atención
  - `ConsultarContacto`: Información de contacto del negocio
  - `ProcesarPedido`: Procesamiento de pedidos de clientes
- **Frameworks**: LangChain Agents con escalabilidad y compatibilidad técnica garantizada
- **Integración**: Herramientas conectadas con módulos RAG (`ProductTools`, `BusinessTools`)

**Memoria de Contenido y Recuperación de Contexto Semántico** ✅
- **Memoria de Contenido**: `ConversationBufferMemory` de LangChain por usuario
- **Recuperación de Contexto Semántico**: `UserContext` con información personalizada
- **Continuidad**: Memoria persistente que mantiene coherencia en flujos prolongados
- **Implementación**: `ConversationMemory` y `UserContext` en módulos RAG

**Planificación y Toma de Decisiones Adaptativas** ✅
- **Planificación Jerárquica**: `TaskPlanner` que descompone objetivos en tareas secuenciales
- **Toma de Decisiones**: `DecisionMaker` que ajusta comportamiento según condiciones
- **Adaptabilidad**: Sistema que ajusta estrategias según contexto del usuario
- **Priorización**: Esquemas de planificación que secuencian actividades según prioridades

**Documentación Técnica** ✅
- **README Detallado**: Este archivo con arquitectura explicada
- **Diagramas**: Diagrama de orquestación de componentes
- **Justificación**: Documentación de elección de componentes y alineación con requerimientos

### Tecnologías Implementadas

1. **LangChain** ✅
   - ChatOllama para integración con Ollama
   - **Agents con Function Calling Real**: `initialize_agent` con `AgentType.ZERO_SHOT_REACT_DESCRIPTION`
   - `ConversationBufferMemory` para memoria conversacional
   - Prompts templates especializados
   - Mensajes estructurados (SystemMessage, HumanMessage)

2. **Ollama** ✅
   - **Modelo activo**: gemma2:2b
   - Configuración de temperatura: 0.7
   - Manejo de tokens configurado
   - Streaming habilitado
   - Base URL: http://localhost:11434

3. **Prompts Especializados** ✅
   - Sistema de prompts para asistente de pastelería
   - Respuestas en español
   - Tono amigable y profesional
   - Especializado en productos de repostería

4. **RAG (Preparado para implementación)** 🔄
   - ChromaDB para almacenamiento vectorial
   - FAISS como alternativa
   - Embeddings con OpenAI/SentenceTransformers
   - Arquitectura lista para chunking y retrieval

5. **LangSmith (Preparado)** 🔄
   - Evaluación de respuestas
   - Monitoreo de performance
   - Métricas de calidad
   - Listo para configuración

6. **Streamlit (Preparado)** 🔄
   - Interfaz de administración
   - Configuración de modelos
   - Monitoreo en tiempo real

### Flujo RAG Preparado

```python
# 1. Chunking de documentos
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# 2. Crear embeddings
embeddings = OpenAIEmbeddings()

# 3. Almacenar en vector store
vector_store = Chroma.from_documents(
    chunks, 
    embeddings
)

# 4. Retrieval
relevant_docs = vector_store.similarity_search(query, k=3)

# 5. Generación con contexto
response = llm_chain.run(
    context=context,
    question=query
)
```

## 🔧 API Endpoints

### Productos
- `GET /api/products` - Listar todos los productos
- `GET /api/products/{id}` - Obtener producto específico
- `GET /api/products/category/{category}` - Productos por categoría

### Chat
- `POST /api/chat` - Enviar mensaje al chatbot
- `GET /api/chat/history` - Obtener historial de chat

### Contacto
- `POST /api/contact` - Enviar mensaje de contacto
- `GET /api/contact/messages` - Obtener mensajes (admin)

### Sistema
- `GET /health` - Estado del servidor
- `GET /api/stats` - Estadísticas del sistema

## 📱 Responsive Design

El sitio está optimizado para:
- **Desktop**: >= 1024px
- **Tablet**: 768px - 1023px
- **Mobile**: < 768px

### Breakpoints Tailwind
```css
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
```

## 🧪 Testing

### Backend
```bash
# Ejecutar tests
pytest tests/

# Con cobertura
pytest --cov=backend tests/
```

### Frontend
```bash
# Tests manuales en navegador
# Abrir DevTools y probar funcionalidades
```

## 🚀 Despliegue

### Desarrollo
```bash
# Backend
uvicorn backend.app:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend && python -m http.server 3000
```

### Producción

#### Backend
```bash
# Con Gunicorn
gunicorn backend.app:app -w 4 -k uvicorn.workers.UvicornWorker

# Con Docker
docker build -t dulceai-backend .
docker run -p 8000:8000 dulceai-backend
```

#### Frontend
```bash
# Build para producción
npm run build

# Servir con nginx
# Configurar nginx para servir archivos estáticos
```

## 🔒 Seguridad

- **CORS**: Configurado para desarrollo
- **Validación**: Pydantic para datos
- **Autenticación**: Preparada para JWT
- **HTTPS**: Recomendado para producción

## 📊 Monitoreo

### Métricas Disponibles
- Estado del servidor
- Número de productos
- Mensajes de chat procesados
- Mensajes de contacto recibidos

### Logs
- Logging configurado con Python logging
- Niveles: INFO, WARNING, ERROR
- Rotación automática de logs

## 🤝 Contribución

1. Fork el proyecto
2. Crear branch para feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -m 'Agregar nueva característica'`)
4. Push al branch (`git push origin feature/nueva-caracteristica`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

Para soporte y preguntas:
- **Email**: info@dulceai.com
- **Teléfono**: +57 300 123 4567
- **Issues**: Usar GitHub Issues

## 📊 Estado del Proyecto

### ✅ Completado
- Frontend completo con animaciones GSAP
- Backend FastAPI con endpoints funcionales
- **IA completamente funcional con Ollama gemma2:2b**
- Chatbot flotante integrado
- LangChain configurado y operativo
- Sistema de prompts especializados
- Documentación completa

### 🔄 En Desarrollo
- Implementación de RAG con ChromaDB
- Integración con LangSmith para evaluación
- Interfaz Streamlit para administración

### 📋 Pendiente
- Sistema de usuarios y autenticación
- Carrito de compras persistente
- Procesamiento de pagos
- Sistema de inventario
- Cache con Redis
- Optimización de imágenes
- PWA (Progressive Web App)

## 🔮 Roadmap Futuro

### Fase 1: Integración IA Completa ✅
- [x] Integrar Ollama local
- [x] Implementar LangChain completo
- [x] Configurar ChatOllama con gemma2:2b
- [x] Sistema de prompts especializados
- [ ] Configurar ChromaDB/FAISS (RAG)
- [ ] Conectar LangSmith (evaluación)

### Fase 2: Funcionalidades Avanzadas
- [ ] Sistema de usuarios
- [ ] Carrito de compras persistente
- [ ] Procesamiento de pagos
- [ ] Sistema de inventario

### Fase 3: Optimización
- [ ] Cache con Redis
- [ ] CDN para assets
- [ ] Optimización de imágenes
- [ ] PWA (Progressive Web App)

## 📚 Recursos Adicionales

### Documentación
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [GSAP Docs](https://greensock.com/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [LangChain Docs](https://python.langchain.com/)

### Tutoriales
- [GSAP ScrollTrigger](https://greensock.com/scrolltrigger/)
- [Tailwind Animations](https://tailwindcss.com/docs/animation)
- [FastAPI + React](https://fastapi.tiangolo.com/tutorial/)

---

**¡Disfruta desarrollando con DulceAI! 🍰✨**



