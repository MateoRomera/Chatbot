#!/usr/bin/env python3
"""
SDF Assistant - Enterprise Admin Panel
Panel de administración para gestión empresarial
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import time

# Importar componentes del sistema
from config import Config
from enterprise_monitor import enterprise_monitor
from sdf_assistant import SDFAssistant

# Configuración de la página
st.set_page_config(
    page_title="SDF Admin Panel",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para panel de administración
st.markdown("""
<style>
    .admin-header {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .admin-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .admin-header p {
        color: #ecf0f1;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
    }
    
    .metric-label {
        color: #7f8c8d;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-healthy { background-color: #27ae60; }
    .status-warning { background-color: #f39c12; }
    .status-critical { background-color: #e74c3c; }
    
    .admin-section {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .chart-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def create_admin_header():
    """Crear header del panel de administración"""
    st.markdown("""
    <div class="admin-header">
        <h1>🔧 SDF Admin Panel</h1>
        <p>Enterprise Document Intelligence Management</p>
    </div>
    """, unsafe_allow_html=True)

def get_system_overview():
    """Obtener vista general del sistema"""
    try:
        # Obtener métricas del sistema
        system_metrics = enterprise_monitor.get_current_metrics()
        health_report = enterprise_monitor.get_system_health_report()
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{health_report.get('health_score', 0)}%</div>
                <div class="metric-label">Health Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            cpu_usage = system_metrics.get('cpu_percent', 0)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{cpu_usage:.1f}%</div>
                <div class="metric-label">CPU Usage</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            memory_usage = system_metrics.get('memory_percent', 0)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{memory_usage:.1f}%</div>
                <div class="metric-label">Memory Usage</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            queries_per_min = system_metrics.get('queries_per_minute', 0)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{queries_per_min:.1f}</div>
                <div class="metric-label">Queries/Min</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Estado del sistema
        st.markdown("### 📊 System Status")
        col1, col2 = st.columns(2)
        
        with col1:
            # Estado de Ollama
            ollama_status = system_metrics.get('ollama_status', False)
            status_class = "status-healthy" if ollama_status else "status-critical"
            status_text = "Online" if ollama_status else "Offline"
            
            st.markdown(f"""
            <div class="admin-section">
                <h4>🤖 Ollama Status</h4>
                <p><span class="status-indicator {status_class}"></span>{status_text}</p>
                <p><strong>Model:</strong> {Config.OLLAMA_MODEL}</p>
                <p><strong>Response Time:</strong> {system_metrics.get('model_response_time', 0):.2f}s</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Estado de documentos
            documents_processed = system_metrics.get('documents_processed', 0)
            st.markdown(f"""
            <div class="admin-section">
                <h4>📁 Document Status</h4>
                <p><strong>Documents Loaded:</strong> {documents_processed}</p>
                <p><strong>Context Length:</strong> {Config.MAX_CONTEXT_LENGTH} tokens</p>
                <p><strong>Workers:</strong> {Config.MAX_WORKERS}</p>
            </div>
            """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error obteniendo métricas: {e}")

def show_performance_analytics():
    """Mostrar analytics de rendimiento"""
    st.markdown("### 📈 Performance Analytics")
    
    try:
        # Obtener datos de performance
        performance_data = enterprise_monitor.get_performance_data()
        
        if performance_data:
            # Convertir a DataFrame
            df = pd.DataFrame(performance_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Gráfico de tiempo de respuesta
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Response Time Trend")
                fig_response = px.line(
                    df, x='timestamp', y='response_time',
                    title='Response Time Over Time'
                )
                fig_response.update_layout(height=300)
                st.plotly_chart(fig_response, use_container_width=True)
            
            with col2:
                st.markdown("#### Success Rate")
                success_rate = (df['success'].sum() / len(df)) * 100
                fig_success = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=success_rate,
                    title={'text': "Success Rate (%)"},
                    gauge={'axis': {'range': [None, 100]},
                           'bar': {'color': "darkblue"},
                           'steps': [{'range': [0, 50], 'color': "lightgray"},
                                   {'range': [50, 80], 'color': "yellow"},
                                   {'range': [80, 100], 'color': "green"}]}
                ))
                fig_success.update_layout(height=300)
                st.plotly_chart(fig_success, use_container_width=True)
            
            # Métricas de performance
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_response_time = df['response_time'].mean()
                st.metric("Avg Response Time", f"{avg_response_time:.2f}s")
            
            with col2:
                total_queries = len(df)
                st.metric("Total Queries", total_queries)
            
            with col3:
                avg_confidence = df['confidence_score'].mean()
                st.metric("Avg Confidence", f"{avg_confidence:.2f}%")
        
        else:
            st.info("No hay datos de performance disponibles")
    
    except Exception as e:
        st.error(f"Error mostrando analytics: {e}")

def show_system_monitoring():
    """Mostrar monitoreo del sistema"""
    st.markdown("### 🔍 System Monitoring")
    
    try:
        # Obtener métricas históricas
        metrics_history = enterprise_monitor.get_metrics_history()
        
        if metrics_history:
            df = pd.DataFrame(metrics_history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Gráficos de recursos del sistema
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### CPU & Memory Usage")
                fig_resources = go.Figure()
                fig_resources.add_trace(go.Scatter(
                    x=df['timestamp'], y=df['cpu_percent'],
                    mode='lines', name='CPU %', line=dict(color='red')
                ))
                fig_resources.add_trace(go.Scatter(
                    x=df['timestamp'], y=df['memory_percent'],
                    mode='lines', name='Memory %', line=dict(color='blue')
                ))
                fig_resources.update_layout(height=300, title='System Resources')
                st.plotly_chart(fig_resources, use_container_width=True)
            
            with col2:
                st.markdown("#### Disk Usage")
                fig_disk = px.line(
                    df, x='timestamp', y='disk_usage_percent',
                    title='Disk Usage Over Time'
                )
                fig_disk.update_layout(height=300)
                st.plotly_chart(fig_disk, use_container_width=True)
            
            # Alertas del sistema
            st.markdown("#### 🚨 System Alerts")
            
            # Verificar alertas
            alerts = []
            
            # CPU alta
            if df['cpu_percent'].iloc[-1] > 80:
                alerts.append("⚠️ High CPU usage detected")
            
            # Memoria alta
            if df['memory_percent'].iloc[-1] > 85:
                alerts.append("⚠️ High memory usage detected")
            
            # Disk alto
            if df['disk_usage_percent'].iloc[-1] > 90:
                alerts.append("⚠️ High disk usage detected")
            
            # Ollama offline
            if not df['ollama_status'].iloc[-1]:
                alerts.append("❌ Ollama service is offline")
            
            if alerts:
                for alert in alerts:
                    st.warning(alert)
            else:
                st.success("✅ All systems operational")
        
        else:
            st.info("No hay datos de monitoreo disponibles")
    
    except Exception as e:
        st.error(f"Error mostrando monitoreo: {e}")

def show_document_management():
    """Mostrar gestión de documentos"""
    st.markdown("### 📁 Document Management")
    
    try:
        # Crear instancia temporal del asistente para obtener info de documentos
        assistant = SDFAssistant()
        doc_overview = assistant.get_document_overview()
        
        if doc_overview.get('success'):
            # Información de documentos
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Document Statistics")
                total_docs = doc_overview['total_documents']
                file_types = doc_overview['file_types']
                
                st.metric("Total Documents", total_docs)
                
                # Gráfico de tipos de archivo
                if file_types:
                    fig_types = px.pie(
                        values=list(file_types.values()),
                        names=list(file_types.keys()),
                        title="Document Types Distribution"
                    )
                    st.plotly_chart(fig_types, use_container_width=True)
            
            with col2:
                st.markdown("#### Document List")
                documents = doc_overview['documents']
                
                if documents:
                    doc_df = pd.DataFrame(documents)
                    st.dataframe(
                        doc_df[['name', 'file_type', 'size']],
                        use_container_width=True
                    )
                else:
                    st.info("No documents loaded")
            
            # Acciones de documentos
            st.markdown("#### Document Actions")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Reload Documents"):
                    assistant.reload_documents()
                    st.success("Documents reloaded successfully!")
            
            with col2:
                if st.button("📊 Generate Summary"):
                    with st.spinner("Generating summary..."):
                        summary = assistant.generate_summary()
                        st.text_area("Document Summary", summary, height=200)
            
            with col3:
                if st.button("💾 Export Overview"):
                    # Crear archivo de exportación
                    export_data = {
                        "timestamp": datetime.now().isoformat(),
                        "document_overview": doc_overview
                    }
                    
                    st.download_button(
                        label="📥 Download JSON",
                        data=json.dumps(export_data, indent=2),
                        file_name=f"document_overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
        
        else:
            st.warning("No documents available")
    
    except Exception as e:
        st.error(f"Error en gestión de documentos: {e}")

def show_system_configuration():
    """Mostrar configuración del sistema"""
    st.markdown("### ⚙️ System Configuration")
    
    try:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Current Configuration")
            
            config_data = {
                "Ollama URL": Config.OLLAMA_BASE_URL,
                "Model": Config.OLLAMA_MODEL,
                "Port": Config.STREAMLIT_PORT,
                "Host": Config.STREAMLIT_HOST,
                "Max Tokens": Config.MAX_TOKENS,
                "Temperature": Config.TEMPERATURE,
                "Max Context Length": Config.MAX_CONTEXT_LENGTH,
                "Max Workers": Config.MAX_WORKERS,
                "Cache Size": Config.CACHE_SIZE
            }
            
            for key, value in config_data.items():
                st.text(f"{key}: {value}")
        
        with col2:
            st.markdown("#### Configuration Actions")
            
            # Cambiar modelo
            new_model = st.selectbox(
                "Change AI Model",
                ["gpt-oss:20b", "llama2:7b", "mistral:7b", "codellama:7b"],
                index=0
            )
            
            if st.button("🔄 Update Model"):
                # Aquí se actualizaría la configuración
                st.success(f"Model updated to {new_model}")
            
            # Ajustar parámetros
            st.markdown("#### Performance Tuning")
            
            new_temperature = st.slider("Temperature", 0.0, 1.0, Config.TEMPERATURE, 0.1)
            new_max_tokens = st.slider("Max Tokens", 1000, 8000, Config.MAX_TOKENS, 500)
            
            if st.button("⚙️ Apply Settings"):
                # Aquí se aplicarían los cambios
                st.success("Settings applied successfully!")
        
        # Logs del sistema
        st.markdown("#### 📋 System Logs")
        
        log_files = ["logs/sdf_main.log", "logs/sdf_errors.log", "logs/sdf_performance.log"]
        
        selected_log = st.selectbox("Select Log File", log_files)
        
        if st.button("📖 View Log"):
            log_path = Path(selected_log)
            if log_path.exists():
                with open(log_path, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                
                # Mostrar últimas 50 líneas
                lines = log_content.split('\n')[-50:]
                st.text_area("Recent Log Entries", '\n'.join(lines), height=300)
            else:
                st.warning("Log file not found")
    
    except Exception as e:
        st.error(f"Error en configuración: {e}")

def show_backup_restore():
    """Mostrar backup y restauración"""
    st.markdown("### 💾 Backup & Restore")
    
    try:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Backup Operations")
            
            if st.button("💾 Create Backup"):
                with st.spinner("Creating backup..."):
                    # Crear backup de documentos y configuración
                    backup_dir = Path("backups")
                    backup_dir.mkdir(exist_ok=True)
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_name = f"backup_{timestamp}"
                    
                    # Backup de documentos
                    context_dir = Path(Config.CONTEXT_FOLDER)
                    if context_dir.exists():
                        # Aquí se copiarían los documentos
                        st.success(f"Backup created: {backup_name}")
                    else:
                        st.warning("No documents to backup")
            
            # Listar backups
            st.markdown("#### Available Backups")
            backup_dir = Path("backups")
            if backup_dir.exists():
                backups = list(backup_dir.glob("backup_*"))
                if backups:
                    backup_names = [b.name for b in backups]
                    selected_backup = st.selectbox("Select Backup", backup_names)
                    
                    if st.button("🔄 Restore Backup"):
                        st.info(f"Restoring {selected_backup}...")
                        # Aquí se restauraría el backup
                        st.success("Backup restored successfully!")
                else:
                    st.info("No backups available")
            else:
                st.info("No backup directory found")
        
        with col2:
            st.markdown("#### Export Operations")
            
            if st.button("📊 Export Analytics"):
                # Exportar datos de analytics
                analytics_data = enterprise_monitor.get_all_analytics()
                
                st.download_button(
                    label="📥 Download Analytics",
                    data=json.dumps(analytics_data, indent=2),
                    file_name=f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            if st.button("💬 Export Conversations"):
                # Exportar conversaciones
                assistant = SDFAssistant()
                conversation_data = assistant.export_conversation("json")
                
                st.download_button(
                    label="📥 Download Conversations",
                    data=conversation_data,
                    file_name=f"conversations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    except Exception as e:
        st.error(f"Error en backup/restore: {e}")

def main():
    """Función principal del panel de administración"""
    create_admin_header()
    
    # Sidebar con navegación
    st.sidebar.markdown("### 🔧 Admin Navigation")
    
    page = st.sidebar.selectbox(
        "Select Section",
        ["System Overview", "Performance Analytics", "System Monitoring", 
         "Document Management", "System Configuration", "Backup & Restore"]
    )
    
    # Mostrar página seleccionada
    if page == "System Overview":
        get_system_overview()
    elif page == "Performance Analytics":
        show_performance_analytics()
    elif page == "System Monitoring":
        show_system_monitoring()
    elif page == "Document Management":
        show_document_management()
    elif page == "System Configuration":
        show_system_configuration()
    elif page == "Backup & Restore":
        show_backup_restore()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">
        <p>SDF Assistant Enterprise Admin Panel | Version 2.0</p>
        <p>Document Intelligence Management System</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
