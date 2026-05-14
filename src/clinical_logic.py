from __future__ import annotations

from .reference_ranges import value_flag


def interpret_diabetes(a1c_percent: float, glucose_mg_dl: float) -> list[str]:
    comments: list[str] = []
    if a1c_percent >= 6.5:
        comments.append("Laboratory pattern is compatible with diabetes range based on HbA1c.")
    elif a1c_percent >= 5.7:
        comments.append("HbA1c is in the prediabetes range.")

    if glucose_mg_dl >= 126:
        comments.append("Fasting glucose is elevated in the diabetes range if the sample was fasting.")
    elif glucose_mg_dl >= 100:
        comments.append("Glucose is mildly elevated above the usual fasting reference range.")
    return comments


def interpret_kidney(creatinine_mg_dl: float, egfr_ml_min: float) -> list[str]:
    comments: list[str] = []
    if value_flag("creatinine_mg_dl", creatinine_mg_dl) == "high":
        comments.append("Creatinine is elevated.")
    if egfr_ml_min < 60:
        comments.append("Estimated glomerular filtration rate is reduced.")
    return comments


def interpret_liver(alt_u_l: float, ast_u_l: float) -> list[str]:
    comments: list[str] = []
    if value_flag("alt_u_l", alt_u_l) == "high" or value_flag("ast_u_l", ast_u_l) == "high":
        comments.append("Transaminases are elevated.")
    return comments


def interpret_cbc(hemoglobin_g_dl: float, wbc_k_ul: float, platelets_k_ul: float) -> list[str]:
    comments: list[str] = []
    if value_flag("hemoglobin_g_dl", hemoglobin_g_dl) == "low":
        comments.append("Hemoglobin is reduced, which may indicate anemia depending on the clinical context.")
    if value_flag("wbc_k_ul", wbc_k_ul) == "high":
        comments.append("White blood cell count is elevated.")
    elif value_flag("wbc_k_ul", wbc_k_ul) == "low":
        comments.append("White blood cell count is reduced.")
    if value_flag("platelets_k_ul", platelets_k_ul) == "low":
        comments.append("Platelet count is reduced.")
    elif value_flag("platelets_k_ul", platelets_k_ul) == "high":
        comments.append("Platelet count is elevated.")
    return comments


def interpret_inflammation(crp_mg_l: float) -> list[str]:
    if value_flag("crp_mg_l", crp_mg_l) == "high":
        return ["C-reactive protein is elevated, suggesting an inflammatory response."]
    return []


def interpret_lipids(ldl_mg_dl: float, triglycerides_mg_dl: float) -> list[str]:
    comments: list[str] = []
    if value_flag("ldl_mg_dl", ldl_mg_dl) == "high":
        comments.append("LDL cholesterol is elevated.")
    if value_flag("triglycerides_mg_dl", triglycerides_mg_dl) == "high":
        comments.append("Triglycerides are elevated.")
    return comments
