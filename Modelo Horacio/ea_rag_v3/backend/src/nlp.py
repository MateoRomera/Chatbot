from __future__ import annotations
import re, unicodedata
from rapidfuzz import process, fuzz


def norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


FORCE_ALIASES = {
    "ejercito": "Ejército",
    "ejercito argentino": "Ejército",
    "ejrcito": "Ejército",
    "armada": "Armada",
    "marina": "Armada",
    "fuerza aerea": "Fuerza Aérea",
    "aerea": "Fuerza Aérea",
    "faa": "Fuerza Aérea",
}
REGION_VALS = ["NOA", "NEA", "Centro", "Cuyo", "Patagonia"]


def best_match(text: str, candidates: list[str], score_cutoff=80) -> str | None:
    if not text or not candidates:
        return None
    cand = process.extractOne(
        text, candidates, scorer=fuzz.token_sort_ratio, score_cutoff=score_cutoff
    )
    return cand[0] if cand else None


def parse_dni(text: str) -> str | None:
    m = re.search(r"\b(\d{7,8})\b", text.replace(".", "").replace(",", ""))
    return m.group(1) if m else None


def find_force(text_n: str) -> str | None:
    for k, v in FORCE_ALIASES.items():
        if k in text_n:
            return v
    return None


def find_region(text_n: str) -> str | None:
    for r in REGION_VALS:
        if norm(r) in text_n:
            return r
    return None
