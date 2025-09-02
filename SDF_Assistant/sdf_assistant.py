import os
import logging
import json
from typing import Dict, Any, List
from langchain_ollama import OllamaLLM
from langchain.schema import HumanMessage, SystemMessage
from document_processor import DocumentProcessor
from config import Config
import time
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SDFAssistant:
    """Asistente SDF inteligente con búsqueda de contexto dinámica"""

    def __init__(self):
        self.llm = OllamaLLM(
            model=Config.OLLAMA_MODEL,
            base_url=Config.OLLAMA_BASE_URL,
            temperature=0.7,
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
            logger.info("🔄 Cargando documentos para SDF...")
            start_time = time.time()

            documents = self.document_processor.process_folder(
                Config.CONTEXT_FOLDER)

            for doc in documents:
                if doc and doc.get("content"):
                    content = doc["content"]
                    if isinstance(content, dict):
                        if "success" in content and not content["success"]:
                            logger.warning(
                                f"Documento con error: {doc['metadata']['file_name']}")
                            continue
                        content = str(content)

                    file_name = doc["metadata"]["file_name"]
                    self.documents_cache[file_name] = {
                        "content": content,
                        "metadata": doc["metadata"],
                        "file_type": doc["metadata"].get("file_type", "unknown")
                    }

            load_time = time.time() - start_time
            logger.info(
                f"✅ SDF cargados {len(self.documents_cache)} documentos en {load_time:.2f}s")

        except Exception as e:
            logger.error(f"❌ Error en carga de documentos SDF: {e}")

    def _find_relevant_documents(self, user_message: str) -> List[str]:
        """Encuentra documentos relevantes basándose en la pregunta del usuario"""
        if not self.documents_cache:
            return []

        relevant_docs = []
        user_keywords = self._extract_keywords(user_message.lower())

        for file_name, doc_data in self.documents_cache.items():
            try:
                content = str(doc_data.get("content", "")).lower()
                file_type = doc_data.get("file_type", "")

                # Calcular relevancia basada en palabras clave
                relevance_score = 0
                for keyword in user_keywords:
                    if keyword in content:
                        relevance_score += content.count(keyword)

                # Bonus para tipos de archivo específicos mencionados
                if any(word in user_message.lower() for word in ['excel', 'xlsx', 'hoja', 'tabla']):
                    if file_type == 'excel':
                        relevance_score += 10

                if any(word in user_message.lower() for word in ['csv', 'datos', 'columna']):
                    if file_type == 'csv':
                        relevance_score += 10

                if any(word in user_message.lower() for word in ['pdf', 'documento', 'texto']):
                    if file_type == 'pdf':
                        relevance_score += 10

                # Si el documento es relevante, incluirlo
                if relevance_score > 0:
                    relevant_docs.append((file_name, relevance_score))

            except Exception as e:
                logger.warning(
                    f"Error analizando relevancia de {file_name}: {e}")
                continue

        # Ordenar por relevancia y devolver los más relevantes
        relevant_docs.sort(key=lambda x: x[1], reverse=True)
        return [doc[0] for doc in relevant_docs[:5]]  # Top 5 más relevantes

    def _extract_keywords(self, text: str) -> List[str]:
        """Extrae palabras clave del texto"""
        # Remover palabras comunes y caracteres especiales
        stop_words = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las', 'una', 'como', 'pero', 'sus', 'me', 'hasta', 'hay', 'donde', 'han', 'quien', 'están', 'estado', 'desde', 'todo', 'nos', 'durante', 'todos',
                      'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 'algunas', 'algo', 'nosotros'}

        # Limpiar texto
        text = re.sub(r'[^\w\s]', ' ', text)
        words = text.split()

        # Filtrar palabras relevantes
        keywords = [word for word in words if len(
            word) > 2 and word not in stop_words]

        return keywords

    def _get_context_from_relevant_docs(self, relevant_docs: List[str]) -> str:
        """Obtiene contexto solo de los documentos relevantes"""
        if not relevant_docs:
            return ""

        context_parts = []

        for file_name in relevant_docs:
            if file_name in self.documents_cache:
                doc_data = self.documents_cache[file_name]
                content = str(doc_data.get("content", ""))
                file_type = doc_data.get("file_type", "")

                if content and content != "None":
                    context_parts.append(
                        f"ARCHIVO RELEVANTE: {file_name}\nTIPO: {file_type}\nCONTENIDO:\n{content}\n")

        full_context = "\n".join(context_parts)
        logger.info(
            f"Contexto relevante generado: {len(full_context)} caracteres de {len(relevant_docs)} documentos")

        return full_context

    def chat(self, user_message: str) -> Dict[str, Any]:
        """Chat inteligente con búsqueda de contexto dinámica"""
        try:
            start_time = time.time()

            # Encontrar documentos relevantes
            relevant_docs = self._find_relevant_documents(user_message)

            # Obtener contexto solo de documentos relevantes
            context = self._get_context_from_relevant_docs(relevant_docs)

            # Si no hay documentos relevantes, usar todos los documentos
            if not context:
                logger.info(
                    "No se encontraron documentos relevantes, usando todos los documentos")
                context = self._get_all_context()

            # Prompt inteligente para SDF
            system_prompt = """Eres SDF (Smart Document Finder), una IA inteligente especializada en análisis de documentos.

CAPACIDADES:
- Analizas documentos de manera inteligente y autónoma
- Buscas información específica en Excel, PDF, CSV y otros formatos
- Proporcionas respuestas precisas basadas en los datos disponibles
- Identificas patrones y tendencias en los datos
- Eres capaz de hacer análisis estadísticos y comparativos

REGLAS:
1. SIEMPRE responde en ESPAÑOL
2. Analiza los datos de manera inteligente y autónoma
3. Si la información no está en los documentos, indícalo claramente
4. Proporciona análisis detallados y conclusiones útiles
5. Si encuentras datos interesantes, compártelos
6. Sé preciso y basado en los datos reales
7. IMPORTANTE: Responde de manera completa y clara
8. Menciona qué documentos utilizaste para tu respuesta

DOCUMENTOS RELEVANTES ENCONTRADOS:
{context}

PREGUNTA DEL USUARIO: {user_message}

Analiza los documentos de manera inteligente y proporciona una respuesta útil y completa basada en los datos disponibles."""

            if context:
                full_message = system_prompt.format(
                    context=context, user_message=user_message)
            else:
                full_message = f"PREGUNTA: {user_message}\n\nNo hay documentos disponibles. Responde de manera general en español."

            # Ejecutar análisis
            try:
                response = self.llm.invoke(full_message)
                response_text = response.content if hasattr(
                    response, 'content') else str(response)

                # Asegurar que la respuesta no esté vacía
                if not response_text or response_text.strip() == "":
                    response_text = "No pude generar una respuesta. Por favor, reformula tu pregunta."

                # Limpiar formato de la respuesta
                response_text = self._clean_response_format(response_text)

                processing_time = time.time() - start_time
                logger.info(
                    f"✅ SDF completado en {processing_time:.2f}s usando {len(relevant_docs)} documentos relevantes")

                return {
                    "success": True,
                    "response": response_text,
                    "processing_time": processing_time,
                    "context_length": len(context) if context else 0,
                    "relevant_documents": relevant_docs,
                    "analysis_type": "smart_context_search"
                }

            except Exception as e:
                logger.error(f"Error en análisis SDF: {e}")

                # Manejar errores específicos de Ollama
                error_msg = str(e)
                if "model runner has unexpectedly stopped" in error_msg:
                    return {
                        "success": False,
                        "response": "El modelo de IA se ha detenido inesperadamente. Esto puede deberse a limitaciones de recursos. Por favor, intenta de nuevo en unos momentos o reinicia Ollama.",
                        "processing_time": time.time() - start_time
                    }
                elif "timeout" in error_msg.lower():
                    return {
                        "success": False,
                        "response": "La respuesta tardó demasiado tiempo. Por favor, intenta con una pregunta más específica o verifica que Ollama esté funcionando correctamente.",
                        "processing_time": time.time() - start_time
                    }
                else:
                    return {
                        "success": False,
                        "response": f"Error en el análisis: {error_msg}",
                        "processing_time": time.time() - start_time
                    }

        except Exception as e:
            logger.error(f"Error en chat SDF: {e}")
            return {
                "success": False,
                "response": f"Error procesando tu mensaje: {str(e)}"
            }

    def _clean_response_format(self, response_text: str) -> str:
        """Limpia el formato de la respuesta para eliminar indentación excesiva"""
        if not response_text:
            return response_text

        # Dividir en líneas
        lines = response_text.split('\n')
        cleaned_lines = []

        for line in lines:
            # Eliminar espacios en blanco al inicio y final
            cleaned_line = line.strip()

            # Si la línea no está vacía, agregarla
            if cleaned_line:
                cleaned_lines.append(cleaned_line)
            # Si está vacía, agregar solo un salto de línea (no múltiples espacios)
            elif cleaned_lines and cleaned_lines[-1] != '':
                cleaned_lines.append('')

        # Unir las líneas con saltos de línea normales
        cleaned_text = '\n'.join(cleaned_lines)

        # Eliminar espacios múltiples consecutivos
        cleaned_text = re.sub(r' +', ' ', cleaned_text)

        # Eliminar saltos de línea múltiples consecutivos
        cleaned_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned_text)

        return cleaned_text.strip()

    def _get_all_context(self) -> str:
        """Obtiene contexto de todos los documentos (fallback)"""
        context_parts = []

        for file_name, doc_data in self.documents_cache.items():
            try:
                content = str(doc_data.get("content", ""))
                if not content or content == "None":
                    continue

                file_type = doc_data.get("file_type", "")
                context_parts.append(
                    f"ARCHIVO: {file_name}\nTIPO: {file_type}\nCONTENIDO:\n{content}\n")

            except Exception as e:
                logger.warning(f"Error procesando {file_name}: {e}")
                continue

        return "\n".join(context_parts)

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

    def reload_documents(self):
        """Recarga todos los documentos"""
        logger.info("🔄 Recargando documentos...")
        self.documents_cache = {}
        self._load_documents()
        logger.info("✅ Documentos recargados")

    def clear_conversation(self):
        """Limpia el historial de conversación"""
        logger.info("Historial de conversación limpiado")
