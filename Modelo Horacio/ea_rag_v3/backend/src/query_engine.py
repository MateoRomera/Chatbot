from __future__ import annotations
import pandas as pd
from .config import CANON, MAX_PREVIEW_ROWS


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    out = df
    for k, v in (filters or {}).items():
        if k.endswith("__contains"):
            col = k.split("__", 1)[0]
            out = out[out[col].str.contains(str(v), case=False, na=False)]
        else:
            out = out[out[k].astype(str).str.lower() == str(v).lower()]
    return out


def preview(df: pd.DataFrame) -> pd.DataFrame:
    # Pediste: sin columna de origen; y con columnas de Especialidad y Formación visibles
    cols = [c for c in CANON if c in df.columns]
    show = df[cols].head(MAX_PREVIEW_ROWS).copy()
    return show
