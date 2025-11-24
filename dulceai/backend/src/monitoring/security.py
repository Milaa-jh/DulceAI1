"""Sistema de seguridad y validación para el agente DulceAI.

Este módulo implementa protocolos de seguridad incluyendo:
- Detección de prompt injection
- Sanitización de PII (información personal identificable)
- Rate limiting
- Validación de contenido
"""

import re
import time
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class SecurityValidator:
    """Validador de seguridad para inputs y outputs del agente.
    
    Implementa protecciones contra:
    - Prompt injection
    - Leakage de PII
    - Contenido malicioso
    """
    
    # Patrones de prompt injection
    PROMPT_INJECTION_PATTERNS = [
        r"ignore\s+(previous|all|above)\s+instructions?",
        r"disregard\s+(all|previous|above)\s+instructions?",
        r"you\s+are\s+now",
        r"act\s+as\s+(?:a\s+)?(?!customer|user)",  # Permitir "act as a customer"
        r"pretend\s+(?:to\s+be|you\s+are)",
        r"forget\s+(?:everything|all|your)",
        r"new\s+instruction",
        r"system\s*:\s*you",
        r"override\s+(?:your|previous)",
    ]
    
    # Patrones de PII
    PII_PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b(?:\+?56|0)?\s*[2-9]\d{8}\b',  # Teléfonos chilenos
        'rut': r'\b\d{1,2}\.\d{3}\.\d{3}[-]?[\dkK]\b',  # RUT chileno
        'credit_card': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
    }
    
    def __init__(self):
        """Inicializa el validador de seguridad."""
        self.injection_regex = re.compile(
            '|'.join(self.PROMPT_INJECTION_PATTERNS),
            re.IGNORECASE
        )
    
    def validate_input(self, user_input: str) -> Tuple[bool, Optional[str]]:
        """Valida el input del usuario contra prompt injection.
        
        Args:
            user_input: Input del usuario a validar
            
        Returns:
            Tupla (es_valido, razon_rechazo)
            - es_valido: True si el input es seguro, False si se detectó inyección
            - razon_rechazo: Descripción del problema si es_valido=False, None si es_valido=True
        """
        # Verificar longitud
        if len(user_input) > 2000:
            return False, "Input excede longitud máxima permitida (2000 caracteres)"
        
        # Detectar prompt injection
        match = self.injection_regex.search(user_input)
        if match:
            return False, f"Posible prompt injection detectado: '{match.group()}'"
        
        return True, None
    
    def sanitize_pii(self, text: str) -> str:
        """Remueve información personal identificable del texto.
        
        Args:
            text: Texto a sanitizar
            
        Returns:
            Texto con PII reemplazada por placeholders
        """
        sanitized = text
        
        # Reemplazar cada tipo de PII
        for pii_type, pattern in self.PII_PATTERNS.items():
            if pii_type == 'email':
                sanitized = re.sub(pattern, '[EMAIL_REDACTED]', sanitized)
            elif pii_type == 'phone':
                sanitized = re.sub(pattern, '[PHONE_REDACTED]', sanitized)
            elif pii_type == 'rut':
                sanitized = re.sub(pattern, '[RUT_REDACTED]', sanitized)
            elif pii_type == 'credit_card':
                sanitized = re.sub(pattern, '[CC_REDACTED]', sanitized)
        
        return sanitized
    
    def check_content_safety(self, response: str) -> Tuple[bool, Optional[str]]:
        """Valida que la respuesta sea segura y apropiada.
        
        Args:
            response: Respuesta generada por el agente
            
        Returns:
            Tupla (es_seguro, advertencia)
            - es_seguro: True si la respuesta es apropiada
            - advertencia: Mensaje de advertencia si hay problemas
        """
        # Verificar que no esté vacía
        if not response or len(response.strip()) == 0:
            return False, "Respuesta vacía"
        
        # Verificar que no contenga PII sin sanitizar (check básico)
        for pii_type, pattern in self.PII_PATTERNS.items():
            if re.search(pattern, response):
                return False, f"Respuesta contiene {pii_type} sin sanitizar"
        
        return True, None


class RateLimiter:
    """Controlador de rate limiting por usuario.
    
    Implementa límite de máximo 20 requests por 60 segundos por usuario.
    """
    
    def __init__(self, max_requests: int = 20, window_seconds: int = 60):
        """Inicializa el rate limiter.
        
        Args:
            max_requests: Máximo número de requests permitidas
            window_seconds: Ventana de tiempo en segundos
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_times: Dict[str, List[float]] = defaultdict(list)
    
    def check_rate_limit(self, user_id: str) -> Tuple[bool, Optional[str]]:
        """Verifica si el usuario está dentro del rate limit.
        
        Args:
            user_id: Identificador del usuario
            
        Returns:
            Tupla (permitido, mensaje_error)
            - permitido: True si está dentro del límite, False si excedió
            - mensaje_error: Descripción del problema si excedió el límite
        """
        current_time = time.time()
        
        # Limpiar requests antiguas fuera de la ventana
        cutoff_time = current_time - self.window_seconds
        self.request_times[user_id] = [
            t for t in self.request_times[user_id] if t > cutoff_time
        ]
        
        # Verificar límite
        request_count = len(self.request_times[user_id])
        if request_count >= self.max_requests:
            return False, f"Rate limit excedido: {request_count}/{self.max_requests} requests en {self.window_seconds}s"
        
        # Registrar esta request
        self.request_times[user_id].append(current_time)
        
        return True, None
    
    def get_user_stats(self, user_id: str) -> Dict[str, any]:
        """Obtiene estadísticas de uso para un usuario.
        
        Args:
            user_id: Identificador del usuario
            
        Returns:
            Diccionario con estadísticas
        """
        current_time = time.time()
        cutoff_time = current_time - self.window_seconds
        
        # Limpiar requests antiguas
        self.request_times[user_id] = [
            t for t in self.request_times[user_id] if t > cutoff_time
        ]
        
        request_count = len(self.request_times[user_id])
        remaining = max(0, self.max_requests - request_count)
        
        return {
            'requests_in_window': request_count,
            'requests_remaining': remaining,
            'window_seconds': self.window_seconds,
            'max_requests': self.max_requests
        }


# Instancia global singleton
_rate_limiter: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    """Obtiene la instancia singleton del rate limiter.
    
    Returns:
        Instancia de RateLimiter
    """
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter
