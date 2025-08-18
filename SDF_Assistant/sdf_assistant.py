#!/usr/bin/env python3
"""
SDF Assistant - Enterprise Edition
Asistente IA avanzado con búsqueda dinámica de contexto y funcionalidades enterprise
"""

import os
import time
import logging
import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

from langchain_ollama import OllamaLLM
from langchain.schema import HumanMessage, SystemMessage

from config import Config
from document_processor import DocumentProcessor

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SDFAssistant:
    """Asistente SDF Enterprise con búsqueda de contexto dinámica y funcionalidades avanzadas"""
    
    def __init__(self, model_name: str = None, temperature: float = None, max_tokens: int = None):
        """Inicializar SDF Assistant con configuración personalizable"""
        self.config = self._load_config(model_name, temperature, max_tokens)
        self.llm = OllamaLLM(
            model=self.config['model_name'],
            base_url=self.config['ollama_url'],
            temperature=self.config['temperature'],
            num_predict=self.config['max_tokens']
        )
        self.document_processor = DocumentProcessor()
        self.documents_cache = {}
        self.conversation_history = []
        self.analytics = {
            'total_queries': 0,
            'avg_response_time': 0,
            'documents_processed': 0,
            'search_accuracy': 0.0,
            'last_activity': None
        }
        self._load_documents()
    
    def _load_config(self, model_name: str = None, temperature: float = None, max_tokens: int = None) -> Dict:
        """Cargar configuración con valores por defecto o personalizados"""
        return {
            'model_name': model_name or Config.OLLAMA_MODEL,
            'ollama_url': Config.OLLAMA_BASE_URL,
            'temperature': temperature or Config.TEMPERATURE,
            'max_tokens': max_tokens or Config.MAX_TOKENS,
            'context_length': Config.MAX_CONTEXT_LENGTH,
            'chunk_size': Config.CONTEXT_CHUNK_SIZE
        }
    
    def update_settings(self, model_name: str, temperature: float, max_tokens: int):
        """Actualizar configuración del sistema en tiempo real"""
        self.config = self._load_config(model_name, temperature, max_tokens)
        self.llm = OllamaLLM(
            model=self.config['model_name'],
            base_url=self.config['ollama_url'],
            temperature=self.config['temperature'],
            num_predict=self.config['max_tokens']
        )
        logger.info(f"✅ Configuración actualizada: {model_name}, temp={temperature}, tokens={max_tokens}")
    
    def _load_documents(self):
        """Cargar documentos con mejor manejo de errores y logging"""
        logger.info("🔄 Cargando documentos para SDF...")
        start_time = time.time()
        
        try:
            context_folder = Path(Config.CONTEXT_FOLDER)
            if not context_folder.exists():
                context_folder.mkdir()
                logger.info(f"📁 Carpeta '{Config.CONTEXT_FOLDER}' creada")
                return
            
            documents = self.document_processor.process_folder(context_folder)
            self.documents_cache = documents
            
            self.analytics['documents_processed'] = len(documents)
            load_time = time.time() - start_time
            
            logger.info(f"✅ SDF cargados {len(documents)} documentos en {load_time:.2f}s")
            
        except Exception as e:
            logger.error(f"❌ Error cargando documentos: {e}")
            self.documents_cache = {}
    
    def reload_documents(self):
        """Recargar documentos con limpieza de cache"""
        logger.info("🔄 Recargando documentos...")
        self.documents_cache.clear()
        self._load_documents()
        logger.info("✅ Documentos recargados")
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extraer palabras clave mejoradas con análisis semántico"""
        # Limpiar y normalizar texto
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        # Filtrar palabras comunes y muy cortas
        stop_words = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las', 'una', 'como', 'pero', 'sus', 'me', 'hasta', 'hay', 'donde', 'han', 'quien', 'están', 'estado', 'desde', 'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 'algunas', 'algo', 'nosotros'}
        
        keywords = []
        for word in words:
            if len(word) > 3 and word not in stop_words:
                keywords.append(word)
        
        # Agregar términos compuestos (bigramas)
        bigrams = []
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            if len(bigram) > 5:
                bigrams.append(bigram)
        
        return keywords + bigrams[:10]  # Limitar a 10 bigramas
    
    def _find_relevant_documents(self, user_message: str) -> List[str]:
        """Búsqueda avanzada de documentos relevantes con puntuación mejorada"""
        if not self.documents_cache:
            return []
        
        keywords = self._extract_keywords(user_message)
        relevant_docs = []
        
        for doc_name, doc_content in self.documents_cache.items():
            score = 0
            
            # Puntuación por coincidencia de palabras clave
            for keyword in keywords:
                if keyword.lower() in doc_content.lower():
                    score += 2
                    
                    # Bonus por coincidencia exacta
                    if keyword.lower() in doc_name.lower():
                        score += 3
            
            # Bonus por tipo de archivo mencionado
            file_extensions = {
                'excel': ['.xlsx', '.xls'],
                'pdf': ['.pdf'],
                'csv': ['.csv'],
                'word': ['.docx', '.doc'],
                'texto': ['.txt', '.md']
            }
            
            for file_type, extensions in file_extensions.items():
                if file_type in user_message.lower():
                    if any(ext in doc_name.lower() for ext in extensions):
                        score += 5
            
            # Bonus por términos específicos del dominio
            domain_terms = {
                'ventas': ['venta', 'ventas', 'comercial', 'cliente'],
                'finanzas': ['financiero', 'dinero', 'presupuesto', 'costo'],
                'recursos humanos': ['empleado', 'personal', 'hr', 'rrhh'],
                'políticas': ['política', 'norma', 'regla', 'procedimiento']
            }
            
            for domain, terms in domain_terms.items():
                if domain in user_message.lower():
                    for term in terms:
                        if term in doc_content.lower():
                            score += 3
            
            if score > 0:
                relevant_docs.append((doc_name, score))
        
        # Ordenar por puntuación y retornar top 5
        relevant_docs.sort(key=lambda x: x[1], reverse=True)
        return [doc[0] for doc in relevant_docs[:5]]
    
    def _get_context_from_relevant_docs(self, relevant_docs: List[str]) -> str:
        """Construir contexto optimizado desde documentos relevantes"""
        if not relevant_docs:
            return ""
        
        context_parts = []
        total_length = 0
        
        for doc_name in relevant_docs:
            if doc_name in self.documents_cache:
                content = self.documents_cache[doc_name]
                
                # Limitar longitud por documento
                if len(content) > self.config['chunk_size']:
                    content = content[:self.config['chunk_size']] + "..."
                
                context_parts.append(f"📄 {doc_name}:\n{content}\n")
                total_length += len(content)
                
                # Limitar contexto total
                if total_length > self.config['context_length']:
                    break
        
        return "\n".join(context_parts)
    
    def chat(self, user_message: str) -> Dict[str, Any]:
        """Procesar mensaje del usuario con análisis avanzado"""
        start_time = time.time()
        
        try:
            # Actualizar analytics
            self.analytics['total_queries'] += 1
            self.analytics['last_activity'] = datetime.now().isoformat()
            
            # Buscar documentos relevantes
            relevant_docs = self._find_relevant_documents(user_message)
            
            if not relevant_docs:
                logger.info("No se encontraron documentos relevantes, usando todos los documentos")
                relevant_docs = list(self.documents_cache.keys())
            
            # Construir contexto
            context = self._get_context_from_relevant_docs(relevant_docs)
            
            # Crear prompt del sistema
            system_prompt = f"""Eres SDF Assistant, un asistente de IA especializado en análisis de documentos empresariales.

