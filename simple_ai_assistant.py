import os
import logging
import json
from typing import Dict, Any, List
from langchain_ollama import OllamaLLM
from langchain.schema import HumanMessage, SystemMessage
from document_processor import DocumentProcessor
from config import Config
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleAIAssistant:
    """Asistente de IA inteligente y autónomo"""
    
    def __init__(self):
        self.llm = OllamaLLM(
            model=Config.OLLAMA_MODEL,
            base_url=Config.OLLAMA_BASE_URL,
            temperature=0.7,  # Más creatividad para análisis autónomo
            timeout=120,
            num_ctx=8192,
            num_predict=2048,
            repeat_penalty=1.1,
            top_k=40,
            top_p=0.9
        )
        self.document_processor = DocumentProcessor()
        self.documents_cache = {}
        self._load_documents()
    
    def _load_documents(self):
        """Carga todos los documentos disponibles"""
        try:
            logger.info("🔄 Cargando documentos...")
            start_time = time.time()
            
            documents = self.document_processor.process_folder(Config.CONTEXT_FOLDER)
            
            for doc in documents:
                if doc and doc.get("content"):
                    # Manejar cualquier tipo de contenido
                    content = doc["content"]
                    if isinstance(content, dict):
                        if "success" in content and not content["success"]:
                            logger.warning(f"Documento con error: {doc['metadata']['file_name']}")
                            continue
                        content = str(content)
                    
                    file_name = doc["metadata"]["file_name"]
                    self.documents_cache[file_name] = {
                        "content": content,
                        "metadata": doc["metadata"],
                        "file_type": doc["metadata"].get("file_type", "unknown")
                    }
            
            load_time = time.time() - start_time
            logger.info(f"✅ Cargados {len(self.documents_cache)} documentos en {load_time:.2f}s")
                
        except Exception as e:
            logger.error(f"❌ Error en carga de documentos: {e}")
    
    def _get_intelligent_context(self, user_message: str) -> str:
        """Extrae contexto de manera inteligente y autónoma sin límites"""
        if not self.documents_cache:
            return ""
        
        # Dejar que la IA decida qué documentos son relevantes
        context_parts = []
        
        for file_name, doc_data in self.documents_cache.items():
            try:
                content = str(doc_data.get("content", ""))
                if not content or content == "None":
                    continue
                    
                file_type = doc_data.get("file_type", "")
                
                # Incluir TODOS los archivos completos para análisis autónomo
                context_parts.append(f"ARCHIVO: {file_name}\nTIPO: {file_type}\nCONTENIDO:\n{content}\n")
                    
            except Exception as e:
                logger.warning(f"Error procesando {file_name}: {e}")
                continue
        
        full_context = "\n".join(context_parts)
        logger.info(f"Contexto completo generado: {len(full_context)} caracteres")
        
        return full_context
    
    def chat(self, user_message: str) -> Dict[str, Any]:
        """Chat inteligente y autónomo sin límites"""
        try:
            start_time = time.time()
            
            # Obtener contexto completo para análisis autónomo
            context = self._get_intelligent_context(user_message)
            
            # Prompt inteligente que permite análisis autónomo sin límites
            system_prompt = """Eres una IA inteligente y autónoma con capacidad de análisis avanzado sin límites.

CAPACIDADES:
- Analiza cualquier tipo de datos y archivos por tu cuenta
- Identifica patrones, tendencias y relaciones en los datos
- Extrae información relevante sin depender de estructuras predefinidas
- Piensa de manera crítica y creativa sobre los datos
- Proporciona insights valiosos y análisis profundos
- NO hay límites en el contexto - analiza TODO lo disponible

REGLAS:
1. SIEMPRE responde en ESPAÑOL
2. Analiza los datos de manera autónoma e inteligente
3. No te limites a estructuras predefinidas
4. Usa tu capacidad de razonamiento para interpretar los datos
5. Proporciona análisis detallados y conclusiones inteligentes
6. Si encuentras datos interesantes, compártelos
7. Sé creativo en tu análisis pero basado en los datos reales
8. IMPORTANTE: Responde de manera completa y clara, sin cortar la respuesta
9. Analiza TODOS los archivos disponibles, no solo algunos

DATOS DISPONIBLES (CONTEXTO COMPLETO):
{context}

PREGUNTA DEL USUARIO: {user_message}

Analiza TODOS los datos de manera inteligente y autónoma. Piensa por ti misma sobre qué información es relevante y cómo responder de manera útil y completa. Responde de forma clara y estructurada."""

            if context:
                full_message = system_prompt.format(context=context, user_message=user_message)
            else:
                full_message = f"PREGUNTA: {user_message}\n\nResponde de manera inteligente y autónoma en español."

            # Ejecutar análisis autónomo sin límites
            try:
                response = self.llm.invoke(full_message)
                response_text = response.content if hasattr(response, 'content') else str(response)
                
                # Asegurar que la respuesta no esté vacía
                if not response_text or response_text.strip() == "":
                    response_text = "No pude generar una respuesta. Por favor, reformula tu pregunta."
                
                processing_time = time.time() - start_time
                logger.info(f"✅ Análisis autónomo completado en {processing_time:.2f}s")
                
                return {
                    "success": True,
                    "response": response_text,
                    "processing_time": processing_time,
                    "context_length": len(context) if context else 0,
                    "analysis_type": "autonomous_unlimited"
                }
                
            except Exception as e:
                logger.error(f"Error en análisis autónomo: {e}")
                return {
                    "success": False,
                    "response": f"Error en el análisis: {str(e)}",
                    "processing_time": time.time() - start_time
                }
                
        except Exception as e:
            logger.error(f"Error en chat: {e}")
            return {
                "success": False,
                "response": f"Error procesando tu mensaje: {str(e)}"
            }
    
    def analyze_any_data(self, query: str) -> Dict[str, Any]:
        """Análisis autónomo de cualquier tipo de datos"""
        return self.chat(query)
    
    def get_document_overview(self) -> Dict[str, Any]:
        """Obtiene una visión general de todos los documentos disponibles"""
        overview = []
        
        for file_name, doc_data in self.documents_cache.items():
            content = str(doc_data.get("content", ""))
            file_type = doc_data.get("file_type", "")
            
            overview.append({
                "file_name": file_name,
                "file_type": file_type,
                "content_length": len(content),
                "has_data": len(content) > 100
            })
        
        return {
            "success": True,
            "documents": overview,
            "total_documents": len(overview)
        }
    
    def clear_conversation(self):
        """Limpia el historial de conversación"""
        logger.info("Historial de conversación limpiado")
