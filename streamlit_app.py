from __future__ import annotations

import streamlit as st

from src.pipeline import ClinicalLabCommentGeneratorPipeline


pipeline = ClinicalLabCommentGeneratorPipeline()
st.set_page_config(page_title="Gerador de Comentário Laboratorial", layout="wide")

st.title("Gerador de Comentário Laboratorial Clínico")
st.write(
    "Este sistema interpreta um conjunto estruturado de exames laboratoriais, recupera casos semelhantes e gera um comentário clínico resumido para revisão humana."
)

with st.form("lab_form"):
    clinical_context = st.text_input("Contexto clínico", value="Seguimento ambulatorial de diabetes com suspeita de doença renal crônica.")
    col1, col2, col3 = st.columns(3)
    hemoglobin_g_dl = col1.number_input("Hemoglobina (g/dL)", min_value=0.0, max_value=25.0, value=13.2)
    wbc_k_ul = col2.number_input("Leucócitos (K/uL)", min_value=0.0, max_value=100.0, value=7.4)
    platelets_k_ul = col3.number_input("Plaquetas (K/uL)", min_value=0.0, max_value=2000.0, value=250.0)

    col4, col5, col6 = st.columns(3)
    creatinine_mg_dl = col4.number_input("Creatinina (mg/dL)", min_value=0.0, max_value=20.0, value=1.8)
    egfr_ml_min = col5.number_input("eGFR (mL/min)", min_value=0.0, max_value=200.0, value=46.0)
    crp_mg_l = col6.number_input("CRP (mg/L)", min_value=0.0, max_value=500.0, value=4.2)

    col7, col8, col9 = st.columns(3)
    alt_u_l = col7.number_input("ALT (U/L)", min_value=0.0, max_value=5000.0, value=32.0)
    ast_u_l = col8.number_input("AST (U/L)", min_value=0.0, max_value=5000.0, value=29.0)
    a1c_percent = col9.number_input("HbA1c (%)", min_value=0.0, max_value=20.0, value=8.0)

    col10, col11, col12 = st.columns(3)
    glucose_mg_dl = col10.number_input("Glicose (mg/dL)", min_value=0.0, max_value=1000.0, value=162.0)
    ldl_mg_dl = col11.number_input("LDL (mg/dL)", min_value=0.0, max_value=500.0, value=140.0)
    triglycerides_mg_dl = col12.number_input("Triglicerídeos (mg/dL)", min_value=0.0, max_value=5000.0, value=188.0)

    submitted = st.form_submit_button("Gerar comentário")

if submitted:
    result = pipeline.run(
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
        clinical_context=clinical_context,
    )

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Confiança RAG", result["confidence"].capitalize())
    col_b.metric("Melhor similaridade", result["best_similarity"])
    col_c.metric("Casos no corpus", result["case_count"])

    st.subheader("Comentário sugerido")
    st.write(result["draft_comment"])

    st.subheader("Apoio à revisão")
    st.write(result["recommendation"])
    st.write(f"Casos de referência: {', '.join(result['reference_case_ids']) or 'n/a'}")

    with st.expander("Evidências recuperadas"):
        for item in result["evidence"]:
            st.write(
                f"- {item['source_type']} | {item['source_id']} | {item['title']} | similarity={item['similarity']}"
            )

    with st.expander("Base pública sugerida"):
        st.code(result["public_dataset_reference"])
