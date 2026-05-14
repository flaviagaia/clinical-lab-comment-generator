from __future__ import annotations

from pathlib import Path
import json


def build_case_corpus() -> list[dict]:
    return [
        {
            "case_id": "LAB-1001",
            "scenario": "Diabetes with kidney impairment",
            "hemoglobin_g_dl": 13.4,
            "wbc_k_ul": 7.6,
            "platelets_k_ul": 265.0,
            "creatinine_mg_dl": 1.7,
            "egfr_ml_min": 48.0,
            "alt_u_l": 28.0,
            "ast_u_l": 25.0,
            "a1c_percent": 8.2,
            "glucose_mg_dl": 168.0,
            "ldl_mg_dl": 118.0,
            "triglycerides_mg_dl": 160.0,
            "crp_mg_l": 3.1,
            "comment": (
                "HbA1c and glucose are in the diabetes range. Creatinine is elevated and estimated glomerular filtration rate is reduced. "
                "Triglycerides are mildly elevated."
            ),
        },
        {
            "case_id": "LAB-1002",
            "scenario": "Inflammatory syndrome with leukocytosis",
            "hemoglobin_g_dl": 12.8,
            "wbc_k_ul": 15.3,
            "platelets_k_ul": 410.0,
            "creatinine_mg_dl": 0.9,
            "egfr_ml_min": 95.0,
            "alt_u_l": 32.0,
            "ast_u_l": 30.0,
            "a1c_percent": 5.5,
            "glucose_mg_dl": 94.0,
            "ldl_mg_dl": 104.0,
            "triglycerides_mg_dl": 120.0,
            "crp_mg_l": 22.0,
            "comment": (
                "Leukocytosis and markedly elevated C-reactive protein suggest an active inflammatory or infectious process."
            ),
        },
        {
            "case_id": "LAB-1003",
            "scenario": "Prediabetes and dyslipidemia",
            "hemoglobin_g_dl": 14.1,
            "wbc_k_ul": 6.8,
            "platelets_k_ul": 248.0,
            "creatinine_mg_dl": 1.0,
            "egfr_ml_min": 88.0,
            "alt_u_l": 33.0,
            "ast_u_l": 29.0,
            "a1c_percent": 5.9,
            "glucose_mg_dl": 108.0,
            "ldl_mg_dl": 154.0,
            "triglycerides_mg_dl": 198.0,
            "crp_mg_l": 2.4,
            "comment": (
                "HbA1c is in the prediabetes range. LDL cholesterol and triglycerides are elevated."
            ),
        },
        {
            "case_id": "LAB-1004",
            "scenario": "Anemia pattern",
            "hemoglobin_g_dl": 9.6,
            "wbc_k_ul": 7.1,
            "platelets_k_ul": 320.0,
            "creatinine_mg_dl": 0.8,
            "egfr_ml_min": 102.0,
            "alt_u_l": 20.0,
            "ast_u_l": 18.0,
            "a1c_percent": 5.4,
            "glucose_mg_dl": 92.0,
            "ldl_mg_dl": 110.0,
            "triglycerides_mg_dl": 118.0,
            "crp_mg_l": 1.2,
            "comment": (
                "Hemoglobin is reduced, suggesting anemia in the appropriate clinical context."
            ),
        },
        {
            "case_id": "LAB-1005",
            "scenario": "Hepatocellular injury pattern",
            "hemoglobin_g_dl": 14.8,
            "wbc_k_ul": 8.0,
            "platelets_k_ul": 240.0,
            "creatinine_mg_dl": 1.0,
            "egfr_ml_min": 84.0,
            "alt_u_l": 145.0,
            "ast_u_l": 118.0,
            "a1c_percent": 5.3,
            "glucose_mg_dl": 96.0,
            "ldl_mg_dl": 108.0,
            "triglycerides_mg_dl": 130.0,
            "crp_mg_l": 4.0,
            "comment": (
                "Transaminases are elevated, compatible with a hepatocellular injury pattern."
            ),
        },
        {
            "case_id": "LAB-1006",
            "scenario": "Reference range profile",
            "hemoglobin_g_dl": 14.4,
            "wbc_k_ul": 6.2,
            "platelets_k_ul": 230.0,
            "creatinine_mg_dl": 0.9,
            "egfr_ml_min": 96.0,
            "alt_u_l": 25.0,
            "ast_u_l": 22.0,
            "a1c_percent": 5.2,
            "glucose_mg_dl": 90.0,
            "ldl_mg_dl": 102.0,
            "triglycerides_mg_dl": 110.0,
            "crp_mg_l": 1.0,
            "comment": (
                "Reviewed analytes are within the expected reference range."
            ),
        },
    ]


def build_knowledge_base() -> list[dict]:
    return [
        {
            "doc_id": "KB-LAB-1001",
            "title": "Diabetes comment wording",
            "category": "guideline",
            "content": (
                "HbA1c in the diabetes range should be distinguished from prediabetes. If fasting glucose is also elevated, the comment can note concordant hyperglycemia."
            ),
        },
        {
            "doc_id": "KB-LAB-1002",
            "title": "Kidney function comment wording",
            "category": "template",
            "content": (
                "Creatinine and estimated glomerular filtration rate should be interpreted together when commenting on renal function."
            ),
        },
        {
            "doc_id": "KB-LAB-1003",
            "title": "Inflammation comment wording",
            "category": "template",
            "content": (
                "Leukocytosis and elevated CRP can be summarized as an inflammatory or infectious pattern if the clinical context supports it."
            ),
        },
        {
            "doc_id": "KB-LAB-1004",
            "title": "Lipid profile comment wording",
            "category": "guideline",
            "content": (
                "LDL cholesterol and triglycerides should be commented on separately because they may carry different management implications."
            ),
        },
    ]


def write_public_dataset_reference(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "recommended_public_dataset": {
            "name": "NHANES laboratory data",
            "why_it_was_chosen": [
                "large official public laboratory datasets from CDC",
                "broad coverage of chemistry and biomarker measurements",
                "strong fit for structured tabular lab interpretation pipelines",
            ],
            "references": [
                {
                    "label": "NHANES official CDC page",
                    "url": "https://www.cdc.gov/nchs/nhanes/",
                },
                {
                    "label": "NHANES laboratory data explorer",
                    "url": "https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Laboratory&Cycle=",
                },
                {
                    "label": "LOINC",
                    "url": "https://loinc.org/",
                },
            ],
        },
        "advanced_upgrade_path": {
            "datasets": [
                {
                    "name": "MIMIC-IV labevents",
                    "note": "richer real-world inpatient lab context, but credentialed access required",
                }
            ]
        },
        "runtime_note": "This repository uses a local structured laboratory sample corpus inspired by public lab datasets and standard comment phrasing so the stack remains reproducible.",
    }
    path = output_dir / "public_dataset_reference.json"
    serialized = json.dumps(payload, indent=2)
    if not path.exists() or path.read_text(encoding="utf-8") != serialized:
        path.write_text(serialized, encoding="utf-8")
    return path
