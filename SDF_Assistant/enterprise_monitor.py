#!/usr/bin/env python3
"""
SDF Assistant - Enterprise Monitoring System
Sistema de monitoreo y logging para entornos empresariales
"""

import os
import json
import logging
import time
import psutil
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import threading
import queue

@dataclass
class SystemMetrics:
    """Métricas del sistema"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    disk_usage_percent: float
    ollama_status: bool
    model_response_time: float
    active_connections: int
    documents_processed: int
    queries_per_minute: float

@dataclass
class PerformanceMetrics:
    """Métricas de rendimiento"""
    timestamp: str
    query_id: str
    response_time: float
    documents_used: int
    context_length: int
    confidence_score: float
    success: bool
    error_message: Optional[str] = None

class EnterpriseLogger:
    """Sistema de logging enterprise"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configurar logging
        self._setup_logging()
        
        # Cola de eventos para logging asíncrono
        self.log_queue = queue.Queue()
        self.log_thread = threading.Thread(target=self._log_worker, daemon=True)
        self.log_thread.start()
    
    def _setup_logging(self):
        """Configurar sistema de logging"""
        # Log principal
        main_handler = logging.FileHandler(self.log_dir / "sdf_main.log")
        main_handler.setLevel(logging.INFO)
        main_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        main_handler.setFormatter(main_formatter)
        
        # Log de errores
        error_handler = logging.FileHandler(self.log_dir / "sdf_errors.log")
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(main_formatter)
        
        # Log de performance
        perf_handler = logging.FileHandler(self.log_dir / "sdf_performance.log")
        perf_handler.setLevel(logging.INFO)
        perf_formatter = logging.Formatter(
            '%(asctime)s - %(message)s'
        )
        perf_handler.setFormatter(perf_formatter)
        
        # Configurar logger principal
        self.logger = logging.getLogger("SDF_Enterprise")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(main_handler)
        self.logger.addHandler(error_handler)
        
        # Logger de performance
        self.perf_logger = logging.getLogger("SDF_Performance")
        self.perf_logger.setLevel(logging.INFO)
        self.perf_logger.addHandler(perf_handler)
    
    def _log_worker(self):
        """Worker para logging asíncrono"""
        while True:
            try:
                log_entry = self.log_queue.get(timeout=1)
                if log_entry is None:  # Señal de parada
                    break
                
                log_type = log_entry.get("type", "info")
                message = log_entry.get("message", "")
                data = log_entry.get("data", {})
                
                if log_type == "performance":
                    self.perf_logger.info(f"{message} | {json.dumps(data)}")
                elif log_type == "error":
                    self.logger.error(f"{message} | {json.dumps(data)}")
                else:
                    self.logger.info(f"{message} | {json.dumps(data)}")
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error en log worker: {e}")
    
    def log_event(self, event_type: str, message: str, data: Dict = None):
        """Log de eventos de manera asíncrona"""
        self.log_queue.put({
            "type": event_type,
            "message": message,
            "data": data or {}
        })
    
    def log_performance(self, metrics: PerformanceMetrics):
        """Log de métricas de rendimiento"""
        self.log_event("performance", "Performance Metrics", asdict(metrics))
    
    def log_error(self, error: str, context: Dict = None):
        """Log de errores"""
        self.log_event("error", f"Error: {error}", context or {})
    
    def log_system_metrics(self, metrics: SystemMetrics):
        """Log de métricas del sistema"""
        self.log_event("system", "System Metrics", asdict(metrics))

