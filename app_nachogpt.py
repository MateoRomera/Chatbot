import streamlit as st
import time
from simple_ai_assistant import SimpleAIAssistant
from config import Config
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la página
st.set_page_config(
    page_title="NachoGPT",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS minimalista
st.markdown("""
<style>
    .main {
        padding: 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .header {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .header h1 {
        font-size: 2.5rem;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .header p {
        color: #7f8c8d;
        font-size: 1.1rem;
    }
    
    .chat-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .message {
        margin-bottom: 1rem;
        padding: 1rem;
        border-radius: 8px;
    }
    
    .user-message {
        background: #3498db;
        color: white;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background: #ecf0f1;
        color: #2c3e50;
        margin-right: 2rem;
    }
    
    .input-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .stTextArea > div > div > textarea {
        border: 2px solid #ecf0f1;
        border-radius: 8px;
        padding: 1rem;
        font-size: 16px;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }
    
    .stButton > button {
        background: #3498db;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background: #2980b9;
        transform: translateY(-1px);
    }
    
    .stats {
        text-align: center;
        color: #7f8c8d;
        font-size: 0.9rem;
        margin-top: 1rem;
    }
    
    .stApp {
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "assistant" not in st.session_state:
    st.session_state.assistant = SimpleAIAssistant()

# Header simple
st.markdown("""
<div class="header">
    <h1>NachoGPT</h1>
    <p>Asistente de IA para análisis de documentos</p>
</div>
""", unsafe_allow_html=True)

# Contenedor de chat
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">
            <p>💬 Escribe tu pregunta para comenzar</p>
            <p>Ejemplo: "¿Dónde está ubicado María González?"</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="message user-message"><strong>Tú:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message assistant-message"><strong>NachoGPT:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input simple
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    user_input = st.text_area(
        "Escribe tu mensaje...",
        key="chat_input",
        height=100,
        placeholder="Ejemplo: ¿Dónde está ubicado María González? ¿Cuántos empleados hay en Santiago?"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("Enviar", use_container_width=True):
            if user_input.strip():
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                with st.spinner("Procesando..."):
                    result = st.session_state.assistant.chat(user_input)
                    
                    if result["success"]:
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": result["response"]
                        })
                    else:
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": f"Error: {result['response']}"
                        })
                
                st.rerun()
    
    with col2:
        if st.button("Limpiar", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col3:
        if st.button("Recargar", use_container_width=True):
            with st.spinner("Recargando..."):
                st.session_state.assistant = SimpleAIAssistant()
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Estadísticas simples
st.markdown(f"""
<div class="stats">
    Documentos: {len(st.session_state.assistant.documents_cache)} | 
    Mensajes: {len(st.session_state.messages)} | 
    Modelo: {Config.OLLAMA_MODEL}
</div>
""", unsafe_allow_html=True)
