import streamlit as st
import time
from sdf_assistant import SDFAssistant
from config import Config
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la página
st.set_page_config(
    page_title="SDF Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS moderno y atractivo
st.markdown("""
<style>
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .header {
        text-align: center;
        margin-bottom: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
    }
    
    .header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        min-height: 500px;
        max-height: 700px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
    }
    
    .message {
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        border-radius: 12px;
        position: relative;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 3rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .assistant-message {
        background: #f8f9fa;
        color: #2c3e50;
        margin-right: 3rem;
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .input-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    
    .stTextArea > div > div > textarea {
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 1.5rem;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stats {
        text-align: center;
        color: #6c757d;
        font-size: 0.9rem;
        margin-top: 1rem;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .sidebar {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .file-upload {
        border: 2px dashed #667eea;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: #f8f9ff;
        transition: all 0.3s ease;
    }
    
    .file-upload:hover {
        border-color: #764ba2;
        background: #f0f2ff;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "assistant" not in st.session_state:
    st.session_state.assistant = SDFAssistant()

# Header atractivo
st.markdown("""
<div class="header">
    <h1>🤖 SDF Assistant</h1>
    <p>Smart Document Finder - Asistente IA para análisis inteligente de documentos</p>
</div>
""", unsafe_allow_html=True)

# Sidebar para configuración y carga de archivos
with st.sidebar:
    st.markdown('<div class="sidebar">', unsafe_allow_html=True)
    
    st.subheader("📁 Cargar Documentos")
    
    uploaded_files = st.file_uploader(
        "Sube tus documentos (Excel, PDF, CSV)",
        type=['xlsx', 'xls', 'pdf', 'csv', 'txt', 'docx'],
        accept_multiple_files=True,
        help="Puedes subir múltiples archivos a la vez"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Guardar archivo en la carpeta contexto
            import os
            file_path = os.path.join(Config.CONTEXT_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ {uploaded_file.name} cargado")
        
        # Recargar documentos después de subir
        if st.button("🔄 Recargar Documentos"):
            with st.spinner("Recargando documentos..."):
                st.session_state.assistant.reload_documents()
                st.success("Documentos recargados exitosamente")
    
    st.markdown("---")
    
    # Información del sistema
    st.subheader("⚙️ Información del Sistema")
    st.info(f"Modelo: {Config.OLLAMA_MODEL}")
    st.info(f"Documentos cargados: {len(st.session_state.assistant.documents_cache)}")
    
    # Botón para limpiar conversación
    if st.button("🗑️ Limpiar Conversación"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Contenedor principal
col1, col2 = st.columns([2, 1])

with col1:
    # Contenedor de chat
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; color: #6c757d; margin-top: 3rem;">
            <h3>💬 ¡Bienvenido a SDF Assistant!</h3>
            <p>Sube tus documentos en la barra lateral y haz preguntas sobre ellos.</p>
            <p><strong>Ejemplos:</strong></p>
            <ul style="text-align: left; display: inline-block;">
                <li>"¿Qué datos contiene el archivo Excel?"</li>
                <li>"Analiza las tendencias en el CSV"</li>
                <li>"¿Qué información hay en el PDF?"</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="message user-message"><strong>👤 Tú:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message assistant-message"><strong>🤖 SDF:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Input para preguntas
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    user_input = st.text_area(
        "Escribe tu pregunta sobre los documentos...",
        key="chat_input",
        height=120,
        placeholder="Ejemplo: ¿Qué datos contiene el archivo Excel? ¿Cuáles son las tendencias en el CSV? ¿Qué información hay en el PDF?"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🚀 Enviar", use_container_width=True):
            if user_input.strip():
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                with st.spinner("🔍 SDF analizando documentos..."):
                    result = st.session_state.assistant.chat(user_input)
                    
                    if result["success"]:
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": result["response"]
                        })
                    else:
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": f"❌ Error: {result['response']}"
                        })
                
                st.rerun()
    
    with col2:
        if st.button("🔄 Recargar", use_container_width=True):
            with st.spinner("Recargando SDF..."):
                st.session_state.assistant = SDFAssistant()
                st.rerun()
    
    with col3:
        if st.button("📊 Documentos", use_container_width=True):
            overview = st.session_state.assistant.get_document_overview()
            if overview["success"]:
                st.info(f"📁 {overview['total_documents']} documentos cargados")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Panel de información
    st.subheader("📊 Estadísticas")
    
    # Información de documentos
    overview = st.session_state.assistant.get_document_overview()
    if overview["success"]:
        st.metric("Documentos", overview["total_documents"])
        
        # Tipos de archivo
        file_types = {}
        for doc in overview["documents"]:
            file_type = doc["file_type"]
            if file_type not in file_types:
                file_types[file_type] = 0
            file_types[file_type] += 1
        
        st.subheader("📁 Tipos de Archivo")
        for file_type, count in file_types.items():
            st.metric(file_type.upper(), count)
    
    # Información de la conversación
    st.subheader("💬 Conversación")
    st.metric("Mensajes", len(st.session_state.messages))
    
    if st.session_state.messages:
        last_message = st.session_state.messages[-1]
        if last_message["role"] == "assistant":
            st.info("✅ Última respuesta generada")
        else:
            st.info("⏳ Esperando respuesta...")

# Estadísticas en el pie de página
if st.session_state.messages:
    last_result = None
    for message in reversed(st.session_state.messages):
        if message["role"] == "assistant":
            # Buscar el resultado más reciente
            break
    
    st.markdown(f"""
    <div class="stats">
        📊 Documentos: {len(st.session_state.assistant.documents_cache)} | 
        💬 Mensajes: {len(st.session_state.messages)} | 
        🤖 Modelo: {Config.OLLAMA_MODEL}
    </div>
    """, unsafe_allow_html=True)