class SystemMonitor:
    """Monitor del sistema"""
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.metrics_history = []
        self.max_history = 1000  # Mantener último día de métricas
    
    def get_system_metrics(self) -> SystemMetrics:
        """Obtener métricas actuales del sistema"""
        try:
            # Métricas del sistema
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Estado de Ollama
            ollama_status = self._check_ollama_status()
            
            # Métricas de red
            connections = len(psutil.net_connections())
            
            return SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                disk_usage_percent=disk.percent,
                ollama_status=ollama_status,
                model_response_time=0.0,  # Se actualiza desde el asistente
                active_connections=connections,
                documents_processed=0,  # Se actualiza desde el asistente
                queries_per_minute=0.0  # Se calcula desde el historial
            )
        except Exception as e:
            # Retornar métricas básicas en caso de error
            return SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=0.0,
                memory_percent=0.0,
                disk_usage_percent=0.0,
                ollama_status=False,
                model_response_time=0.0,
                active_connections=0,
                documents_processed=0,
                queries_per_minute=0.0
            )
    
    def _check_ollama_status(self) -> bool:
        """Verificar estado de Ollama"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def add_metrics(self, metrics: SystemMetrics):
        """Agregar métricas al historial"""
        self.metrics_history.append(metrics)
        
        # Limpiar historial antiguo
        cutoff_time = datetime.now() - timedelta(days=1)
        self.metrics_history = [
            m for m in self.metrics_history 
            if datetime.fromisoformat(m.timestamp) > cutoff_time
        ]
        
        # Limitar tamaño del historial
        if len(self.metrics_history) > self.max_history:
            self.metrics_history = self.metrics_history[-self.max_history:]
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Obtener resumen de rendimiento"""
        if not self.metrics_history:
            return {"error": "No hay métricas disponibles"}
        
        recent_metrics = self.metrics_history[-100:]  # Últimas 100 métricas
        
        return {
            "avg_cpu": sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics),
            "avg_memory": sum(m.memory_percent for m in recent_metrics) / len(recent_metrics),
            "avg_disk": sum(m.disk_usage_percent for m in recent_metrics) / len(recent_metrics),
            "ollama_uptime": sum(1 for m in recent_metrics if m.ollama_status) / len(recent_metrics),
            "total_metrics": len(self.metrics_history),
            "time_range": {
                "start": self.metrics_history[0].timestamp,
                "end": self.metrics_history[-1].timestamp
            }
        }

