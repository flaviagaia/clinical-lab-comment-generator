from __future__ import annotations

import unittest

from src.clinical_logic import interpret_diabetes, interpret_kidney
from src.pipeline import ClinicalLabCommentGeneratorPipeline


class ClinicalLabCommentGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.pipeline = ClinicalLabCommentGeneratorPipeline()

    def test_diabetes_interpretation(self) -> None:
        comments = interpret_diabetes(8.1, 150.0)
        self.assertTrue(any("diabetes range" in comment.lower() for comment in comments))

    def test_kidney_interpretation(self) -> None:
        comments = interpret_kidney(1.7, 45.0)
        self.assertTrue(any("creatinine" in comment.lower() for comment in comments))
        self.assertTrue(any("filtration" in comment.lower() for comment in comments))

    def test_pipeline_returns_lab_comment(self) -> None:
        result = self.pipeline.run(
            hemoglobin_g_dl=13.2,
            wbc_k_ul=7.4,
            platelets_k_ul=250.0,
            creatinine_mg_dl=1.8,
            egfr_ml_min=46.0,
            alt_u_l=32.0,
            ast_u_l=29.0,
            a1c_percent=8.0,
            glucose_mg_dl=162.0,
            ldl_mg_dl=140.0,
            triglycerides_mg_dl=188.0,
            crp_mg_l=4.2,
            clinical_context="Outpatient diabetes follow-up.",
        )
        self.assertGreaterEqual(result["retrieved_count"], 1)
        self.assertIn("diabetes", result["draft_comment"].lower())
        self.assertIn("creatinine", result["draft_comment"].lower())


if __name__ == "__main__":
    unittest.main()
