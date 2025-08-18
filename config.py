import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración del sistema SDF optimizada para contexto extenso"""
    
    # Configuración de Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")  # Modelo GPT OSS 20B
    
    # Configuración de documentos
    CONTEXT_FOLDER = os.getenv("CONTEXT_FOLDER", "contexto")
    SUPPORTED_EXTENSIONS = {
        '.txt': 'text',
        '.md': 'markdown',
        '.pdf': 'pdf',
        '.docx': 'word',
        '.doc': 'word',
        '.xlsx': 'excel',
        '.xls': 'excel',
        '.csv': 'csv',
        '.ods': 'excel'
    }
    
    # Configuración de la aplicación optimizada
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "vector_db")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "8192"))  # Aumentado para contexto extenso
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Configuración de procesamiento paralelo
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))  # Número de workers para procesamiento paralelo
    CACHE_SIZE = int(os.getenv("CACHE_SIZE", "100"))  # Tamaño del cache de documentos
    
    # Configuración de contexto
    MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", "8000"))  # Longitud máxima del contexto
    CONTEXT_CHUNK_SIZE = int(os.getenv("CONTEXT_CHUNK_SIZE", "2000"))  # Tamaño de chunks para archivos grandes
    
    # Configuración de Streamlit
    STREAMLIT_TITLE = os.getenv("STREAMLIT_TITLE", "🤖 SDF - Asistente IA Avanzado")
    STREAMLIT_PAGE_CONFIG = {
        "page_title": os.getenv("STREAMLIT_PAGE_TITLE", "SDF Assistant"),
        "page_icon": os.getenv("STREAMLIT_PAGE_ICON", "🤖"),
        "layout": os.getenv("STREAMLIT_LAYOUT", "wide"),
        "initial_sidebar_state": os.getenv("STREAMLIT_SIDEBAR_STATE", "expanded")
    }
    
    # Configuración de red
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8502"))
    STREAMLIT_HOST = os.getenv("STREAMLIT_HOST", "localhost")
