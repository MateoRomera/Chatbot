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
    page_title="IA del Personal Militar Argentino",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS mejorado con tema oscuro y colores azul marino
st.markdown("""
<style>
    /* Variables de color */
    :root {
        --navy-blue: #1e3a8a;
        --light-navy: #3b82f6;
        --white: #ffffff;
        --dark-bg: #0f172a;
        --darker-bg: #020617;
        --border-color: #334155;
        --text-color: #e2e8f0;
    }
    
    /* Estilos generales */
    .main {
        padding: 0;
        max-width: 100%;
        background: var(--dark-bg);
        color: var(--text-color);
    }
    
    /* Ocultar elementos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo general */
    .stApp {
        background: var(--dark-bg);
    }
    
    /* Título principal */
    .main-title {
        background: linear-gradient(135deg, var(--navy-blue) 0%, var(--light-navy) 100%);
        color: var(--white);
        padding: 2rem 1rem;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border-radius: 0 0 15px 15px;
    }
    
    .main-title h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Contenedores principales */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
        background: var(--dark-bg);
    }
    
    /* Secciones - sin bordes ni fondo */
    .section {
        margin-bottom: 2rem;
        padding: 1.5rem;
        border: none;
        border-radius: 0;
        background: transparent;
        box-shadow: none;
        transition: all 0.3s ease;
    }
    
    .section:hover {
        box-shadow: none;
        border: none;
    }
    
    .section-title {
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 1.3rem;
        color: var(--white);
        border-bottom: 3px solid var(--navy-blue);
        padding-bottom: 0.5rem;
    }
    
    /* Área de respuesta - sin bordes */
    .response-area {
        min-height: 200px;
        background: var(--darker-bg);
        padding: 1.5rem;
        border: none;
        border-radius: 0;
        color: var(--text-color);
        font-size: 15px;
        line-height: 1.6;
        white-space: normal;
        word-wrap: break-word;
        box-shadow: none;
        text-align: justify;
    }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, var(--navy-blue) 0%, var(--light-navy) 100%);
        color: var(--white);
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        background: linear-gradient(135deg, var(--light-navy) 0%, var(--navy-blue) 100%);
    }
    
    /* Textarea - sin bordes */
    .stTextArea textarea {
        background: var(--darker-bg);
        border: none;
        border-radius: 0;
        padding: 1rem;
        font-size: 15px;
        color: var(--text-color);
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border: none;
        box-shadow: none;
        background: var(--darker-bg);
    }
    
    /* Selectbox - sin bordes */
    .stSelectbox select {
        background: var(--darker-bg);
        border: none;
        border-radius: 0;
        padding: 0.5rem;
        font-size: 14px;
        color: var(--text-color);
        transition: all 0.3s ease;
    }
    
    .stSelectbox select:focus {
        border: none;
        box-shadow: none;
        background: var(--darker-bg);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: var(--darker-bg);
        border-right: none;
    }
    
    .sidebar .sidebar-content {
        background: var(--darker-bg);
        color: var(--text-color);
    }
    
    /* Mensajes del sistema */
    .stAlert {
        border-radius: 0;
        border: none;
        box-shadow: none;
        background: var(--darker-bg);
        color: var(--text-color);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: var(--navy-blue);
    }
    
    /* Eliminar barras blancas de Streamlit */
    .block-container {
        background: var(--dark-bg);
        padding: 0;
    }
    
    .stApp > header {
        background: var(--dark-bg);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title h1 {
            font-size: 2rem;
        }
        
        .section {
            padding: 1rem;
        }
        
        .main-container {
            padding: 0 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "assistant" not in st.session_state:
    st.session_state.assistant = SDFAssistant()

# Título principal mejorado
st.markdown('<div class="main-title"><h1>🎖️ IA del Personal Militar Argentino</h1></div>',
            unsafe_allow_html=True)

# Contenedor principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Sección 1: Input
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📝 Escribe tu consulta</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_area("Consulta", key="chat_input",
                              height=80, placeholder="Escribe aquí tu consulta...", label_visibility="collapsed")
with col2:
    if st.button("🚀 Enviar"):
        if user_input.strip():
            st.session_state.messages.append(
                {"role": "user", "content": user_input})

            with st.spinner("🔄 Procesando..."):
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

st.markdown('</div>', unsafe_allow_html=True)

# Sección 2: Respuesta
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">💬 Respuesta</div>',
            unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown('<div class="response-area">📋 La respuesta aparecerá aquí...</div>',
                unsafe_allow_html=True)
else:
    # Mostrar solo la última respuesta del asistente
    last_assistant_message = None
    for message in reversed(st.session_state.messages):
        if message["role"] == "assistant":
            last_assistant_message = message["content"]
            break

    if last_assistant_message:
        st.markdown(
            f'<div class="response-area">{last_assistant_message}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="response-area">🔄 Procesando...</div>',
                    unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Sección 3: Query
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🔍 Búsqueda estructurada</div>',
            unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    fuerza = st.selectbox(
        "Fuerza", ["-- Fuerza --", "Ejército", "Armada", "Fuerza Aérea"])

with col2:
    provincia = st.selectbox("Provincia", [
                             "-- Provincia --", "Buenos Aires", "Córdoba", "Santa Fe", "Mendoza", "Tucumán"])

with col3:
    especialidad = st.selectbox("Especialidad", [
                                "-- Especialidad --", "Infantería", "Artillería", "Caballería", "Ingenieros", "Comunicaciones"])

with col4:
    if st.button("🔎 Buscar"):
        st.info("🔍 Búsqueda implementada")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Cerrar main-container

# Sidebar mejorado
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); 
                color: white; 
                padding: 1rem; 
                border-radius: 8px; 
                margin-bottom: 1rem;">
        <h3 style="margin: 0; text-align: center;">⚙️ Sistema</h3>
    </div>
    """, unsafe_allow_html=True)

    st.write(f"🤖 **Modelo:** {Config.OLLAMA_MODEL}")

    overview = st.session_state.assistant.get_document_overview()
    if overview["success"]:
        st.write(f"📚 **Documentos:** {overview['total_documents']}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧹 Limpiar"):
            st.session_state.messages = []
            st.rerun()

    with col2:
        if st.button("🔄 Recargar"):
            st.session_state.assistant.reload_documents()
            st.rerun()
