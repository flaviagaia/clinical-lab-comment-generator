from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class RetrievedItem:
    source_type: str
    source_id: str
    title: str
    similarity: float
    payload: dict


class ClinicalLabRetriever:
    def __init__(self, cases: list[dict], knowledge_docs: list[dict]) -> None:
        self.documents = self._build_documents(cases, knowledge_docs)
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([doc["search_text"] for doc in self.documents])

    @staticmethod
    def _build_documents(cases: list[dict], knowledge_docs: list[dict]) -> list[dict]:
        documents: list[dict] = []
        for case in cases:
            search_text = " ".join(str(value) for value in case.values())
            documents.append(
                {
                    "source_type": "case",
                    "source_id": case["case_id"],
                    "title": case["scenario"],
                    "payload": case,
                    "search_text": search_text,
                }
            )
        for doc in knowledge_docs:
            documents.append(
                {
                    "source_type": "knowledge",
                    "source_id": doc["doc_id"],
                    "title": doc["title"],
                    "payload": doc,
                    "search_text": f'{doc["title"]} {doc["category"]} {doc["content"]}',
                }
            )
        return documents

    def search(self, question: str, structured_terms: Iterable[str] | None = None, top_k: int = 5) -> list[RetrievedItem]:
        query = " ".join([question] + list(structured_terms or []))
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.matrix)[0]
        top_indices = similarities.argsort()[::-1][:top_k]
        return [
            RetrievedItem(
                source_type=self.documents[idx]["source_type"],
                source_id=self.documents[idx]["source_id"],
                title=self.documents[idx]["title"],
                similarity=float(similarities[idx]),
                payload=self.documents[idx]["payload"],
            )
            for idx in top_indices
        ]
