"""Dashboard de Observabilidad para DulceAI Agent.

Dashboard interactivo construido con Streamlit para monitorear métricas,
logs, errores y desempeño del agente de IA en tiempo real.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import sys

# Agregar path para imports
sys.path.append(str(Path(__file__).parent))

from src.monitoring.metrics import get_metrics_collector
from src.monitoring.logger import get_logger


# Configuración de la página
st.set_page_config(
    page_title="DulceAI - Dashboard de Observabilidad",
    page_icon="🍰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🍰 DulceAI - Dashboard de Observabilidad")
st.markdown("---")


def load_metrics():
    """Carga las métricas desde el archivo JSON."""
    metrics_file = Path("backend/logs/metrics.json")
    if not metrics_file.exists():
        return None
    
    try:
        with open(metrics_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error cargando métricas: {e}")
        return None


def load_logs():
    """Carga los logs desde el archivo."""
    log_file = Path("backend/logs/agent.log")
    if not log_file.exists():
        return []
    
    logs = []
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    logs.append(json.loads(line))
    except Exception as e:
        st.error(f"Error cargando logs: {e}")
    
    return logs


# Cargar datos
metrics_data = load_metrics()
logs_data = load_logs()


# ========================================
# SECCIÓN A: KPIs PRINCIPALES
# ========================================
st.header("📊 KPIs Principales")

if metrics_data and 'summary' in metrics_data:
    summary = metrics_data['summary']
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Requests",
            value=summary.get('total_requests', 0),
            delta=None
        )
    
    with col2:
        error_rate = summary.get('error_rate', 0) * 100
        st.metric(
            label="Tasa de Error",
            value=f"{error_rate:.1f}%",
            delta=f"{-error_rate:.1f}%" if error_rate < 5 else f"+{error_rate:.1f}%",
            delta_color="inverse"
        )
    
    with col3:
        avg_latency = summary.get('avg_latency', 0)
        st.metric(
            label="Latencia Promedio",
            value=f"{avg_latency:.2f}s",
            delta=None
        )
    
    with col4:
        p95_latency = summary.get('p95_latency', 0)
        st.metric(
            label="P95 Latencia",
            value=f"{p95_latency:.2f}s",
            delta=None
        )
    
    with col5:
        avg_cpu = summary.get('avg_cpu_percent', 0)
        st.metric(
            label="CPU Promedio",
            value=f"{avg_cpu:.1f}%",
            delta=None
        )
else:
    st.info("No hay datos de métricas disponibles. Ejecuta el agente para generar métricas.")

st.markdown("---")


# ========================================
# SECCIÓN B: ANÁLISIS DE LATENCIA
# ========================================
st.header("⏱️ Análisis de Latencia")

if metrics_data and 'requests' in metrics_data and len(metrics_data['requests']) > 0:
    requests_df = pd.DataFrame(metrics_data['requests'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histograma de latencias
        st.subheader("Distribución de Latencias")
        fig_hist = px.histogram(
            requests_df,
            x='latency',
            nbins=20,
            title="Histograma de Latencias",
            labels={'latency': 'Latencia (s)', 'count': 'Frecuencia'}
        )
        fig_hist.update_layout(showlegend=False)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Percentiles
        st.subheader("Percentiles de Latencia")
        
        latencies = requests_df['latency'].tolist()
        percentiles = {
            'P50': requests_df['latency'].median(),
            'P75': requests_df['latency'].quantile(0.75),
            'P90': requests_df['latency'].quantile(0.90),
            'P95': requests_df['latency'].quantile(0.95),
            'P99': requests_df['latency'].quantile(0.99) if len(latencies) > 100 else requests_df['latency'].max()
        }
        
        fig_percentiles = go.Figure(data=[
            go.Bar(
                x=list(percentiles.keys()),
                y=list(percentiles.values()),
                text=[f"{v:.2f}s" for v in percentiles.values()],
                textposition='auto',
            )
        ])
        fig_percentiles.update_layout(
            title="Percentiles de Latencia",
            xaxis_title="Percentil",
            yaxis_title="Latencia (s)",
            showlegend=False
        )
        st.plotly_chart(fig_percentiles, use_container_width=True)

else:
    st.info("No hay datos de requests disponibles.")

st.markdown("---")


# ========================================
# SECCIÓN C: USO DE HERRAMIENTAS
# ========================================
st.header("🛠️ Uso de Herramientas")

if metrics_data and 'tool_usage' in metrics_data and metrics_data['tool_usage']:
    tool_usage = metrics_data['tool_usage']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart de uso de herramientas
        st.subheader("Distribución de Uso de Herramientas")
        fig_pie = px.pie(
            names=list(tool_usage.keys()),
            values=list(tool_usage.values()),
            title="Uso de Herramientas"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Tabla de estadísticas de herramientas
        st.subheader("Estadísticas por Herramienta")
        
        tool_stats = []
        tool_latencies = metrics_data.get('tool_latencies', {})
        tool_errors = metrics_data.get('tool_errors', {})
        
        for tool, count in tool_usage.items():
            latencies = tool_latencies.get(tool, [])
            errors = tool_errors.get(tool, 0)
            
            tool_stats.append({
                'Herramienta': tool,
                'Usos': count,
                'Errores': errors,
                'Latencia Prom': f"{sum(latencies)/len(latencies):.2f}s" if latencies else "N/A"
            })
        
        st.dataframe(pd.DataFrame(tool_stats), use_container_width=True)

else:
    st.info("No hay datos de uso de herramientas disponibles.")

st.markdown("---")


# ========================================
# SECCIÓN D: USO DE RECURSOS
# ========================================
st.header("💻 Uso de Recursos")

if metrics_data and 'summary' in metrics_data:
    summary = metrics_data['summary']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gauge de CPU
        st.subheader("CPU")
        avg_cpu = summary.get('avg_cpu_percent', 0)
        
        fig_cpu = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_cpu,
            title={'text': "CPU Promedio (%)"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgreen"},
                    {'range': [50, 75], 'color': "yellow"},
                    {'range': [75, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        st.plotly_chart(fig_cpu, use_container_width=True)
    
    with col2:
        # Gauge de Memoria
        st.subheader("Memoria")
        avg_memory = summary.get('avg_memory_mb', 0)
        
        fig_memory = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_memory,
            title={'text': "Memoria Promedio (MB)"},
            gauge={
                'axis': {'range': [0, 1000]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 300], 'color': "lightgreen"},
                    {'range': [300, 600], 'color': "yellow"},
                    {'range': [600, 1000], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 800
                }
            }
        ))
        st.plotly_chart(fig_memory, use_container_width=True)

else:
    st.info("No hay datos de uso de recursos disponibles.")

st.markdown("---")


# ========================================
# SECCIÓN E: ERRORES Y ANOMALÍAS
# ========================================
st.header("⚠️ Errores y Anomalías")

col1, col2 = st.columns(2)

with col1:
    # Tabla de errores recientes
    st.subheader("Errores Recientes")
    
    if metrics_data and 'errors' in metrics_data and metrics_data['errors']:
        errors_df = pd.DataFrame(metrics_data['errors'])
        errors_df = errors_df.tail(10)  # Últimos 10 errores
        st.dataframe(errors_df, use_container_width=True)
    else:
        st.success("✅ No se han registrado errores")

with col2:
    # Anomalías de latencia
    st.subheader("Anomalías de Latencia")
    
    if metrics_data and 'requests' in metrics_data and len(metrics_data['requests']) > 0:
        requests_df = pd.DataFrame(metrics_data['requests'])
        
        # Detectar anomalías (latencias > P95)
        p95 = requests_df['latency'].quantile(0.95)
        anomalies = requests_df[requests_df['latency'] > p95]
        
        if len(anomalies) > 0:
            st.warning(f"🔴 {len(anomalies)} requests con latencia anómala (> P95: {p95:.2f}s)")
            st.dataframe(
                anomalies[['trace_id', 'latency', 'status']].tail(5),
                use_container_width=True
            )
        else:
            st.success("✅ No se detectaron anomalías de latencia")
    else:
        st.info("No hay suficientes datos para detectar anomalías")

st.markdown("---")


# ========================================
# SECCIÓN F: LOGS Y TRAZABILIDAD
# ========================================
st.header("📋 Logs y Trazabilidad")

if logs_data:
    st.subheader(f"Últimas {min(10, len(logs_data))} Requests")
    
    # Agrupar logs por trace_id
    logs_by_trace = {}
    for log in reversed(logs_data[-100:]):  # Últimos 100 logs
        trace_id = log.get('trace_id')
        if trace_id:
            if trace_id not in logs_by_trace:
                logs_by_trace[trace_id] = []
            logs_by_trace[trace_id].append(log)
    
    # Mostrar últimos 10 traces
    for i, (trace_id, trace_logs) in enumerate(list(logs_by_trace.items())[:10]):
        # Buscar request_start para obtener query
        query = "N/A"
        timestamp = "N/A"
        
        for log in trace_logs:
            if log.get('event') == 'request_start':
                query = log.get('data', {}).get('query', 'N/A')
                timestamp = log.get('timestamp', 'N/A')
                break
        
        with st.expander(f"🔍 Request {i+1} - {trace_id} - {timestamp[:19]}"):
            st.markdown(f"**Query:** {query}")
            st.markdown(f"**Trace ID:** `{trace_id}`")
            st.markdown(f"**Número de eventos:** {len(trace_logs)}")
            
            # Tabla de logs del trace
            trace_df = pd.DataFrame(trace_logs)
            st.dataframe(trace_df[['timestamp', 'level', 'event']], use_container_width=True)
            
            # Detalles expandibles
            with st.expander("Ver detalles completos"):
                for log in trace_logs:
                    st.json(log)

else:
    st.info("No hay logs disponibles. Ejecuta el agente para generar logs.")


# Footer
st.markdown("---")
st.caption("DulceAI Dashboard de Observabilidad | Actualizado en tiempo real")