CONTEXTO DE DOCUMENTOS:
{context}

INSTRUCCIONES:
1. Analiza solo la información de los documentos proporcionados
2. Proporciona respuestas precisas y detalladas
3. Si la información no está en los documentos, indícalo claramente
4. Usa un tono profesional y empresarial
5. Incluye insights y análisis cuando sea relevante

Documentos analizados: {', '.join(relevant_docs[:3])}

Responde de manera clara y estructurada:"""

            # Generar respuesta
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            
            # Calcular tiempo de respuesta
            response_time = time.time() - start_time
            
            # Actualizar analytics
            self._update_analytics(response_time)
            
            # Guardar en historial
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'user_message': user_message,
                'assistant_response': response.content,
                'relevant_docs': relevant_docs,
                'response_time': response_time
            })
            
            return {
                "success": True,
                "response": response.content,
                "processing_time": response_time,
                "documents_used": relevant_docs[:3],
                "confidence_score": self._calculate_confidence(relevant_docs, user_message)
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
    
    def _update_analytics(self, response_time: float):
        """Actualizar métricas de analytics"""
        if self.analytics['avg_response_time'] == 0:
            self.analytics['avg_response_time'] = response_time
        else:
            self.analytics['avg_response_time'] = (
                self.analytics['avg_response_time'] + response_time
            ) / 2
    
    def _calculate_confidence(self, relevant_docs: List[str], user_message: str) -> float:
        """Calcular puntuación de confianza de la respuesta"""
        if not relevant_docs:
            return 0.0
        
        # Factores de confianza
        doc_coverage = min(len(relevant_docs) / 3, 1.0)  # Más documentos = mayor confianza
        keyword_density = len(self._extract_keywords(user_message)) / 10  # Más keywords = mayor confianza
        
        confidence = (doc_coverage + keyword_density) / 2
        return min(confidence, 1.0)
    
    def generate_summary(self) -> str:
        """Generar resumen ejecutivo de todos los documentos"""
        if not self.documents_cache:
            return "No hay documentos cargados para generar resumen."
        
        try:
            summary_prompt = f"""Genera un resumen ejecutivo de los siguientes documentos empresariales:

