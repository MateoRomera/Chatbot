from __future__ import annotations
from typing import List, Dict
import pandas as pd

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import linear_kernel

    SK_AVAIL = True
except Exception:
    SK_AVAIL = False


class SimpleRAG:
    def __init__(self):
        self.vec = None
        self.mat = None
        self.df = None

    def build(self, df: pd.DataFrame):
        if not SK_AVAIL:
            return
        self.df = df
        docs = (
            df["Nombre completo"].fillna("")
            + " | "
            + df["Fuerza"].fillna("")
            + " | "
            + df["Región"].fillna("")
            + " | "
            + df["Provincia"].fillna("")
            + " | "
            + df["Especialidad"].fillna("")
            + " | "
            + df["Formación universitaria"].fillna("")
        )
        self.vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        self.mat = self.vec.fit_transform(docs)

    def search(self, query: str, k: int = 5) -> List[Dict]:
        if not SK_AVAIL or self.mat is None:
            return []
        q = self.vec.transform([query])
        sims = linear_kernel(q, self.mat).ravel()
        top = sims.argsort()[-k:][::-1]
        rows = self.df.iloc[top][
            [
                "Nombre completo",
                "Fuerza",
                "Región",
                "Provincia",
                "Especialidad",
                "Formación universitaria",
            ]
        ]
        return rows.to_dict(orient="records")


RAG = SimpleRAG()
