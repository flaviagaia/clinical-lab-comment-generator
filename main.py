from __future__ import annotations

import json

from src.pipeline import ClinicalLabCommentGeneratorPipeline


def main() -> None:
    pipeline = ClinicalLabCommentGeneratorPipeline()
    result = pipeline.run(
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
        clinical_context="Outpatient diabetes follow-up with chronic kidney disease concern.",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
