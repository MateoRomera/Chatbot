# backend/src/slm_parser.py
import re
from .common import (
    norm,
    FORCE_ALIASES,
    REGION_SYNONYMS,
    PROV_ALIASES,
    SPECIALTY_ALIASES,
    STUDY_ALIASES,
    RANK_ALIASES,
)

STOP = {"en", "de", "del", "la", "las", "los", "con", "y", "o", "a", "al", "el"}


def _index_catalog(catalog: dict):
    """Mapeos normalizados -> canónicos para provincias y catálogos abiertos."""
    prov_map = {}
    for it in catalog.get("Provincia", []):
        v = it.get("Provincia") or ""
        prov_map[norm(v)] = v
    # también aceptar alias manuales
    for k, v in PROV_ALIASES.items():
        prov_map[norm(k)] = v

    study_map = {
        norm(i.get("Formación universitaria", "")): i.get("Formación universitaria", "")
        for i in catalog.get("Formación universitaria", [])
    }
    spec_map = {
        norm(i.get("Especialidad", "")): i.get("Especialidad", "")
        for i in catalog.get("Especialidad", [])
    }
    rank_map = {
        norm(i): i
        for i in ["Sargento", "Suboficial", "Teniente", "Coronel", "Capitán", "Mayor"]
    }

    return prov_map, study_map, spec_map, rank_map


def parse_free(text: str, catalog: dict) -> dict:
    """Convierte lenguaje natural en filtros canónicos, robusto a tildes y errores simples."""
    t = norm(text)
    filters = {}

    # DNI suelto
    m = re.search(r"\b(\d{7,9})\b", t)
    if m:
        filters["DNI"] = m.group(1)
        return filters  # corto circuito: búsqueda por DNI debe ser exacta

    prov_map, study_map, spec_map, rank_map = _index_catalog(catalog)

    # Fuerza
    tt = f" {t} "
    for k, canon in FORCE_ALIASES.items():
        if f" {k} " in tt:
            filters["Fuerza"] = canon
            break

    # Región
    for k, canon in REGION_SYNONYMS.items():
        if f" {k} " in tt:
            filters["Región"] = canon
            break

    # Provincia (por catálogo + alias)
    for key, canon in prov_map.items():
        if f" {key} " in tt:
            filters["Provincia"] = canon
            break

    # Especialidad
    for k, canon in {**SPECIALTY_ALIASES, **spec_map}.items():
        if f" {k} " in tt:
            filters["Especialidad"] = canon
            break

    # Formación universitaria
    for k, canon in {**STUDY_ALIASES, **study_map}.items():
        if f" {k} " in tt:
            filters["Formación universitaria"] = canon
            break

    # Grado o Rango
    for k, canon in {**RANK_ALIASES, **rank_map}.items():
        if f" {k} " in tt:
            filters["Grado o Rango"] = canon
            break

    # Nombre (contiene): cualquier token sobrado (>=4 letras) que exista en algún nombre
    if "Nombre completo__contains" not in filters:
        tokens = [w for w in t.split() if w not in STOP and len(w) >= 4]
        if tokens:
            filters["Nombre completo__contains"] = tokens[0]

    return filters
