import os
import PyPDF2
import pandas as pd
import numpy as np
from docx import Document
from typing import List, Dict, Any
import logging
import json
import csv
import chardet
from pathlib import Path
from config import Config
import concurrent.futures
import threading
from functools import lru_cache
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Procesador de documentos optimizado para velocidad y contexto extenso"""
    
    def __init__(self):
        self.supported_extensions = Config.SUPPORTED_EXTENSIONS
        self.supported_extensions.update({
            '.json': 'json', '.xml': 'xml', '.html': 'html', '.htm': 'html',
            '.log': 'log', '.dat': 'data', '.sql': 'sql', '.py': 'python',
            '.js': 'javascript', '.java': 'java', '.cpp': 'cpp', '.c': 'c',
            '.h': 'header', '.yaml': 'yaml', '.yml': 'yaml', '.ini': 'ini',
            '.cfg': 'config', '.conf': 'config', '.properties': 'properties',
            '.tsv': 'tsv', '.parquet': 'parquet', '.feather': 'feather',
            '.pickle': 'pickle', '.pkl': 'pickle', '.h5': 'hdf5', '.hdf5': 'hdf5'
        })
        self._cache = {}
        self._cache_lock = threading.Lock()
    
    @lru_cache(maxsize=100)
    def _get_file_hash(self, file_path: str) -> str:
        """Genera un hash del archivo para cache"""
        try:
            stat = os.stat(file_path)
            return f"{file_path}_{stat.st_mtime}_{stat.st_size}"
        except:
            return file_path
    
    def _is_cached(self, file_path: str) -> bool:
        """Verifica si el archivo está en cache"""
        file_hash = self._get_file_hash(file_path)
        with self._cache_lock:
            return file_hash in self._cache
    
    def _cache_result(self, file_path: str, result: Dict[str, Any]):
        """Guarda el resultado en cache"""
        file_hash = self._get_file_hash(file_path)
        with self._cache_lock:
            self._cache[file_hash] = result
    
    def _get_cached_result(self, file_path: str) -> Dict[str, Any]:
        """Obtiene el resultado del cache"""
        file_hash = self._get_file_hash(file_path)
        with self._cache_lock:
            return self._cache.get(file_hash, {})
    
    def process_file_optimized(self, file_path: str) -> Dict[str, Any]:
        """Procesa un archivo con optimizaciones de velocidad"""
        # Verificar cache primero
        if self._is_cached(file_path):
            logger.info(f"📋 Usando cache para: {file_path}")
            return self._get_cached_result(file_path)
        
        try:
            result = self.process_file(file_path)
            if result.get("success", False):
                self._cache_result(file_path, result)
            return result
        except Exception as e:
            logger.error(f"Error procesando {file_path}: {e}")
            return {"success": False, "error": str(e), "content": ""}
    
    def process_folder_parallel(self, folder_path: str) -> Dict[str, Any]:
        """Procesa una carpeta en paralelo para mayor velocidad"""
        folder_path = Path(folder_path)
        if not folder_path.exists():
            return {"success": False, "error": f"Carpeta no encontrada: {folder_path}"}
        
        files = []
        for ext in self.supported_extensions:
            files.extend(folder_path.glob(f"*{ext}"))
            files.extend(folder_path.glob(f"*{ext.upper()}"))
        
        # Procesar archivos en paralelo
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_file = {executor.submit(self.process_file_optimized, str(f)): f for f in files}
            
            for future in concurrent.futures.as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    result = future.result()
                    results[file.name] = result
                    if result.get("success"):
                        logger.info(f"✅ Procesado: {file.name}")
                    else:
                        logger.warning(f"⚠️ Error en: {file.name} - {result.get('error', 'Error desconocido')}")
                except Exception as e:
                    logger.error(f"❌ Error procesando {file.name}: {e}")
                    results[file.name] = {"success": False, "error": str(e), "content": ""}
        
        successful_files = sum(1 for r in results.values() if r.get("success", False))
        logger.info(f"📊 Procesados {len(results)} archivos, {successful_files} exitosos")
        
        return {
            "success": True,
            "files": results,
            "total_files": len(results),
            "successful_files": successful_files
        }
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Procesa un archivo y extrae su contenido de manera robusta"""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            file_size = os.path.getsize(file_path)
            
            # Procesar archivos de cualquier tamaño
            if file_size == 0:
                return {
                    "content": "ARCHIVO VACÍO",
                    "metadata": {
                        "file_path": file_path,
                        "file_name": os.path.basename(file_path),
                        "file_type": "empty",
                        "file_size": 0
                    }
                }
            
            # Si la extensión no está en la lista, intentar detectar el tipo
            if file_extension not in self.supported_extensions:
                file_extension = self._detect_file_type(file_path)
            
            content = ""
            metadata = {
                "file_path": file_path,
                "file_name": os.path.basename(file_path),
                "file_type": self.supported_extensions.get(file_extension, "unknown"),
                "file_size": file_size
            }
            
            # Procesar según el tipo de archivo
            if file_extension in ['.txt', '.md', '.log', '.dat', '.sql', '.py', '.js', '.java', '.cpp', '.c', '.h', '.ini', '.cfg', '.conf', '.properties']:
                content = self._read_text_file_robust(file_path)
            elif file_extension == '.pdf':
                content = self._read_pdf_file_enhanced(file_path)
            elif file_extension == '.docx':
                content = self._read_docx_file_enhanced(file_path)
            elif file_extension in ['.xlsx', '.xls']:
                try:
                    excel_result = self._read_excel_file_enhanced(file_path)
                    if isinstance(excel_result, dict) and excel_result.get("success"):
                        content = excel_result.get("content", "")
                        metadata.update(excel_result.get("metadata", {}))
                    else:
                        content = f"ERROR PROCESANDO EXCEL: {excel_result.get('error', 'Error desconocido') if isinstance(excel_result, dict) else str(excel_result)}"
                except Exception as excel_error:
                    # Manejo específico para errores de datetime
                    if "datetime.datetime found" in str(excel_error):
                        content = self._read_excel_with_datetime_fix(file_path)
                    else:
                        content = f"ERROR PROCESANDO EXCEL: {str(excel_error)}"
            elif file_extension == '.csv':
                content = self._read_csv_file_enhanced(file_path)
            elif file_extension == '.json':
                content = self._read_json_file(file_path)
            elif file_extension in ['.xml', '.html', '.htm']:
                content = self._read_xml_html_file(file_path)
            elif file_extension in ['.yaml', '.yml']:
                content = self._read_yaml_file(file_path)
            else:
                # Intentar leer como texto genérico
                content = self._read_text_file_robust(file_path)
            
            return {
                "content": content,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error procesando archivo {file_path}: {str(e)}")
            return {
                "content": f"ERROR PROCESANDO ARCHIVO: {str(e)}",
                "metadata": {
                    "file_path": file_path,
                    "file_name": os.path.basename(file_path),
                    "file_type": "error",
                    "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else 0
                }
            }
    
    def _detect_file_type(self, file_path: str) -> str:
        """Detecta el tipo de archivo basado en su contenido"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(1024)
                
            # Detectar por magic bytes
            if header.startswith(b'%PDF'):
                return '.pdf'
            elif header.startswith(b'PK'):
                return '.zip'  # DOCX es un ZIP
            elif header.startswith(b'\x89PNG'):
                return '.png'
            elif header.startswith(b'GIF'):
                return '.gif'
            elif header.startswith(b'\xff\xd8\xff'):
                return '.jpg'
            elif header.startswith(b'BM'):
                return '.bmp'
            else:
                # Intentar detectar encoding y leer como texto
                return '.txt'
        except:
            return '.txt'
    
    def _read_text_file_robust(self, file_path: str) -> str:
        """Lee archivos de texto con detección automática de encoding"""
        content = ""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16', 'ascii']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                    break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.warning(f"Error con encoding {encoding}: {str(e)}")
                continue
        
        if not content:
            # Si todos los encodings fallan, usar detección automática
            try:
                with open(file_path, 'rb') as file:
                    raw_data = file.read()
                    detected = chardet.detect(raw_data)
                    encoding = detected['encoding'] if detected['encoding'] else 'utf-8'
                
                content = raw_data.decode(encoding, errors='replace')
            except Exception as e:
                content = f"ERROR LEYENDO ARCHIVO: {str(e)}"
        
        return content
    
    def _read_pdf_file_enhanced(self, file_path: str) -> str:
        """Lee archivos PDF con información completa y mejorada"""
        content = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                content += f"=== ARCHIVO PDF: {os.path.basename(file_path)} ===\n"
                content += f"Total de páginas: {len(pdf_reader.pages)}\n"
                
                # Información del documento
                if pdf_reader.metadata:
                    content += "METADATOS DEL PDF:\n"
                    for key, value in pdf_reader.metadata.items():
                        if value:
                            content += f"- {key}: {value}\n"
                    content += "\n"
                
                # Extraer texto de todas las páginas
                for i, page in enumerate(pdf_reader.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text.strip():
                            content += f"--- PÁGINA {i} ---\n"
                            content += page_text + "\n\n"
                        else:
                            content += f"--- PÁGINA {i} (SIN TEXTO) ---\n"
                    except Exception as e:
                        content += f"--- PÁGINA {i} (ERROR: {str(e)}) ---\n"
                
                content += "="*50 + "\n\n"
        except Exception as e:
            logger.error(f"Error leyendo PDF {file_path}: {str(e)}")
            content = f"Error leyendo archivo PDF {file_path}: {str(e)}"
        return content
    
    def _read_docx_file_enhanced(self, file_path: str) -> str:
        """Lee archivos DOCX con información completa"""
        content = ""
        try:
            doc = Document(file_path)
            content += f"=== ARCHIVO DOCX: {os.path.basename(file_path)} ===\n"
            
            # Información del documento
            if doc.core_properties:
                content += "PROPIEDADES DEL DOCUMENTO:\n"
                if doc.core_properties.title:
                    content += f"- Título: {doc.core_properties.title}\n"
                if doc.core_properties.author:
                    content += f"- Autor: {doc.core_properties.author}\n"
                if doc.core_properties.subject:
                    content += f"- Asunto: {doc.core_properties.subject}\n"
                if doc.core_properties.created:
                    content += f"- Creado: {doc.core_properties.created}\n"
                if doc.core_properties.modified:
                    content += f"- Modificado: {doc.core_properties.modified}\n"
                content += "\n"
            
            # Contenido del documento
            content += "CONTENIDO DEL DOCUMENTO:\n"
            for i, paragraph in enumerate(doc.paragraphs, 1):
                if paragraph.text.strip():
                    content += f"{i}. {paragraph.text}\n"
            
            # Tablas
            if doc.tables:
                content += "\nTABLAS EN EL DOCUMENTO:\n"
                for table_idx, table in enumerate(doc.tables, 1):
                    content += f"\n--- TABLA {table_idx} ---\n"
                    for row_idx, row in enumerate(table.rows):
                        row_data = []
                        for cell in row.cells:
                            row_data.append(cell.text.strip())
                        content += f"Fila {row_idx + 1}: {' | '.join(row_data)}\n"
            
            content += "\n" + "="*50 + "\n\n"
        except Exception as e:
            logger.error(f"Error leyendo DOCX {file_path}: {str(e)}")
            content = f"Error leyendo archivo DOCX {file_path}: {str(e)}"
        return content
    
    def _read_excel_file_enhanced(self, file_path: str) -> Dict[str, Any]:
        """Lee archivos Excel con extracción universal y sin límites"""
        try:
            # Intentar diferentes engines para mayor compatibilidad
            df = None
            engines_to_try = ['openpyxl', 'xlrd', 'odf']
            
            for engine in engines_to_try:
                try:
                    # Configuración específica para evitar errores de datetime
                    if engine == 'openpyxl':
                        df = pd.read_excel(file_path, engine=engine, parse_dates=False, keep_default_na=False)
                    else:
                        df = pd.read_excel(file_path, engine=engine, keep_default_na=False)
                    logger.info(f"Archivo {file_path} leído exitosamente con engine: {engine}")
                    break
                except Exception as e:
                    logger.warning(f"Engine {engine} falló para {file_path}: {e}")
                    continue
            
            if df is None:
                # Si ningún engine funciona, intentar leer como CSV
                try:
                    df = pd.read_csv(file_path, keep_default_na=False)
                    logger.info(f"Archivo {file_path} leído como CSV")
                except:
                    return {"success": False, "error": f"No se pudo leer el archivo con ningún método", "content": ""}
            
            # Convertir DataFrame a texto estructurado universal
            content_parts = []
            content_parts.append(f"ARCHIVO: {os.path.basename(file_path)}")
            content_parts.append(f"TOTAL DE REGISTROS: {len(df)}")
            content_parts.append(f"COLUMNAS: {', '.join(df.columns.tolist())}")
            content_parts.append("")
            content_parts.append("DATOS COMPLETOS:")
            content_parts.append("=" * 50)
            
            # Procesar cada fila de manera segura
            for index, row in df.iterrows():
                try:
                    row_text = f"REGISTRO {index + 1}:"
                    for col in df.columns:
                        try:
                            value = row[col]
                            # Manejar todos los tipos de datos de forma segura
                            if pd.isna(value) or value == '' or value is None:
                                value_str = "N/A"
                            elif isinstance(value, (pd.Timestamp, datetime)):
                                value_str = value.strftime("%d/%m/%Y")
                            elif isinstance(value, (int, float)):
                                value_str = str(value)
                            elif isinstance(value, bool):
                                value_str = "Sí" if value else "No"
                            else:
                                value_str = str(value)
                            row_text += f" {col}={value_str} |"
                        except Exception as cell_error:
                            # Si hay error con una celda específica, continuar
                            row_text += f" {col}=ERROR |"
                            continue
                    content_parts.append(row_text)
                except Exception as row_error:
                    # Si hay error con una fila completa, continuar
                    content_parts.append(f"REGISTRO {index + 1}: ERROR PROCESANDO FILA")
                    continue
            
            # Agregar estadísticas básicas de manera segura
            content_parts.append("")
            content_parts.append("ESTADÍSTICAS:")
            content_parts.append("=" * 30)
            
            for col in df.columns:
                try:
                    if df[col].dtype in ['int64', 'float64']:
                        if not df[col].isna().all():
                            min_val = df[col].min()
                            max_val = df[col].max()
                            mean_val = df[col].mean()
                            # Convertir a string de manera segura
                            min_str = str(min_val) if not pd.isna(min_val) else "N/A"
                            max_str = str(max_val) if not pd.isna(max_val) else "N/A"
                            mean_str = f"{mean_val:.2f}" if not pd.isna(mean_val) else "N/A"
                            content_parts.append(f"  {col}: min={min_str}, max={max_str}, promedio={mean_str}")
                    else:
                        unique_count = df[col].nunique()
                        content_parts.append(f"  {col}: {unique_count} valores únicos")
                except Exception as e:
                    content_parts.append(f"  {col}: No se pudieron calcular estadísticas (error: {str(e)})")
            
            content = "\n".join(content_parts)
            
            return {
                "success": True,
                "content": content,
                "metadata": {
                    "file_name": os.path.basename(file_path),
                    "file_type": "excel",
                    "file_size": os.path.getsize(file_path),
                    "rows": df.shape[0],
                    "columns": df.shape[1],
                    "column_names": df.columns.tolist()
                }
            }
            
        except Exception as e:
            logger.error(f"Error leyendo Excel {file_path}: {e}")
            # Intentar leer como archivo de texto como último recurso
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    "success": True,
                    "content": f"ARCHIVO: {os.path.basename(file_path)}\nCONTENIDO COMO TEXTO:\n{content}",
                    "metadata": {
                        "file_name": os.path.basename(file_path),
                        "file_type": "text",
                        "file_size": os.path.getsize(file_path)
                    }
                }
            except:
                return {"success": False, "error": str(e), "content": ""}
    
    def _read_csv_file_enhanced(self, file_path: str) -> str:
        """Lee archivos CSV con análisis completo"""
        content = ""
        try:
            # Detectar encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read(1024)
                detected = chardet.detect(raw_data)
                encoding = detected['encoding'] if detected['encoding'] else 'utf-8'
            
            # Intentar diferentes delimitadores
            delimiters = [',', ';', '\t', '|', ' ']
            df = None
            
            for delimiter in delimiters:
                try:
                    df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)
                    break
                except Exception:
                    continue
            
            if df is None:
                content = f"Error: No se pudo leer el archivo CSV {file_path}"
                return content
            
            content += f"=== ARCHIVO CSV: {os.path.basename(file_path)} ===\n"
            content += f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas\n"
            content += f"Columnas: {', '.join([str(col) for col in df.columns.tolist()])}\n\n"
            
            # Información detallada
            content += "INFORMACIÓN DETALLADA:\n"
            for col in df.columns:
                dtype = str(df[col].dtype)
                non_null = df[col].count()
                null_count = df[col].isnull().sum()
                content += f"- {col}: {dtype} (No nulos: {non_null}, Nulos: {null_count})\n"
            content += "\n"
            
            # Mostrar datos
            content += "DATOS COMPLETOS:\n"
            try:
                if len(df) > 100:
                    content += "PRIMERAS 50 FILAS:\n"
                    content += df.head(50).to_string(index=False) + "\n\n"
                    content += "ÚLTIMAS 50 FILAS:\n"
                    content += df.tail(50).to_string(index=False) + "\n\n"
                else:
                    content += df.to_string(index=False) + "\n\n"
            except Exception as e:
                content += f"Error mostrando datos: {str(e)}\n\n"
            
            # Análisis estadístico
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                content += "ANÁLISIS ESTADÍSTICO:\n"
                try:
                    content += df[numeric_cols].describe().to_string() + "\n\n"
                except Exception as e:
                    content += f"Error en análisis estadístico: {str(e)}\n\n"
            
            content += "="*50 + "\n\n"
            
        except Exception as e:
            logger.error(f"Error leyendo CSV {file_path}: {str(e)}")
            content = f"Error leyendo archivo CSV {file_path}: {str(e)}"
        return content
    
    def _read_json_file(self, file_path: str) -> str:
        """Lee archivos JSON"""
        content = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                content += f"=== ARCHIVO JSON: {os.path.basename(file_path)} ===\n"
                content += json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error leyendo JSON {file_path}: {str(e)}")
            content = f"Error leyendo archivo JSON {file_path}: {str(e)}"
        return content
    
    def _read_xml_html_file(self, file_path: str) -> str:
        """Lee archivos XML y HTML"""
        content = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except Exception as e:
            logger.error(f"Error leyendo XML/HTML {file_path}: {str(e)}")
            content = f"Error leyendo archivo XML/HTML {file_path}: {str(e)}"
        return content
    
    def _read_yaml_file(self, file_path: str) -> str:
        """Lee archivos YAML"""
        content = ""
        try:
            import yaml
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                content += f"=== ARCHIVO YAML: {os.path.basename(file_path)} ===\n"
                content += yaml.dump(data, default_flow_style=False, allow_unicode=True)
        except ImportError:
            content = f"Error: PyYAML no está instalado para leer archivos YAML"
        except Exception as e:
            logger.error(f"Error leyendo YAML {file_path}: {str(e)}")
            content = f"Error leyendo archivo YAML {file_path}: {str(e)}"
        return content
    
    def _read_excel_with_datetime_fix(self, file_path: str) -> str:
        """Lee archivos Excel con corrección específica para errores de datetime"""
        try:
            import openpyxl
            from openpyxl import load_workbook
            
            # Cargar el archivo con openpyxl directamente
            wb = load_workbook(filename=file_path, data_only=True)
            ws = wb.active
            
            content_parts = []
            content_parts.append(f"ARCHIVO: {os.path.basename(file_path)}")
            content_parts.append("LECTURA CON CORRECCIÓN DE DATETIME")
            content_parts.append("=" * 50)
            
            # Procesar fila por fila manualmente
            for row_idx, row in enumerate(ws.iter_rows(values_only=True), 1):
                if row_idx == 1:  # Primera fila (encabezados)
                    headers = []
                    for cell_value in row:
                        if cell_value is None:
                            headers.append("Columna_Vacia")
                        else:
                            headers.append(str(cell_value))
                    content_parts.append(f"ENCABEZADOS: {' | '.join(headers)}")
                    content_parts.append("")
                    content_parts.append("DATOS COMPLETOS:")
                    content_parts.append("=" * 30)
                else:
                    row_text = f"REGISTRO {row_idx}:"
                    for col_idx, cell_value in enumerate(row):
                        col_name = headers[col_idx] if col_idx < len(headers) else f"Col{col_idx+1}"
                        
                        # Manejar valores de celda de forma segura
                        if cell_value is None:
                            value_str = "N/A"
                        elif isinstance(cell_value, (pd.Timestamp, datetime)):
                            value_str = cell_value.strftime("%d/%m/%Y")
                        elif isinstance(cell_value, (int, float)):
                            value_str = str(cell_value)
                        elif isinstance(cell_value, bool):
                            value_str = "Sí" if cell_value else "No"
                        else:
                            value_str = str(cell_value)
                        
                        row_text += f" {col_name}={value_str} |"
                    
                    content_parts.append(row_text)
            
            content = "\n".join(content_parts)
            return content
            
        except Exception as e:
            logger.error(f"Error en corrección datetime para {file_path}: {e}")
            return f"ERROR EN CORRECCIÓN DATETIME: {str(e)}"
    
    def process_folder(self, folder_path: str) -> List[Dict[str, Any]]:
        """Procesa todos los archivos en una carpeta de manera robusta"""
        documents = []
        
        if not os.path.exists(folder_path):
            logger.warning(f"La carpeta {folder_path} no existe")
            return documents
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1].lower()
                
                # Procesar cualquier archivo, incluso si no está en la lista de soportados
                logger.info(f"Procesando: {file_path}")
                document = self.process_file(file_path)
                if document and document.get("content"):
                    documents.append(document)
        
        logger.info(f"Procesados {len(documents)} documentos")
        return documents
