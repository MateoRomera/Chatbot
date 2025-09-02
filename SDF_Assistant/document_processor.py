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
    """Procesador de documentos optimizado para SDF con soporte para Excel, PDF y CSV"""

    def __init__(self):
        self.supported_extensions = Config.SUPPORTED_EXTENSIONS
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

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Procesa un archivo individual"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {"success": False, "error": f"Archivo no encontrado: {file_path}"}

            file_extension = file_path.suffix.lower()
            file_type = self.supported_extensions.get(
                file_extension, "unknown")

            logger.info(f"📄 Procesando: {file_path.name} ({file_type})")

            if file_type == "pdf":
                return self._process_pdf(file_path)
            elif file_type == "excel":
                return self._process_excel(file_path)
            elif file_type == "csv":
                return self._process_csv(file_path)
            elif file_type == "word":
                return self._process_word(file_path)
            elif file_type == "text":
                return self._process_text(file_path)
            else:
                return self._process_text(file_path)

        except Exception as e:
            logger.error(f"Error procesando {file_path}: {e}")
            return {"success": False, "error": str(e), "content": ""}

    def _process_pdf(self, file_path: Path) -> Dict[str, Any]:
        """Procesa archivos PDF"""
        try:
            content = []
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        content.append(f"Página {page_num + 1}: {text}")

            return {
                "success": True,
                "content": "\n".join(content),
                "metadata": {
                    "file_name": file_path.name,
                    "file_type": "pdf",
                    "pages": len(content),
                    "file_size": file_path.stat().st_size
                }
            }
        except Exception as e:
            return {"success": False, "error": f"Error procesando PDF: {e}"}

    def _process_excel(self, file_path: Path) -> Dict[str, Any]:
        """Procesa archivos Excel"""
        try:
            content = []

            # Intentar diferentes motores de Excel
            engines = ['openpyxl', 'xlrd', 'odf']
            excel_file = None

            for engine in engines:
                try:
                    excel_file = pd.ExcelFile(file_path, engine=engine)
                    break
                except Exception:
                    continue

            if excel_file is None:
                return {"success": False, "error": "No se pudo abrir el archivo Excel con ningún motor disponible"}

            for sheet_name in excel_file.sheet_names:
                try:
                    df = pd.read_excel(
                        file_path, sheet_name=sheet_name, engine=excel_file.engine)
                    if not df.empty:
                        content.append(f"Hoja: {sheet_name}")
                        content.append(
                            f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
                        content.append("Columnas: " + ", ".join(str(col)
                                       for col in df.columns.tolist()))
                        content.append("Datos completos:")

                        # Convertir todas las columnas a string para evitar errores de datetime
                        df_display = df.astype(str)
                        content.append(df_display.to_string())
                        content.append("\n" + "="*50 + "\n")
                except Exception as e:
                    content.append(
                        f"Error procesando hoja {sheet_name}: {str(e)}")
                    continue

            return {
                "success": True,
                "content": "\n".join(content),
                "metadata": {
                    "file_name": file_path.name,
                    "file_type": "excel",
                    "sheets": len(excel_file.sheet_names),
                    "file_size": file_path.stat().st_size
                }
            }
        except Exception as e:
            return {"success": False, "error": f"Error procesando Excel: {e}"}

    def _process_csv(self, file_path: Path) -> Dict[str, Any]:
        """Procesa archivos CSV"""
        try:
            # Detectar encoding
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                detected = chardet.detect(raw_data)
                encoding = detected['encoding'] or 'utf-8'

            # Leer CSV
            df = pd.read_csv(file_path, encoding=encoding)

            content = []
            content.append(f"Archivo CSV: {file_path.name}")
            content.append(
                f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
            content.append("Columnas: " + ", ".join(df.columns.tolist()))
            content.append("Tipos de datos:")
            for col, dtype in df.dtypes.items():
                content.append(f"  {col}: {dtype}")
            content.append("\nDatos completos:")
            content.append(df.to_string())

            # Información estadística básica
            content.append("\nInformación estadística:")
            content.append(df.describe().to_string())

            return {
                "success": True,
                "content": "\n".join(content),
                "metadata": {
                    "file_name": file_path.name,
                    "file_type": "csv",
                    "rows": df.shape[0],
                    "columns": df.shape[1],
                    "encoding": encoding,
                    "file_size": file_path.stat().st_size
                }
            }
        except Exception as e:
            return {"success": False, "error": f"Error procesando CSV: {e}"}

    def _process_word(self, file_path: Path) -> Dict[str, Any]:
        """Procesa archivos Word"""
        try:
            doc = Document(file_path)
            content = []

            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    content.append(paragraph.text)

            return {
                "success": True,
                "content": "\n".join(content),
                "metadata": {
                    "file_name": file_path.name,
                    "file_type": "word",
                    "paragraphs": len(content),
                    "file_size": file_path.stat().st_size
                }
            }
        except Exception as e:
            return {"success": False, "error": f"Error procesando Word: {e}"}

    def _process_text(self, file_path: Path) -> Dict[str, Any]:
        """Procesa archivos de texto"""
        try:
            # Detectar encoding
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                detected = chardet.detect(raw_data)
                encoding = detected['encoding'] or 'utf-8'

            # Intentar diferentes encodings si falla el detectado
            encodings_to_try = [encoding, 'utf-8',
                                'latin-1', 'cp1252', 'iso-8859-1']
            content = None

            for enc in encodings_to_try:
                try:
                    with open(file_path, 'r', encoding=enc) as file:
                        content = file.read()
                    encoding = enc
                    break
                except UnicodeDecodeError:
                    continue

            if content is None:
                # Último recurso: leer como bytes y decodificar con errors='ignore'
                with open(file_path, 'rb') as file:
                    raw_data = file.read()
                content = raw_data.decode('utf-8', errors='ignore')
                encoding = 'utf-8 (con errores ignorados)'

            return {
                "success": True,
                "content": content,
                "metadata": {
                    "file_name": file_path.name,
                    "file_type": "text",
                    "encoding": encoding,
                    "file_size": file_path.stat().st_size
                }
            }
        except Exception as e:
            return {"success": False, "error": f"Error procesando texto: {e}"}

    def process_folder(self, folder_path: str) -> List[Dict[str, Any]]:
        """Procesa todos los archivos en una carpeta"""
        folder_path = Path(folder_path)
        if not folder_path.exists():
            logger.error(f"Carpeta no encontrada: {folder_path}")
            return []

        documents = []
        files = []

        # Recopilar archivos soportados
        for ext in self.supported_extensions:
            files.extend(folder_path.glob(f"*{ext}"))
            files.extend(folder_path.glob(f"*{ext.upper()}"))

        logger.info(f"📁 Encontrados {len(files)} archivos en {folder_path}")

        # Procesar archivos en paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=Config.MAX_WORKERS) as executor:
            future_to_file = {executor.submit(
                self.process_file, str(f)): f for f in files}

            for future in concurrent.futures.as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    result = future.result()
                    if result.get("success", False):
                        documents.append(result)
                        logger.info(f"✅ Procesado: {file.name}")
                    else:
                        logger.warning(
                            f"❌ Error en {file.name}: {result.get('error', 'Error desconocido')}")
                except Exception as e:
                    logger.error(f"Error procesando {file}: {e}")

        logger.info(f"📊 Total de documentos procesados: {len(documents)}")
        return documents

    def get_document_summary(self, folder_path: str) -> Dict[str, Any]:
        """Obtiene un resumen de los documentos en la carpeta"""
        documents = self.process_folder(folder_path)

        summary = {
            "total_documents": len(documents),
            "by_type": {},
            "total_size": 0,
            "documents": []
        }

        for doc in documents:
            file_type = doc["metadata"]["file_type"]
            file_size = doc["metadata"]["file_size"]

            if file_type not in summary["by_type"]:
                summary["by_type"][file_type] = 0
            summary["by_type"][file_type] += 1
            summary["total_size"] += file_size

            summary["documents"].append({
                "name": doc["metadata"]["file_name"],
                "type": file_type,
                "size": file_size,
                "success": doc["success"]
            })

        return summary
