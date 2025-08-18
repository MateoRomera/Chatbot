#!/usr/bin/env python3
"""
SDF Assistant - Enterprise Edition
Interfaz web moderna y profesional para análisis de documentos
"""

import streamlit as st
import time
import os
from datetime import datetime
from pathlib import Path
import json

# Importar componentes del sistema
from sdf_assistant import SDFAssistant
from config import Config
from document_processor import DocumentProcessor

# Configuración de la página
st.set_page_config(
    page_title=Config.STREAMLIT_PAGE_CONFIG["page_title"],
    page_icon=Config.STREAMLIT_PAGE_CONFIG["page_icon"],
    layout=Config.STREAMLIT_PAGE_CONFIG["layout"],
    initial_sidebar_state=Config.STREAMLIT_PAGE_CONFIG["initial_sidebar_state"]
)

# CSS personalizado para diseño enterprise
st.markdown("""
<style>
    /* Diseño Enterprise */
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: #e8f4fd;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    .chat-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 0 15px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .assistant-message {
        background: white;
        border: 1px solid #e9ecef;
        padding: 1rem;
        border-radius: 15px 15px 15px 0;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .input-container {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        border: 2px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .sidebar-section {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online { background-color: #28a745; }
    .status-offline { background-color: #dc3545; }
    .status-processing { background-color: #ffc107; }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1e3c72;
    }
    
    .metric-label {
        color: #6c757d;
        font-size: 0.9rem;
    }
    
    /* Botones enterprise */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e9ecef;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* File uploader */
    .stFileUploader > div {
        border: 2px dashed #e9ecef;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: #f8f9fa;
    }
    
    .stFileUploader > div:hover {
        border-color: #667eea;
        background: #f0f2ff;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Inicializar variables de sesión"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'assistant' not in st.session_state:
        st.session_state.assistant = None
    if 'documents_loaded' not in st.session_state:
        st.session_state.documents_loaded = False
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'stats' not in st.session_state:
        st.session_state.stats = {
            'total_questions': 0,
            'total_documents': 0,
            'avg_response_time': 0,
            'last_activity': None
        }

def create_header():
    """Crear header principal"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 SDF Assistant</h1>
        <p>Enterprise Document Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Crear sidebar con funcionalidades enterprise"""
    with st.sidebar:
        st.markdown("### 📊 System Status")
        
        # Indicador de estado del sistema
        if st.session_state.assistant:
            st.markdown('<span class="status-indicator status-online"></span>System Online', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-indicator status-offline"></span>System Offline', unsafe_allow_html=True)
        
        # Métricas del sistema
        st.markdown("### 📈 Analytics")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{st.session_state.stats['total_questions']}</div>
                <div class="metric-label">Questions</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{st.session_state.stats['total_documents']}</div>
                <div class="metric-label">Documents</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Gestión de documentos
        st.markdown("### 📁 Document Management")
        
        with st.expander("Upload Documents", expanded=False):
            uploaded_files = st.file_uploader(
                "Select files to analyze",
                type=['pdf', 'xlsx', 'xls', 'csv', 'docx', 'txt', 'md'],
                accept_multiple_files=True,
                help="Upload documents for analysis"
            )
            
            if uploaded_files:
                if st.button("📥 Process Documents", key="process_upload"):
                    process_uploaded_files(uploaded_files)
        
        # Configuración del sistema
        st.markdown("### ⚙️ System Configuration")
        
        with st.expander("Advanced Settings", expanded=False):
            model_name = st.selectbox(
                "AI Model",
                ["gpt-oss:20b", "llama2:7b", "mistral:7b", "codellama:7b"],
                index=0
            )
            
            temperature = st.slider("Creativity Level", 0.0, 1.0, 0.7, 0.1)
            max_tokens = st.slider("Max Response Length", 1000, 8000, 4000, 500)
            
            if st.button("🔄 Apply Settings"):
                update_system_settings(model_name, temperature, max_tokens)
        
        # Herramientas de análisis
        st.markdown("### 🔧 Analysis Tools")
        
        if st.button("📊 Document Summary", key="summary_btn"):
            generate_document_summary()
        
        if st.button("🔍 Search Documents", key="search_btn"):
            search_documents()
        
        # Exportar conversación
        if st.session_state.messages:
            if st.button("💾 Export Chat", key="export_btn"):
                export_conversation()

def process_uploaded_files(files):
    """Procesar archivos subidos"""
    with st.spinner("Processing uploaded documents..."):
        for uploaded_file in files:
            # Guardar archivo en contexto
            file_path = Path(Config.CONTEXT_FOLDER) / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        # Recargar documentos
        if st.session_state.assistant:
            st.session_state.assistant.reload_documents()
            st.session_state.documents_loaded = True
            st.session_state.stats['total_documents'] = len(list(Path(Config.CONTEXT_FOLDER).glob("*")))
            st.success(f"✅ {len(files)} documents processed successfully!")

def update_system_settings(model_name, temperature, max_tokens):
    """Actualizar configuración del sistema"""
    if st.session_state.assistant:
        st.session_state.assistant.update_settings(model_name, temperature, max_tokens)
        st.success("✅ System settings updated!")

def generate_document_summary():
    """Generar resumen de documentos"""
    if st.session_state.assistant and st.session_state.documents_loaded:
        with st.spinner("Generating document summary..."):
            summary = st.session_state.assistant.generate_summary()
            st.info("📊 Document Summary Generated")
            st.write(summary)

def search_documents():
    """Buscar en documentos"""
    search_query = st.text_input("Enter search terms:")
    if search_query and st.session_state.assistant:
        with st.spinner("Searching documents..."):
            results = st.session_state.assistant.search_documents(search_query)
            st.write("🔍 Search Results:")
            st.write(results)

def export_conversation():
    """Exportar conversación"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sdf_conversation_{timestamp}.json"
    
    conversation_data = {
        "timestamp": timestamp,
        "messages": st.session_state.messages,
        "stats": st.session_state.stats
    }
    
    # Crear archivo de descarga
    st.download_button(
        label="📥 Download Conversation",
        data=json.dumps(conversation_data, indent=2),
        file_name=filename,
        mime="application/json"
    )

def create_chat_interface():
    """Crear interfaz de chat mejorada"""
    st.markdown("### 💬 Document Analysis Chat")
    
    # Contenedor de mensajes
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>SDF Assistant:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Input mejorado con funcionalidad Enter
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Usar JavaScript para detectar Enter y limpiar input
    st.markdown("""
    <script>
        const textInput = document.querySelector('input[type="text"]');
        if (textInput) {
            textInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    // Trigger submit
                    const submitButton = document.querySelector('button[data-testid="baseButton-secondary"]');
                    if (submitButton) {
                        submitButton.click();
                    }
                    // Clear input after a short delay
                    setTimeout(() => {
                        textInput.value = '';
                    }, 100);
                }
            });
        }
    </script>
    """, unsafe_allow_html=True)
    
    # Input con placeholder mejorado
    user_input = st.text_input(
        "Ask about your documents...",
        placeholder="e.g., 'Analyze the sales data in the Excel file' or 'What are the main policies in the PDF?'",
        key="user_input",
        help="Press Enter to send and clear input automatically"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botones de acción
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🚀 Send", key="send_btn"):
            process_user_input(user_input)
    
    with col2:
        if st.button("🔄 Clear Chat", key="clear_btn"):
            st.session_state.messages = []
            st.rerun()
    
    with col3:
        if st.button("📋 New Session", key="new_session_btn"):
            st.session_state.messages = []
            st.session_state.stats['total_questions'] = 0
            st.rerun()

def process_user_input(user_input):
    """Procesar input del usuario"""
    if not user_input.strip():
        return
    
    if not st.session_state.assistant:
        with st.spinner("Initializing SDF Assistant..."):
            st.session_state.assistant = SDFAssistant()
            st.session_state.documents_loaded = True
    
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Procesar con indicador de progreso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🔍 Searching relevant documents...")
        progress_bar.progress(25)
        
        status_text.text("📊 Analyzing content...")
        progress_bar.progress(50)
        
        start_time = time.time()
        
        status_text.text("🤖 Generating response...")
        progress_bar.progress(75)
        
        response = st.session_state.assistant.chat(user_input)
        
        progress_bar.progress(100)
        status_text.text("✅ Response ready!")
        
        # Calcular tiempo de respuesta
        response_time = time.time() - start_time
        
        if response["success"]:
            st.session_state.messages.append({"role": "assistant", "content": response["response"]})
            st.session_state.stats['total_questions'] += 1
            st.session_state.stats['last_activity'] = datetime.now().isoformat()
            
            # Actualizar tiempo promedio de respuesta
            if st.session_state.stats['avg_response_time'] == 0:
                st.session_state.stats['avg_response_time'] = response_time
            else:
                st.session_state.stats['avg_response_time'] = (
                    st.session_state.stats['avg_response_time'] + response_time
                ) / 2
        else:
            st.error(f"❌ Error: {response['response']}")
    
    except Exception as e:
        st.error(f"❌ System Error: {str(e)}")
    
    finally:
        progress_bar.empty()
        status_text.empty()
        time.sleep(0.5)
        st.rerun()

def main():
    """Función principal"""
    initialize_session_state()
    create_header()
    create_sidebar()
    create_chat_interface()
    
    # Footer con información del sistema
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
        <p>SDF Assistant Enterprise Edition | Powered by Ollama & Streamlit</p>
        <p>Document Intelligence Platform for Enterprise</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
