# clinical-lab-comment-generator

## Português

### Visão geral
Este projeto implementa um **gerador assistido de comentários laboratoriais clínicos com RAG e lógica determinística**, desenhado para transformar um conjunto estruturado de exames em um **comentário clínico resumido pronto para revisão humana**.

O sistema recebe valores laboratoriais como:
- hemoglobina
- leucócitos
- plaquetas
- creatinina
- eGFR
- ALT / AST
- HbA1c
- glicose
- LDL
- triglicerídeos
- CRP

e usa esses dados para:
- identificar padrões laboratoriais relevantes;
- recuperar casos semelhantes;
- recuperar snippets de conhecimento/wording;
- montar um comentário clínico compacto.

O objetivo não é emitir diagnóstico final. O objetivo é:
- acelerar a produção de comentários laboratoriais;
- melhorar consistência textual;
- apoiar revisão médica ou laboratorial.

### Base pública recomendada
A melhor base pública para a evolução deste projeto é **NHANES laboratory data**, porque oferece:
- grande volume de medições laboratoriais públicas;
- padronização oficial do CDC;
- forte aderência a pipelines tabulares de interpretação laboratorial.

Referências:
- [NHANES official CDC page](https://www.cdc.gov/nchs/nhanes/)
- [NHANES laboratory data explorer](https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Laboratory&Cycle=)
- [LOINC](https://loinc.org/)

### Caminho de evolução
Como evolução para contexto clínico real mais rico:
- `MIMIC-IV labevents`

### Arquitetura
#### 1. Entrada estruturada
O pipeline recebe um painel resumido de exames laboratoriais.

#### 2. Regras clínicas
Em [clinical_logic.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/clinical_logic.py), o projeto implementa interpretações para:
- glicose/HbA1c
- função renal
- transaminases
- hemograma
- inflamação
- perfil lipídico

#### 3. Faixas de referência
Em [reference_ranges.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/reference_ranges.py), o projeto centraliza limites de referência e flags básicas.

#### 4. Corpus e knowledge base
Em [data_factory.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/data_factory.py), o projeto cria:
- casos clínico-laboratoriais locais;
- templates de comentário;
- referência formal à base pública sugerida.

#### 5. Retrieval
Em [retrieval.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/retrieval.py), cada caso e documento é indexado com:
- `TfidfVectorizer`
- `cosine_similarity`

#### 6. Geração do comentário
Em [generation.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/generation.py), o sistema:
- combina regras clínicas;
- ancora a redação em casos parecidos;
- retorna comentário final, evidências e confiança.

#### 7. Orquestração
Em [pipeline.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/pipeline.py), o pipeline integra:
- interpretação clínica
- retrieval
- geração do comentário

### Ferramentas e bibliotecas
- `Python`
- `scikit-learn`
  - `TfidfVectorizer`
  - `cosine_similarity`
- `FastAPI`
- `Streamlit`
- `pydantic`
- `unittest`

### Interface
- API em [app.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/app.py)
- demo em [streamlit_app.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/streamlit_app.py)

### Execução
```bash
python3 main.py
python3 -m unittest discover -s tests -v
streamlit run streamlit_app.py
uvicorn app:app --reload
```

### Limitações
- usa corpus local inspirado em bases públicas;
- não integra intervalo de referência por sexo/idade;
- não substitui interpretação médica;
- não modela longitudinalidade do paciente.

### Próximos passos
- integração com LOINC real;
- painéis laboratoriais por contexto clínico;
- interpretação longitudinal;
- comentários por especialidade;
- UI com revisão e aprovação.

## English

### Overview
This repository implements an **assisted clinical lab comment generator with RAG and deterministic interpretation logic**, designed to turn a structured set of laboratory values into a **concise clinical comment ready for human review**.

The system receives laboratory values such as:
- hemoglobin
- white blood cells
- platelets
- creatinine
- eGFR
- ALT / AST
- HbA1c
- glucose
- LDL
- triglycerides
- CRP

and uses them to:
- identify clinically relevant lab patterns;
- retrieve similar cases;
- retrieve wording/knowledge snippets;
- assemble a compact clinical comment.

The goal is not to produce a final diagnosis. The goal is to:
- accelerate lab comment drafting;
- improve wording consistency;
- support physician or laboratory review.

### Recommended public dataset
The strongest public dataset for the evolution of this project is **NHANES laboratory data**, because it provides:
- large-scale public laboratory measurements;
- official CDC standardization;
- strong fit for tabular lab interpretation pipelines.

References:
- [NHANES official CDC page](https://www.cdc.gov/nchs/nhanes/)
- [NHANES laboratory data explorer](https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Laboratory&Cycle=)
- [LOINC](https://loinc.org/)

### Upgrade path
For richer real-world clinical context:
- `MIMIC-IV labevents`

### Architecture
#### 1. Structured input
The pipeline receives a compact structured lab panel.

#### 2. Clinical rules
In [clinical_logic.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/clinical_logic.py), the project implements interpretation for:
- glucose / HbA1c
- kidney function
- transaminases
- CBC
- inflammation
- lipid profile

#### 3. Reference ranges
In [reference_ranges.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/reference_ranges.py), the repository centralizes reference cutoffs and basic flags.

#### 4. Case corpus and knowledge base
In [data_factory.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/data_factory.py), the project builds:
- local clinic-lab cases;
- comment templates;
- a formal reference to the suggested public dataset.

#### 5. Retrieval
In [retrieval.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/retrieval.py), each case and document is indexed with:
- `TfidfVectorizer`
- `cosine_similarity`

#### 6. Comment generation
In [generation.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/generation.py), the system:
- combines deterministic interpretation rules;
- anchors wording in similar retrieved cases;
- returns a final draft comment, evidence, and confidence.

#### 7. Orchestration
In [pipeline.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/pipeline.py), the pipeline integrates:
- clinical interpretation
- retrieval
- comment generation

### Tools and libraries
- `Python`
- `scikit-learn`
  - `TfidfVectorizer`
  - `cosine_similarity`
- `FastAPI`
- `Streamlit`
- `pydantic`
- `unittest`

### Interfaces
- API in [app.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/app.py)
- demo in [streamlit_app.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/streamlit_app.py)

### Run
```bash
python3 main.py
python3 -m unittest discover -s tests -v
streamlit run streamlit_app.py
uvicorn app:app --reload
```

### Limitations
- uses a local corpus inspired by public datasets;
- no sex/age-specific reference intervals yet;
- not a replacement for physician interpretation;
- no patient longitudinal modeling yet.

### Next steps
- real LOINC integration;
- context-specific lab panels;
- longitudinal interpretation;
- specialty-specific comment templates;
- review and approval UI.
