from __future__ import annotations

from collections import Counter

from .retrieval import RetrievedItem


def similarity_to_confidence(similarity: float) -> str:
    if similarity >= 0.5:
        return "high"
    if similarity >= 0.25:
        return "medium"
    return "low"


def generate_comment(question: str, retrieved_items: list[RetrievedItem], interpretation_lines: list[str]) -> dict:
    case_hits = [item for item in retrieved_items if item.source_type == "case"]
    knowledge_hits = [item for item in retrieved_items if item.source_type == "knowledge"]
    primary_case = case_hits[0].payload if case_hits else None
    best_similarity = retrieved_items[0].similarity if retrieved_items else 0.0

    scenario_counter = Counter()
    for item in case_hits[:3]:
        scenario_counter.update([item.payload["scenario"]])

    comment = " ".join(interpretation_lines)
    if not comment:
        comment = "Reviewed analytes are within or close to the expected reference range in this simplified rule set."
    if primary_case:
        comment += f" Similar retrieved case comment: {primary_case['comment']}"

    review_note = "Clinical review is required before sign-off."
    if knowledge_hits:
        review_note += " Supporting knowledge snippets were retrieved for wording consistency."

    return {
        "question": question,
        "confidence": similarity_to_confidence(best_similarity),
        "best_similarity": round(best_similarity, 4),
        "draft_comment": comment,
        "suggested_patterns": [label for label, _ in scenario_counter.most_common(3)],
        "reference_case_ids": [item.source_id for item in case_hits[:3]],
        "recommendation": review_note,
        "evidence": [
            {
                "source_type": item.source_type,
                "source_id": item.source_id,
                "title": item.title,
                "similarity": round(item.similarity, 4),
            }
            for item in retrieved_items
        ],
    }