DOCUMENTOS:
{chr(10).join([f"- {doc_name}: {content[:500]}..." for doc_name, content in self.documents_cache.items()])}

INSTRUCCIONES:
1. Identifica los temas principales
2. Extrae información clave y métricas importantes
3. Identifica tendencias o patrones
4. Proporciona insights empresariales
5. Estructura el resumen de manera profesional

Resumen ejecutivo:"""

            messages = [
                SystemMessage(content=summary_prompt),
                HumanMessage(content="Genera un resumen ejecutivo detallado")
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generando resumen: {e}")
            return f"Error generando resumen: {str(e)}"
    
    def search_documents(self, query: str) -> Dict[str, Any]:
        """Búsqueda avanzada en documentos"""
        if not self.documents_cache:
            return {"success": False, "results": [], "message": "No hay documentos cargados"}
        
        try:
            relevant_docs = self._find_relevant_documents(query)
            results = []
            
            for doc_name in relevant_docs:
                if doc_name in self.documents_cache:
                    content = self.documents_cache[doc_name]
                    
                    # Buscar coincidencias específicas
                    matches = []
                    query_terms = query.lower().split()
                    
                    for term in query_terms:
                        if term in content.lower():
                            # Encontrar contexto alrededor del término
                            start = max(0, content.lower().find(term) - 100)
                            end = min(len(content), content.lower().find(term) + 100)
                            context = content[start:end]
                            matches.append(f"...{context}...")
                    
                    if matches:
                        results.append({
                            "document": doc_name,
                            "relevance_score": len(matches),
                            "matches": matches[:3]  # Top 3 matches
                        })
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "total_results": len(results)
            }
            
        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")
            return {"success": False, "results": [], "error": str(e)}
    
    def get_analytics(self) -> Dict[str, Any]:
        """Obtener métricas y analytics del sistema"""
        return {
            "system_metrics": self.analytics,
            "documents_loaded": len(self.documents_cache),
            "conversation_history_length": len(self.conversation_history),
            "system_config": self.config
        }
    
    def export_conversation(self, format: str = "json") -> str:
        """Exportar historial de conversación"""
        if format == "json":
            return json.dumps(self.conversation_history, indent=2, ensure_ascii=False)
        elif format == "txt":
            text = "SDF Assistant - Historial de Conversación\n"
            text += "=" * 50 + "\n\n"
            
            for entry in self.conversation_history:
                text += f"Fecha: {entry['timestamp']}\n"
                text += f"Usuario: {entry['user_message']}\n"
                text += f"Asistente: {entry['assistant_response']}\n"
                text += f"Documentos usados: {', '.join(entry['relevant_docs'])}\n"
                text += f"Tiempo de respuesta: {entry['response_time']:.2f}s\n"
                text += "-" * 30 + "\n\n"
            
            return text
        else:
            raise ValueError("Formato no soportado. Use 'json' o 'txt'")
    
    def get_document_overview(self) -> Dict[str, Any]:
        """Obtener vista general de documentos cargados"""
        if not self.documents_cache:
            return {"success": False, "message": "No hay documentos cargados"}
        
        documents_info = []
        file_types = {}
        
        for doc_name, content in self.documents_cache.items():
            file_ext = Path(doc_name).suffix.lower()
            file_type = file_ext[1:] if file_ext else "unknown"
            
            if file_type not in file_types:
                file_types[file_type] = 0
            file_types[file_type] += 1
            
            documents_info.append({
                "name": doc_name,
                "file_type": file_type,
                "size": len(content),
                "last_modified": datetime.now().isoformat()
            })
        
        return {
            "success": True,
            "total_documents": len(self.documents_cache),
            "file_types": file_types,
            "documents": documents_info
        }
