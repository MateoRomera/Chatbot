# backend/src/common.py
import re, unicodedata


def norm(s: str) -> str:
    """Min-normalizador: quita tildes/puntuación, minúsculas y colapsa espacios."""
    if s is None:
        return ""
    s = str(s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# Aliases/sinónimos canónicos
FORCE_ALIASES = {
    "ejercito": "Ejército",
    "ejer": "Ejército",
    "fuerza aerea": "Fuerza Aérea",
    "faa": "Fuerza Aérea",
    "aerea": "Fuerza Aérea",
    "armada": "Armada",
    "marina": "Armada",
}

REGION_SYNONYMS = {
    "noa": "NOA",
    "nea": "NEA",
    "patagonia": "Patagonia",
    "cuyo": "Cuyo",
    "centro": "Centro",
}

PROV_ALIASES = {
    "caba": "Ciudad Autónoma de Buenos Aires",
    "capital federal": "Ciudad Autónoma de Buenos Aires",
    "ciudad autonoma de buenos aires": "Ciudad Autónoma de Buenos Aires",
    "buenos aires": "Buenos Aires",
    "rio negro": "Río Negro",
    "tierradel fuego": "Tierra del Fuego",
    "tierra del fuego": "Tierra del Fuego",
    # el resto se resuelve por coincidencia directa con el catálogo
}

SPECIALTY_ALIASES = {
    "sanidad": "Sanidad",
    "medico": "Médico",
    "logistica": "Logística",
    "ingeniero": "Ingeniero",
    "inteligencia": "Inteligencia",
    "comunicaciones": "Comunicaciones",
    "infanteria": "Infantería",
    "artilleria": "Artillería",
    "caballeria": "Caballería",
    "piloto": "Piloto",
}

STUDY_ALIASES = {
    "medicina": "Medicina",
    "psicologia": "Psicología",
    "informatica": "Informática",
    "ingenieria": "Ingeniería",
    "historia": "Historia",
    "geografia": "Geografía",
    "derecho": "Derecho",
    "administracion": "Administración",
    "contabilidad": "Contabilidad",
    "relaciones internacionales": "Relaciones Internacionales",
}

RANK_ALIASES = {
    "sargento": "Sargento",
    "suboficial": "Suboficial",
    "teniente": "Teniente",
    "coronel": "Coronel",
    "capitan": "Capitán",
    "mayor": "Mayor",
}
