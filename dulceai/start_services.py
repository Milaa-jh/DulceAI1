"""
Script para iniciar Backend y Frontend simultáneamente
Con logs detallados para debugging
"""

import subprocess
import sys
import os
import time
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('services.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def get_project_root():
    """Obtener ruta raíz del proyecto"""
    return Path(__file__).parent.absolute()

def check_ports():
    """Verificar si los puertos están disponibles"""
    import socket
    
    ports = [8000, 3000]
    available = []
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result != 0:
            available.append(port)
            logger.info(f"✅ Puerto {port} disponible")
        else:
            logger.warning(f"⚠️ Puerto {port} está en uso")
    
    return available

def start_backend():
    """Iniciar servidor backend con uvicorn"""
    project_root = get_project_root()
    venv_python = project_root / "venv" / "Scripts" / "python.exe"
    backend_dir = project_root / "dulceai" / "backend"
    
    if not venv_python.exists():
        logger.error(f"❌ No se encuentra venv: {venv_python}")
        logger.error(f"   Ruta buscada: {venv_python.absolute()}")
        return None
    
    if not backend_dir.exists():
        logger.error(f"❌ No se encuentra directorio backend: {backend_dir}")
        return None
    
    logger.info("🚀 Iniciando Backend FastAPI con UVICORN...")
    logger.info(f"   Directorio de trabajo: {backend_dir.absolute()}")
    logger.info(f"   Python: {venv_python.absolute()}")
    logger.info(f"   Comando: uvicorn app:app --host 0.0.0.0 --port 8000")
    logger.info(f"   Puerto: 8000")
    
    try:
        # Usar uvicorn con módulo Python
        cmd = [str(venv_python), "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
        logger.info(f"   Comando completo: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd,
            cwd=str(backend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
        )
        
        logger.info(f"✅ Backend iniciado con UVICORN (PID: {process.pid})")
        return process
    except Exception as e:
        logger.error(f"❌ Error iniciando backend: {e}")
        import traceback
        logger.error(f"   Traceback: {traceback.format_exc()}")
        return None

def start_frontend():
    """Iniciar servidor frontend con http.server"""
    project_root = get_project_root()
    frontend_dir = project_root / "dulceai" / "frontend"
    
    if not frontend_dir.exists():
        logger.error(f"❌ No se encuentra directorio frontend: {frontend_dir}")
        logger.error(f"   Ruta buscada: {frontend_dir.absolute()}")
        return None
    
    logger.info("🚀 Iniciando Frontend HTTP Server...")
    logger.info(f"   Directorio: {frontend_dir.absolute()}")
    logger.info(f"   Comando: python -m http.server 3000")
    logger.info(f"   Puerto: 3000")
    
    try:
        cmd = [sys.executable, "-m", "http.server", "3000"]
        logger.info(f"   Comando completo: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd,
            cwd=str(frontend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
        )
        
        logger.info(f"✅ Frontend iniciado (PID: {process.pid})")
        return process
    except Exception as e:
        logger.error(f"❌ Error iniciando frontend: {e}")
        import traceback
        logger.error(f"   Traceback: {traceback.format_exc()}")
        return None

def monitor_processes(backend_proc, frontend_proc):
    """Monitorear procesos y mostrar logs"""
    logger.info("=" * 60)
    logger.info("📊 Monitoreando servicios...")
    logger.info("=" * 60)
    logger.info("🔗 URLs:")
    logger.info("   Backend (UVICORN):  http://localhost:8000")
    logger.info("   Frontend:           http://localhost:3000")
    logger.info("   API Docs:           http://localhost:8000/docs")
    logger.info("   Health Check:        http://localhost:8000/health")
    logger.info("   AI Status:          http://localhost:8000/api/ai/status")
    logger.info("=" * 60)
    logger.info("💡 Presiona Ctrl+C para detener todos los servicios")
    logger.info("=" * 60)
    
    backend_buffer = []
    frontend_buffer = []
    
    try:
        # Monitorear ambos procesos
        while True:
            # Verificar estado backend
            if backend_proc and backend_proc.poll() is not None:
                logger.error("❌ Backend (UVICORN) se detuvo inesperadamente")
                if backend_proc.stdout:
                    try:
                        remaining = backend_proc.stdout.read()
                        if remaining:
                            logger.error(f"Backend output: {remaining}")
                    except:
                        pass
                break
            
            # Verificar estado frontend
            if frontend_proc and frontend_proc.poll() is not None:
                logger.error("❌ Frontend se detuvo inesperadamente")
                if frontend_proc.stdout:
                    try:
                        remaining = frontend_proc.stdout.read()
                        if remaining:
                            logger.error(f"Frontend output: {remaining}")
                    except:
                        pass
                break
            
            # Leer logs de backend (UVICORN)
            if backend_proc and backend_proc.stdout:
                try:
                    import select
                    import sys
                    # En Windows, usar threading para leer buffers
                    import threading
                    
                    # Leer línea por línea
                    line = backend_proc.stdout.readline()
                    if line:
                        line_clean = line.strip()
                        if line_clean:
                            logger.info(f"[BACKEND-UVICORN] {line_clean}")
                            backend_buffer.append(line_clean)
                            # Mostrar errores críticos inmediatamente
                            if "ERROR" in line_clean or "CRITICAL" in line_clean:
                                logger.error(f"⚠️ {line_clean}")
                except Exception as e:
                    # Silenciar errores de lectura
                    pass
            
            # Leer logs de frontend
            if frontend_proc and frontend_proc.stdout:
                try:
                    line = frontend_proc.stdout.readline()
                    if line:
                        line_clean = line.strip()
                        if line_clean:
                            logger.info(f"[FRONTEND] {line_clean}")
                            frontend_buffer.append(line_clean)
                except Exception as e:
                    # Silenciar errores de lectura
                    pass
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        logger.info("\n🛑 Deteniendo servicios...")
        
        if backend_proc:
            logger.info("   Deteniendo Backend...")
            backend_proc.terminate()
            try:
                backend_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend_proc.kill()
        
        if frontend_proc:
            logger.info("   Deteniendo Frontend...")
            frontend_proc.terminate()
            try:
                frontend_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                frontend_proc.kill()
        
        logger.info("✅ Todos los servicios detenidos")

def main():
    """Función principal"""
    logger.info("=" * 60)
    logger.info("🍰 DulceAI - Iniciando Servicios")
    logger.info("=" * 60)
    
    # Verificar puertos
    logger.info("🔍 Verificando puertos...")
    available_ports = check_ports()
    
    if 8000 not in available_ports:
        logger.error("❌ Puerto 8000 (Backend) no está disponible")
        logger.error("   Detén cualquier proceso que esté usando el puerto 8000")
        return
    
    if 3000 not in available_ports:
        logger.error("❌ Puerto 3000 (Frontend) no está disponible")
        logger.error("   Detén cualquier proceso que esté usando el puerto 3000")
        return
    
    # Iniciar servicios
    backend_proc = start_backend()
    time.sleep(2)  # Esperar un poco antes de iniciar frontend
    
    frontend_proc = start_frontend()
    time.sleep(2)  # Esperar a que ambos servicios inicien
    
    # Verificar que ambos estén corriendo
    if backend_proc and backend_proc.poll() is None:
        logger.info("✅ Backend está corriendo")
    else:
        logger.error("❌ Backend no está corriendo")
        if backend_proc:
            output = backend_proc.stdout.read() if backend_proc.stdout else ""
            logger.error(f"Backend error: {output}")
    
    if frontend_proc and frontend_proc.poll() is None:
        logger.info("✅ Frontend está corriendo")
    else:
        logger.error("❌ Frontend no está corriendo")
        if frontend_proc:
            output = frontend_proc.stdout.read() if frontend_proc.stdout else ""
            logger.error(f"Frontend error: {output}")
    
    # Monitorear procesos
    if backend_proc and frontend_proc:
        monitor_processes(backend_proc, frontend_proc)
    else:
        logger.error("❌ No se pudieron iniciar todos los servicios")
        if backend_proc:
            backend_proc.terminate()
        if frontend_proc:
            frontend_proc.terminate()

if __name__ == "__main__":
    main()

