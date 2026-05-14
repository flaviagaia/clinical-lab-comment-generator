from __future__ import annotations


REFERENCE_RANGES = {
    "hemoglobin_g_dl": {"low": 12.0, "high": 17.5},
    "wbc_k_ul": {"low": 4.0, "high": 11.0},
    "platelets_k_ul": {"low": 150.0, "high": 450.0},
    "creatinine_mg_dl": {"low": 0.5, "high": 1.3},
    "egfr_ml_min": {"low": 60.0, "high": 999.0},
    "alt_u_l": {"low": 0.0, "high": 55.0},
    "ast_u_l": {"low": 0.0, "high": 40.0},
    "a1c_percent": {"low": 0.0, "high": 5.6},
    "glucose_mg_dl": {"low": 70.0, "high": 99.0},
    "ldl_mg_dl": {"low": 0.0, "high": 129.0},
    "triglycerides_mg_dl": {"low": 0.0, "high": 149.0},
    "crp_mg_l": {"low": 0.0, "high": 5.0},
}


def value_flag(name: str, value: float) -> str:
    reference = REFERENCE_RANGES[name]
    if value < reference["low"]:
        return "low"
    if value > reference["high"]:
        return "high"
    return "normal"
