"""Sistema de logging estructurado para trazabilidad del agente DulceAI.

Este módulo implementa logging en formato JSON para facilitar el análisis
de la ejecución del agente y debugging de problemas.
"""

import json
import random
import string
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class StructuredLogger:
    """Logger estructurado para el agente de IA.
    
    Genera logs en formato JSON (una línea por evento) para facilitar
    el análisis y trazabilidad de las ejecuciones del agente.
    """
    
    def __init__(self, log_file: str = "backend/logs/agent.log"):
        """Inicializa el logger estructurado.
        
        Args:
            log_file: Ruta al archivo donde se guardarán los logs
        """
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def generate_trace_id(self) -> str:
        """Genera un ID único de trazabilidad de 8 caracteres.
        
        Returns:
            String único de 8 caracteres alfanuméricos
        """
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    def _write_log(self, level: str, event: str, trace_id: Optional[str], data: Dict[str, Any]) -> None:
        """Escribe una entrada de log en formato JSON.
        
        Args:
            level: Nivel del log (INFO, WARNING, ERROR, DEBUG)
            event: Tipo de evento
            trace_id: ID de trazabilidad de la request
            data: Datos adicionales del evento
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'event': event,
            'trace_id': trace_id,
            'data': data
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def log_request_start(self, trace_id: str, query: str, session_id: str) -> None:
        """Registra el inicio de una request del usuario.
        
        Args:
            trace_id: ID único de trazabilidad
            query: Consulta del usuario
            session_id: ID de sesión del usuario
        """
        self._write_log(
            level='INFO',
            event='request_start',
            trace_id=trace_id,
            data={
                'query': query,
                'session_id': session_id,
                'query_length': len(query)
            }
        )
    
    def log_request_end(self, trace_id: str, response: str, latency: float, status: str) -> None:
        """Registra el fin de una request.
        
        Args:
            trace_id: ID único de trazabilidad
            response: Respuesta generada
            latency: Tiempo total de procesamiento en segundos
            status: Estado de la request (success/error)
        """
        self._write_log(
            level='INFO',
            event='request_end',
            trace_id=trace_id,
            data={
                'response_length': len(response),
                'latency': latency,
                'status': status
            }
        )
    
    def log_action(self, trace_id: str, tool_name: str, input_data: Any) -> None:
        """Registra una acción (llamada a herramienta) del agente.
        
        Args:
            trace_id: ID de trazabilidad
            tool_name: Nombre de la herramienta llamada
            input_data: Datos de entrada a la herramienta
        """
        self._write_log(
            level='INFO',
            event='action',
            trace_id=trace_id,
            data={
                'tool_name': tool_name,
                'input': str(input_data)[:200]  # Limitar longitud
            }
        )
    
    def log_observation(self, trace_id: str, tool_name: str, result: Any, latency: float) -> None:
        """Registra la observación (resultado de herramienta).
        
        Args:
            trace_id: ID de trazabilidad
            tool_name: Nombre de la herramienta ejecutada
            result: Resultado de la ejecución
            latency: Tiempo de ejecución en segundos
        """
        self._write_log(
            level='INFO',
            event='observation',
            trace_id=trace_id,
            data={
                'tool_name': tool_name,
                'result': str(result)[:200],  # Limitar longitud
                'latency': latency
            }
        )
    
    def log_error(self, trace_id: Optional[str], component: str, error_type: str, message: str) -> None:
        """Registra un error del sistema.
        
        Args:
            trace_id: ID de trazabilidad (puede ser None si error global)
            component: Componente donde ocurrió el error
            error_type: Tipo de error
            message: Mensaje de error
        """
        self._write_log(
            level='ERROR',
            event='error',
            trace_id=trace_id,
            data={
                'component': component,
                'error_type': error_type,
                'message': message
            }
        )
    
    def log_memory_update(self, trace_id: str, session_id: str, action: str) -> None:
        """Registra actualizaciones en la memoria conversacional.
        
        Args:
            trace_id: ID de trazabilidad
            session_id: ID de sesión
            action: Acción realizada (add_message, clear, etc.)
        """
        self._write_log(
            level='DEBUG',
            event='memory_update',
            trace_id=trace_id,
            data={
                'session_id': session_id,
                'action': action
            }
        )
    
    def log_llm_call(self, trace_id: str, model: str, tokens_input: int, tokens_output: int, latency: float) -> None:
        """Registra llamadas al modelo de lenguaje.
        
        Args:
            trace_id: ID de trazabilidad
            model: Nombre del modelo usado
            tokens_input: Tokens de entrada
            tokens_output: Tokens de salida
            latency: Tiempo de la llamada en segundos
        """
        self._write_log(
            level='DEBUG',
            event='llm_call',
            trace_id=trace_id,
            data={
                'model': model,
                'tokens_input': tokens_input,
                'tokens_output': tokens_output,
                'latency': latency
            }
        )
    
    def log_security_check(self, trace_id: str, check_type: str, result: str, details: Optional[str] = None) -> None:
        """Registra verificaciones de seguridad.
        
        Args:
            trace_id: ID de trazabilidad
            check_type: Tipo de verificación (rate_limit, prompt_injection, pii, etc.)
            result: Resultado (passed/blocked)
            details: Detalles adicionales opcionales
        """
        self._write_log(
            level='WARNING' if result == 'blocked' else 'INFO',
            event='security_check',
            trace_id=trace_id,
            data={
                'check_type': check_type,
                'result': result,
                'details': details
            }
        )


# Instancia global singleton
_logger: Optional[StructuredLogger] = None


def get_logger() -> StructuredLogger:
    """Obtiene la instancia singleton del logger estructurado.
    
    Returns:
        Instancia de StructuredLogger
    """
    global _logger
    if _logger is None:
        _logger = StructuredLogger()
    return _logger