class PerformanceTracker:
    """Tracker de rendimiento"""
    
    def __init__(self):
        self.performance_history = []
        self.max_history = 1000
    
    def add_performance_metrics(self, metrics: PerformanceMetrics):
        """Agregar métricas de rendimiento"""
        self.performance_history.append(metrics)
        
        # Limpiar historial antiguo
        cutoff_time = datetime.now() - timedelta(days=1)
        self.performance_history = [
            m for m in self.performance_history 
            if datetime.fromisoformat(m.timestamp) > cutoff_time
        ]
        
        # Limitar tamaño del historial
        if len(self.performance_history) > self.max_history:
            self.performance_history = self.performance_history[-self.max_history:]
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de rendimiento"""
        if not self.performance_history:
            return {"error": "No hay métricas de rendimiento disponibles"}
        
        recent_performance = self.performance_history[-100:]
        
        response_times = [p.response_time for p in recent_performance]
        success_rate = sum(1 for p in recent_performance if p.success) / len(recent_performance)
        avg_confidence = sum(p.confidence_score for p in recent_performance) / len(recent_performance)
        
        return {
            "avg_response_time": sum(response_times) / len(response_times),
            "min_response_time": min(response_times),
            "max_response_time": max(response_times),
            "success_rate": success_rate,
            "avg_confidence": avg_confidence,
            "total_queries": len(self.performance_history),
            "recent_queries": len(recent_performance)
        }
    
    def get_error_analysis(self) -> Dict[str, Any]:
        """Análisis de errores"""
        errors = [p for p in self.performance_history if not p.success]
        
        if not errors:
            return {"error_count": 0, "common_errors": []}
        
        error_messages = [e.error_message for e in errors if e.error_message]
        error_counts = {}
        
        for error in error_messages:
            error_counts[error] = error_counts.get(error, 0) + 1
        
        return {
            "error_count": len(errors),
            "error_rate": len(errors) / len(self.performance_history),
            "common_errors": sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }

class EnterpriseMonitor:
    """Monitor enterprise principal"""
    
    def __init__(self, log_dir: str = "logs", ollama_url: str = "http://localhost:11434"):
        self.logger = EnterpriseLogger(log_dir)
        self.system_monitor = SystemMonitor(ollama_url)
        self.performance_tracker = PerformanceTracker()
        self.monitoring_active = False
        self.monitor_thread = None
    
    def start_monitoring(self, interval: int = 30):
        """Iniciar monitoreo continuo"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop, 
            args=(interval,), 
            daemon=True
        )
        self.monitor_thread.start()
        self.logger.log_event("system", "Enterprise monitoring started")
    
    def stop_monitoring(self):
        """Detener monitoreo"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.log_event("system", "Enterprise monitoring stopped")
    
    def _monitoring_loop(self, interval: int):
        """Loop de monitoreo"""
        while self.monitoring_active:
            try:
                # Obtener métricas del sistema
                metrics = self.system_monitor.get_system_metrics()
                self.system_monitor.add_metrics(metrics)
                
                # Log de métricas
                self.logger.log_system_metrics(metrics)
                
                # Verificar alertas
                self._check_alerts(metrics)
                
                time.sleep(interval)
                
            except Exception as e:
                self.logger.log_error(f"Error en monitoring loop: {e}")
                time.sleep(interval)
    
    def _check_alerts(self, metrics: SystemMetrics):
        """Verificar alertas del sistema"""
        alerts = []
        
        if metrics.cpu_percent > 80:
            alerts.append(f"CPU usage high: {metrics.cpu_percent}%")
        
        if metrics.memory_percent > 85:
            alerts.append(f"Memory usage high: {metrics.memory_percent}%")
        
        if metrics.disk_usage_percent > 90:
            alerts.append(f"Disk usage high: {metrics.disk_usage_percent}%")
        
        if not metrics.ollama_status:
            alerts.append("Ollama service is down")
        
        for alert in alerts:
            self.logger.log_event("alert", alert, {"metrics": asdict(metrics)})
    
    def track_query_performance(self, query_id: str, response_time: float, 
                               documents_used: int, context_length: int, 
                               confidence_score: float, success: bool, 
                               error_message: str = None):
        """Trackear rendimiento de una consulta"""
        metrics = PerformanceMetrics(
            timestamp=datetime.now().isoformat(),
            query_id=query_id,
            response_time=response_time,
            documents_used=documents_used,
            context_length=context_length,
            confidence_score=confidence_score,
            success=success,
            error_message=error_message
        )
        
        self.performance_tracker.add_performance_metrics(metrics)
        self.logger.log_performance(metrics)
    
    def get_system_health_report(self) -> Dict[str, Any]:
        """Obtener reporte de salud del sistema"""
        current_metrics = self.system_monitor.get_system_metrics()
        performance_stats = self.performance_tracker.get_performance_stats()
        error_analysis = self.performance_tracker.get_error_analysis()
        system_summary = self.system_monitor.get_performance_summary()
        
        # Calcular estado general
        health_score = 100
        
        if current_metrics.cpu_percent > 80:
            health_score -= 20
        if current_metrics.memory_percent > 85:
            health_score -= 20
        if current_metrics.disk_usage_percent > 90:
            health_score -= 15
        if not current_metrics.ollama_status:
            health_score -= 25
        if performance_stats.get("success_rate", 1.0) < 0.9:
            health_score -= 10
        
        health_status = "Excellent" if health_score >= 90 else \
                       "Good" if health_score >= 70 else \
                       "Fair" if health_score >= 50 else "Poor"
        
        return {
            "timestamp": datetime.now().isoformat(),
            "health_score": max(0, health_score),
            "health_status": health_status,
            "current_metrics": asdict(current_metrics),
            "performance_stats": performance_stats,
            "error_analysis": error_analysis,
            "system_summary": system_summary,
            "recommendations": self._generate_recommendations(
                current_metrics, performance_stats, error_analysis
            )
        }
    
    def _generate_recommendations(self, metrics: SystemMetrics, 
                                 performance_stats: Dict, 
                                 error_analysis: Dict) -> List[str]:
        """Generar recomendaciones basadas en métricas"""
        recommendations = []
        
        if metrics.cpu_percent > 80:
            recommendations.append("Consider upgrading CPU or optimizing workload")
        
        if metrics.memory_percent > 85:
            recommendations.append("Increase system memory or optimize memory usage")
        
        if metrics.disk_usage_percent > 90:
            recommendations.append("Clean up disk space or expand storage")
        
        if not metrics.ollama_status:
            recommendations.append("Restart Ollama service immediately")
        
        if performance_stats.get("success_rate", 1.0) < 0.9:
            recommendations.append("Investigate query failures and improve error handling")
        
        if performance_stats.get("avg_response_time", 0) > 30:
            recommendations.append("Optimize model performance or reduce context size")
        
        if not recommendations:
            recommendations.append("System is performing optimally")
        
        return recommendations
    
    def export_monitoring_data(self, format: str = "json") -> str:
        """Exportar datos de monitoreo"""
        data = {
            "system_metrics": [asdict(m) for m in self.system_monitor.metrics_history],
            "performance_metrics": [asdict(m) for m in self.performance_tracker.performance_history],
            "health_report": self.get_system_health_report(),
            "export_timestamp": datetime.now().isoformat()
        }
        
        if format == "json":
            return json.dumps(data, indent=2)
        else:
            raise ValueError("Formato no soportado. Use 'json'")

# Instancia global del monitor
enterprise_monitor = EnterpriseMonitor()
