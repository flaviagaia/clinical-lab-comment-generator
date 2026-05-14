from __future__ import annotations

from pathlib import Path

from .clinical_logic import (
    interpret_cbc,
    interpret_diabetes,
    interpret_inflammation,
    interpret_kidney,
    interpret_lipids,
    interpret_liver,
)
from .data_factory import build_case_corpus, build_knowledge_base, write_public_dataset_reference
from .generation import generate_comment
from .retrieval import ClinicalLabRetriever


class ClinicalLabCommentGeneratorPipeline:
    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root = Path(project_root or Path(__file__).resolve().parents[1])
        self.case_corpus = build_case_corpus()
        self.knowledge_base = build_knowledge_base()
        self.retriever = ClinicalLabRetriever(self.case_corpus, self.knowledge_base)
        self.dataset_reference_path = write_public_dataset_reference(self.project_root / "data" / "raw")

    def run(
        self,
        hemoglobin_g_dl: float,
        wbc_k_ul: float,
        platelets_k_ul: float,
        creatinine_mg_dl: float,
        egfr_ml_min: float,
        alt_u_l: float,
        ast_u_l: float,
        a1c_percent: float,
        glucose_mg_dl: float,
        ldl_mg_dl: float,
        triglycerides_mg_dl: float,
        crp_mg_l: float,
        clinical_context: str = "",
        top_k: int = 5,
    ) -> dict:
        self._validate_inputs(
            hemoglobin_g_dl=hemoglobin_g_dl,
            wbc_k_ul=wbc_k_ul,
            platelets_k_ul=platelets_k_ul,
            creatinine_mg_dl=creatinine_mg_dl,
            egfr_ml_min=egfr_ml_min,
            alt_u_l=alt_u_l,
            ast_u_l=ast_u_l,
            a1c_percent=a1c_percent,
            glucose_mg_dl=glucose_mg_dl,
            ldl_mg_dl=ldl_mg_dl,
            triglycerides_mg_dl=triglycerides_mg_dl,
            crp_mg_l=crp_mg_l,
        )

        interpretation_lines: list[str] = []
        interpretation_lines.extend(interpret_cbc(hemoglobin_g_dl, wbc_k_ul, platelets_k_ul))
        interpretation_lines.extend(interpret_kidney(creatinine_mg_dl, egfr_ml_min))
        interpretation_lines.extend(interpret_liver(alt_u_l, ast_u_l))
        interpretation_lines.extend(interpret_diabetes(a1c_percent, glucose_mg_dl))
        interpretation_lines.extend(interpret_lipids(ldl_mg_dl, triglycerides_mg_dl))
        interpretation_lines.extend(interpret_inflammation(crp_mg_l))

        question = "Generate a concise clinical laboratory comment."
        structured_terms = [
            clinical_context,
            f"hemoglobin {hemoglobin_g_dl}",
            f"wbc {wbc_k_ul}",
            f"platelets {platelets_k_ul}",
            f"creatinine {creatinine_mg_dl}",
            f"egfr {egfr_ml_min}",
            f"alt {alt_u_l}",
            f"ast {ast_u_l}",
            f"a1c {a1c_percent}",
            f"glucose {glucose_mg_dl}",
            f"ldl {ldl_mg_dl}",
            f"triglycerides {triglycerides_mg_dl}",
            f"crp {crp_mg_l}",
        ]
        retrieved = self.retriever.search(question=question, structured_terms=structured_terms, top_k=top_k)
        generated = generate_comment(question=question, retrieved_items=retrieved, interpretation_lines=interpretation_lines)
        return {
            "dataset_source": "nhanes_style_local_sample",
            "public_dataset_reference": str(self.dataset_reference_path),
            "case_count": len(self.case_corpus),
            "knowledge_doc_count": len(self.knowledge_base),
            "retrieved_count": len(retrieved),
            **generated,
        }

    @staticmethod
    def _validate_inputs(**values: float) -> None:
        allowed_ranges = {
            "hemoglobin_g_dl": (0.0, 25.0),
            "wbc_k_ul": (0.0, 100.0),
            "platelets_k_ul": (0.0, 2000.0),
            "creatinine_mg_dl": (0.0, 20.0),
            "egfr_ml_min": (0.0, 200.0),
            "alt_u_l": (0.0, 5000.0),
            "ast_u_l": (0.0, 5000.0),
            "a1c_percent": (0.0, 20.0),
            "glucose_mg_dl": (0.0, 1000.0),
            "ldl_mg_dl": (0.0, 500.0),
            "triglycerides_mg_dl": (0.0, 5000.0),
            "crp_mg_l": (0.0, 500.0),
        }
        for name, value in values.items():
            low, high = allowed_ranges[name]
            if not low <= value <= high:
                raise ValueError(f"Invalid value for {name}: expected between {low} and {high}, got {value}.")
