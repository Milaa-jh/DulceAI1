"""Sistema de métricas para observabilidad del agente DulceAI.

Este módulo implementa la captura y análisis de métricas de desempeño,
incluyendo latencia, uso de herramientas, recursos del sistema y errores.
"""

import time
import json
import psutil
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from collections import defaultdict
import statistics


class MetricsCollector:
    """Colector de métricas para el agente de IA.
    
    Captura métricas de:
    - Precisión y consistencia (IE1)
    - Latencia y uso de recursos (IE2)
    - Errores y anomalías (IE3)
    """
    
    def __init__(self, metrics_file: str = "backend/logs/metrics.json"):
        """Inicializa el colector de métricas.
        
        Args:
            metrics_file: Ruta al archivo donde se guardarán las métricas
        """
        self.metrics_file = Path(metrics_file)
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Estado actual de la request
        self.current_trace_id: Optional[str] = None
        self.current_start_time: Optional[float] = None
        self.current_query: Optional[str] = None
        self.current_session_id: Optional[str] = None
        
        # Métricas acumuladas
        self.requests: List[Dict[str, Any]] = []
        self.tool_usage: Dict[str, int] = defaultdict(int)
        self.tool_latencies: Dict[str, List[float]] = defaultdict(list)
        self.tool_errors: Dict[str, int] = defaultdict(int)
        self.component_latencies: Dict[str, List[float]] = defaultdict(list)
        self.errors: List[Dict[str, Any]] = []
        self.cpu_samples: List[float] = []
        self.memory_samples: List[float] = []
        
        # Cargar métricas existentes si existen
        self._load_metrics()
    
    def _load_metrics(self) -> None:
        """Carga métricas existentes desde el archivo."""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.requests = data.get('requests', [])
                    self.tool_usage = defaultdict(int, data.get('tool_usage', {}))
                    self.tool_latencies = defaultdict(list, data.get('tool_latencies', {}))
                    self.tool_errors = defaultdict(int, data.get('tool_errors', {}))
                    self.component_latencies = defaultdict(list, data.get('component_latencies', {}))
                    self.errors = data.get('errors', [])
            except Exception as e:
                print(f"Error cargando métricas: {e}")
    
    def _save_metrics(self) -> None:
        """Guarda las métricas en el archivo JSON."""
        data = {
            'requests': self.requests,
            'tool_usage': dict(self.tool_usage),
            'tool_latencies': {k: list(v) for k, v in self.tool_latencies.items()},
            'tool_errors': dict(self.tool_errors),
            'component_latencies': {k: list(v) for k, v in self.component_latencies.items()},
            'errors': self.errors,
            'summary': self.get_summary_stats()
        }
        
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def start_request(self, trace_id: str, query: str, session_id: str) -> None:
        """Inicia el registro de una nueva request.
        
        Args:
            trace_id: ID único de trazabilidad
            query: Consulta del usuario
            session_id: ID de sesión del usuario
        """
        self.current_trace_id = trace_id
        self.current_start_time = time.time()
        self.current_query = query
        self.current_session_id = session_id
        
        # Capturar recursos al inicio
        self.cpu_samples.append(psutil.cpu_percent(interval=0.1))
        self.memory_samples.append(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024)
    
    def end_request(self, response: str, status: str) -> None:
        """Finaliza el registro de la request actual.
        
        Args:
            response: Respuesta generada por el agente
            status: Estado de la request ('success', 'error', etc.)
        """
        if self.current_start_time is None:
            return
        
        latency = time.time() - self.current_start_time
        
        request_data = {
            'trace_id': self.current_trace_id,
            'timestamp': datetime.now().isoformat(),
            'query': self.current_query,
            'session_id': self.current_session_id,
            'response_length': len(response),
            'latency': latency,
            'status': status,
            'cpu_percent': self.cpu_samples[-1] if self.cpu_samples else 0,
            'memory_mb': self.memory_samples[-1] if self.memory_samples else 0
        }
        
        self.requests.append(request_data)
        
        # Guardar después de cada request
        self._save_metrics()
        
        # Resetear estado actual
        self.current_trace_id = None
        self.current_start_time = None
        self.current_query = None
        self.current_session_id = None
    
    def track_tool(self, tool_name: str, latency: float, success: bool, 
                   input_data: Any, output_data: Any) -> None:
        """Registra el uso de una herramienta.
        
        Args:
            tool_name: Nombre de la herramienta ejecutada
            latency: Tiempo de ejecución en segundos
            success: Si la ejecución fue exitosa
            input_data: Datos de entrada a la herramienta
            output_data: Datos de salida de la herramienta
        """
        self.tool_usage[tool_name] += 1
        self.tool_latencies[tool_name].append(latency)
        
        if not success:
            self.tool_errors[tool_name] += 1
    
    def track_component(self, component_name: str, start_time: float, 
                        end_time: float, metadata: Optional[Dict] = None) -> None:
        """Registra la latencia de un componente específico.
        
        Args:
            component_name: Nombre del componente (agent, tools, RAG, memory)
            start_time: Tiempo de inicio (time.time())
            end_time: Tiempo de fin (time.time())
            metadata: Metadatos adicionales opcionales
        """
        latency = end_time - start_time
        self.component_latencies[component_name].append(latency)
    
    def track_error(self, component: str, error_type: str, message: str) -> None:
        """Registra un error del sistema.
        
        Args:
            component: Componente donde ocurrió el error
            error_type: Tipo de error
            message: Mensaje de error
        """
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'component': component,
            'error_type': error_type,
            'message': message,
            'trace_id': self.current_trace_id
        }
        self.errors.append(error_data)
        self._save_metrics()
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Calcula estadísticas resumidas de todas las métricas.
        
        Returns:
            Diccionario con estadísticas calculadas
        """
        total_requests = len(self.requests)
        
        if total_requests == 0:
            return {
                'total_requests': 0,
                'error_rate': 0.0,
                'avg_latency': 0.0,
                'p50_latency': 0.0,
                'p95_latency': 0.0,
                'p99_latency': 0.0,
                'min_latency': 0.0,
                'max_latency': 0.0,
                'tool_usage': {},
                'avg_cpu_percent': 0.0,
                'avg_memory_mb': 0.0
            }
        
        latencies = [r['latency'] for r in self.requests]
        error_count = sum(1 for r in self.requests if r['status'] == 'error')
        
        stats = {
            'total_requests': total_requests,
            'error_rate': error_count / total_requests if total_requests > 0 else 0.0,
            'avg_latency': statistics.mean(latencies) if latencies else 0.0,
            'p50_latency': statistics.median(latencies) if latencies else 0.0,
            'p95_latency': statistics.quantiles(latencies, n=20)[18] if len(latencies) > 20 else (max(latencies) if latencies else 0.0),
            'p99_latency': statistics.quantiles(latencies, n=100)[98] if len(latencies) > 100 else (max(latencies) if latencies else 0.0),
            'min_latency': min(latencies) if latencies else 0.0,
            'max_latency': max(latencies) if latencies else 0.0,
            'tool_usage': dict(self.tool_usage),
            'avg_cpu_percent': statistics.mean(self.cpu_samples) if self.cpu_samples else 0.0,
            'avg_memory_mb': statistics.mean(self.memory_samples) if self.memory_samples else 0.0
        }
        
        return stats


# Instancia global singleton
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """Obtiene la instancia singleton del colector de métricas.
    
    Returns:
        Instancia de MetricsCollector
    """
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector
