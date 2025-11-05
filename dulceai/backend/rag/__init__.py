# DulceAI RAG - Sistema modular de Inteligencia Artificial
# Estructura modular para agentes LLM con memoria, herramientas y planificación

from .config import AIConfig

# NO importar DulceAIAgent automáticamente para evitar problemas con dependencias de LangChain
# Los usuarios deben importarlo directamente: from rag.agent import DulceAIAgent

__all__ = ['AIConfig']


