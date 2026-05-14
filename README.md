# clinical-lab-comment-generator

## Português

### Visão geral
Este projeto implementa um **gerador assistido de comentários laboratoriais clínicos com RAG e interpretação determinística**, desenhado para transformar um conjunto estruturado de exames em um **comentário clínico resumido pronto para revisão humana**.

A proposta central é combinar:

1. **regras clínicas explícitas**
   - leitura de faixas de referência;
   - interpretação de padrões laboratoriais;
   - consolidação de sinais relevantes;

2. **RAG textual**
   - recuperação de casos laboratoriais semelhantes;
   - recuperação de snippets de conhecimento e templates de wording;
   - apoio à redação do comentário final.

O sistema recebe um painel estruturado contendo:
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
- recuperar contexto comparável;
- produzir um comentário final compacto e revisável.

O objetivo não é emitir diagnóstico definitivo. O objetivo é:
- reduzir tempo de comentário laboratorial;
- melhorar consistência textual;
- apoiar revisão médica ou laboratorial;
- preparar o terreno para um workflow mais estruturado de apoio à decisão.

---

### Problema que o projeto resolve
Comentários laboratoriais costumam sofrer com:
- alta repetição de padrões;
- variação de wording entre profissionais;
- necessidade de concisão sem perder sinal clínico;
- dificuldade de reaproveitar exemplos históricos;
- falta de padronização na forma de comentar combinações de achados.

Esse projeto ataca exatamente esse espaço:

**“Dado um conjunto de exames laboratoriais estruturados, como gerar um comentário clínico curto, consistente e apoiado por casos semelhantes e knowledge snippets?”**

A escolha foi por uma arquitetura híbrida:
- **lógica determinística** para o núcleo da interpretação;
- **RAG** para reforçar consistência e recuperação de linguagem útil.

Essa combinação faz sentido porque interpretação laboratorial frequentemente exige:
- rastreabilidade;
- previsibilidade;
- leitura transparente das regras aplicadas.

---

### Base pública recomendada
A melhor base pública para a evolução deste projeto é **NHANES laboratory data**.

#### Por que essa base foi escolhida
Ela oferece:
- grande volume de medições laboratoriais públicas;
- padronização oficial do CDC;
- cobertura ampla de química clínica e biomarcadores;
- ótima aderência a pipelines tabulares;
- excelente ponto de partida para normalização e interpretação laboratorial estruturada.

#### Referências
- [NHANES official CDC page](https://www.cdc.gov/nchs/nhanes/)
- [NHANES laboratory data explorer](https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Laboratory&Cycle=)
- [LOINC](https://loinc.org/)

#### Nota importante sobre o runtime do repositório
Este repositório **não distribui o corpus completo da NHANES**. Em vez disso, ele usa uma **amostra local `NHANES style`**, desenhada para:
- manter o projeto leve;
- permitir execução imediata;
- preservar reprodutibilidade completa no GitHub.

O mapeamento para a base pública recomendada está documentado em [public_dataset_reference.json](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/data/raw/public_dataset_reference.json).

---

### Caminho de evolução
Como próxima etapa para contexto clínico real mais rico:
- `MIMIC-IV labevents`

#### Papel dessa evolução
Enquanto NHANES é excelente para:
- medições laboratoriais públicas;
- análise populacional;
- padronização de valores e ranges;

`MIMIC-IV labevents` é melhor para:
- contexto hospitalar real;
- longitudinalidade;
- correlação com internação, diagnóstico e medicação;
- comentários laboratoriais mais situacionais.

Ou seja:
- **NHANES** = melhor para MVP público e reprodutível
- **MIMIC-IV labevents** = melhor para evolução clínica avançada

---

### Arquitetura do projeto

#### 1. Entrada estruturada
O pipeline recebe um painel resumido de exames laboratoriais em formato numérico, mais um `clinical_context` opcional.

Esse desenho foi escolhido porque:
- aproxima o projeto de um LIS/LIMS ou middleware clínico;
- evita dependência inicial de OCR ou parsing textual;
- facilita validação programática;
- torna o pipeline mais determinístico.

#### 2. Faixas de referência
Arquivo principal: [reference_ranges.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/reference_ranges.py)

Essa camada centraliza faixas básicas de referência para:
- hemoglobina
- leucócitos
- plaquetas
- creatinina
- eGFR
- ALT
- AST
- HbA1c
- glicose
- LDL
- triglicerídeos
- CRP

Também implementa a função:
- `value_flag(name, value)`

que devolve:
- `low`
- `normal`
- `high`

Essa camada é pequena, mas estrutural. Ela torna o projeto:
- testável;
- auditável;
- fácil de expandir para sexo/idade/faixa etária.

#### 3. Lógica clínica determinística
Arquivo principal: [clinical_logic.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/clinical_logic.py)

Essa camada implementa interpretação por domínio:
- `interpret_diabetes`
- `interpret_kidney`
- `interpret_liver`
- `interpret_cbc`
- `interpret_inflammation`
- `interpret_lipids`

##### O que cada função faz
- **Diabetes**
  - interpreta HbA1c e glicose
  - distingue prediabetes e diabetes range
- **Kidney**
  - combina creatinina e eGFR
- **Liver**
  - consolida elevação de transaminases
- **CBC**
  - comenta hemoglobina, leucócitos e plaquetas
- **Inflammation**
  - usa CRP como sinal inflamatório
- **Lipids**
  - destaca LDL e triglicerídeos elevados

Esse é o núcleo clínico do projeto.

Importante:
o sistema **não tenta inferir doenças complexas**. Ele identifica padrões laboratoriais coerentes e os transforma em linguagem clínica curta.

#### 4. Corpus local e knowledge base
Arquivo principal: [data_factory.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/data_factory.py)

Essa camada cria:

##### A. Casos clínico-laboratoriais locais
Cada caso contém:
- cenário clínico
- valores laboratoriais
- comentário final de referência

##### B. Knowledge base
Inclui snippets como:
- wording para diabetes
- wording para função renal
- wording para inflamação
- wording para perfil lipídico

Isso cria uma arquitetura híbrida de retrieval:
- **case-based retrieval**
- **knowledge-based retrieval**

#### 5. Retrieval
Arquivo principal: [retrieval.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/retrieval.py)

O sistema indexa casos e documentos com:
- `TfidfVectorizer(stop_words="english", ngram_range=(1, 2))`
- `cosine_similarity`

##### Espaço de busca
A consulta combina:
- contexto clínico;
- valores laboratoriais serializados em texto;
- e o texto fixo da solicitação.

Cada caso indexado agrega:
- cenário;
- valores;
- comentário clínico de referência.

Isso ajuda o retriever a recuperar não só “valor igual”, mas também um padrão clínico próximo.

#### 6. Geração do comentário
Arquivo principal: [generation.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/generation.py)

A geração combina:
- linhas de interpretação produzidas pela lógica clínica;
- similaridade com casos recuperados;
- snippets de knowledge base;
- comentário do caso mais próximo como reforço contextual.

##### Estratégia atual
Este projeto **não chama um LLM remoto nesta versão**.

A estratégia de geração é:
- **rule-guided drafting**
- com **retrieval de contexto**

Isso foi uma escolha intencional porque:
- mantém o projeto totalmente reproduzível;
- facilita auditoria do raciocínio;
- evita alucinação em contexto clínico delicado;
- prepara o sistema para uma futura camada generativa mais avançada.

#### 7. Orquestração do pipeline
Arquivo principal: [pipeline.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/pipeline.py)

O pipeline:
1. valida ranges plausíveis de entrada;
2. interpreta o painel laboratorial por subdomínio;
3. monta consulta expandida;
4. recupera casos e knowledge snippets;
5. produz o comentário final.

O contrato de saída inclui:
- `dataset_source`
- `public_dataset_reference`
- `case_count`
- `knowledge_doc_count`
- `retrieved_count`
- `confidence`
- `best_similarity`
- `draft_comment`
- `suggested_patterns`
- `reference_case_ids`
- `recommendation`
- `evidence`

---

### Validação defensiva
Um ponto importante neste projeto é que a validação não fica só na API.

O pipeline implementa validação própria em [pipeline.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/pipeline.py), para impedir que valores numericamente absurdos gerem comentários clínicos sem sentido quando o sistema for usado diretamente em Python.

Isso torna o projeto mais robusto em dois cenários:
- uso via `FastAPI`
- uso programático do pipeline como biblioteca

---

### Estratégia de RAG usada neste projeto
Este projeto usa uma forma de RAG orientada a interpretação tabular:

#### Input
- exames laboratoriais estruturados
- contexto clínico opcional

#### Retrieval
- consulta textual baseada em valores e contexto
- top-k casos e snippets mais semelhantes

#### Augmentation
- recuperação de casos comparáveis
- recuperação de guidance de wording
- uso do caso mais próximo como apoio textual

#### Generation
- comentário clínico curto
- guiado por regras e reforçado por recuperação

#### Human review
- nota explícita de revisão clínica obrigatória

Esse design é especialmente adequado para comentários laboratoriais porque:
- a interpretação pode ser parcialmente determinística;
- a linguagem pode ser padronizada;
- o sistema precisa ser conservador.

---

### Contrato técnico da saída
O principal artefato é:

```json
{
  "draft_comment": "...",
  "confidence": "low|medium|high",
  "best_similarity": 0.235,
  "reference_case_ids": ["LAB-1001"],
  "evidence": [...]
}
```

#### Semântica dos campos
- `draft_comment`
  comentário clínico resumido proposto
- `confidence`
  confiança heurística baseada na similaridade do retrieval
- `best_similarity`
  maior score de recuperação
- `reference_case_ids`
  casos usados como principal apoio
- `evidence`
  trilha de recuperação usada pelo pipeline

Esse contrato facilita:
- revisão humana;
- inspeção do racional;
- futura exportação para UI de aprovação.

---

### Interfaces

#### API
Arquivo: [app.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/app.py)

Endpoints:
- `GET /health`
- `POST /generate-comment`

Payload esperado:

```json
{
  "hemoglobin_g_dl": 13.2,
  "wbc_k_ul": 7.4,
  "platelets_k_ul": 250.0,
  "creatinine_mg_dl": 1.8,
  "egfr_ml_min": 46.0,
  "alt_u_l": 32.0,
  "ast_u_l": 29.0,
  "a1c_percent": 8.0,
  "glucose_mg_dl": 162.0,
  "ldl_mg_dl": 140.0,
  "triglycerides_mg_dl": 188.0,
  "crp_mg_l": 4.2,
  "clinical_context": "Outpatient diabetes follow-up with chronic kidney disease concern.",
  "top_k": 5
}
```

#### Streamlit demo
Arquivo: [streamlit_app.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/streamlit_app.py)

A demo expõe:
- entrada manual dos exames;
- comentário sugerido;
- confiança;
- casos de referência;
- evidências recuperadas.

---

### Ferramentas e bibliotecas

#### Runtime principal
- `Python`
- `scikit-learn`
- `FastAPI`
- `Streamlit`
- `pydantic`

#### Componentes usados do scikit-learn
- `TfidfVectorizer`
  - indexação textual com unigramas e bigramas
- `cosine_similarity`
  - ranking de casos e documentos

#### Standard library relevante
- `json`
- `pathlib`
- `dataclasses`
- `typing`
- `collections.Counter`

#### Testes
- `unittest`

---

### Como executar
```bash
python3 main.py
python3 -m unittest discover -s tests -v
streamlit run streamlit_app.py
uvicorn app:app --reload
```

---

### Resultado atual do exemplo principal
O exemplo padrão atual produz:

- `dataset_source = nhanes_style_local_sample`
- `case_count = 6`
- `knowledge_doc_count = 4`
- `best_similarity = 0.235`
- `confidence = low`

O comentário gerado destaca:
- alteração renal;
- padrão compatível com diabetes;
- dislipidemia.

Isso é coerente com a amostra usada:
- creatinina elevada;
- eGFR reduzido;
- HbA1c e glicose elevadas;
- LDL e triglicerídeos elevados.

---

### Validação
O projeto foi validado com:

```bash
python3 main.py
python3 -m unittest discover -s tests -v
python3 -m py_compile main.py app.py streamlit_app.py src/reference_ranges.py src/clinical_logic.py src/data_factory.py src/retrieval.py src/generation.py src/pipeline.py tests/test_project.py
```

Testes cobertos em [test_project.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/tests/test_project.py):
- interpretação de diabetes;
- interpretação de função renal;
- geração de comentário final;
- rejeição de entradas implausíveis no pipeline.

---

### Limitações atuais
Este MVP ainda tem limites importantes:

- usa corpus local inspirado em bases públicas;
- não modela sexo, idade ou faixa etária;
- não usa ranges laboratoriais específicos por população;
- não modela longitudinalidade;
- não integra LOINC real;
- não substitui interpretação médica.

Portanto, o projeto deve ser entendido como:

**um MVP de arquitetura clínica para geração assistida de comentários laboratoriais, não como um interpretador diagnóstico final.**

---

### Próximos passos técnicos recomendados
1. Integrar códigos `LOINC` reais.
2. Adaptar referência por sexo/idade quando aplicável.
3. Adicionar contexto longitudinal.
4. Criar templates por especialidade:
   - endocrinologia
   - nefrologia
   - hepatologia
   - inflamação/infeccioso
5. Evoluir para `MIMIC-IV labevents`.
6. Criar UI de revisão/aprovação com histórico.

---

### Como defender este projeto em entrevista
Uma síntese forte seria:

> Construí um gerador assistido de comentários laboratoriais que combina interpretação determinística de exames com um pipeline de RAG. O sistema recebe um painel laboratorial estruturado, identifica padrões relevantes como disfunção renal, diabetes e inflamação, recupera casos e snippets semelhantes e gera um comentário final para revisão clínica. O MVP é totalmente reproduzível com base local inspirada em NHANES, mas foi desenhado para evoluir para bases como MIMIC-IV e integração real com LOINC.

---

## English

### Overview
This repository implements an **assisted clinical laboratory comment generator with RAG and deterministic interpretation logic**, designed to transform a structured set of lab results into a **concise clinical comment ready for human review**.

The core idea is to combine:

1. **explicit clinical rules**
   - reference range evaluation;
   - pattern interpretation;
   - signal consolidation;

2. **textual RAG**
   - retrieval of similar lab cases;
   - retrieval of wording/guideline snippets;
   - support for final comment drafting.

The system receives a structured panel including:
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

and uses those measurements to:
- identify relevant lab patterns;
- retrieve comparable context;
- generate a compact and reviewable final comment.

The goal is not to produce a final diagnosis. The goal is to:
- reduce lab comment drafting time;
- improve wording consistency;
- support physician or laboratory review;
- provide a foundation for more structured decision support.

---

### Problem statement
Clinical lab comments often suffer from:
- repetitive patterns;
- wording variability across professionals;
- the need for concise but clinically meaningful summaries;
- difficulty reusing historical examples;
- lack of standardization when commenting on combinations of abnormal values.

This repository addresses exactly that space:

**“Given a structured laboratory panel, how can we generate a short clinical comment supported by similar cases and knowledge snippets?”**

The architecture is intentionally hybrid:
- **deterministic logic** for the core interpretation
- **RAG** for contextual wording support

This makes sense because lab interpretation often requires:
- traceability;
- predictability;
- transparent rule application.

---

### Recommended public dataset
The strongest public dataset for the evolution of this project is **NHANES laboratory data**.

#### Why this dataset was selected
It provides:
- large-scale public laboratory measurements;
- official CDC standardization;
- broad chemistry and biomarker coverage;
- strong fit for structured tabular pipelines;
- an excellent base for normalized laboratory interpretation workflows.

#### References
- [NHANES official CDC page](https://www.cdc.gov/nchs/nhanes/)
- [NHANES laboratory data explorer](https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Laboratory&Cycle=)
- [LOINC](https://loinc.org/)

#### Important runtime note
This repository does **not** redistribute the full NHANES corpus. Instead, it uses a **local `NHANES style` sample**, designed to:
- keep the project lightweight;
- allow immediate execution;
- preserve full reproducibility on GitHub.

The mapping to the recommended public dataset is documented in [public_dataset_reference.json](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/data/raw/public_dataset_reference.json).

---

### Upgrade path
For richer real-world clinical context, the next natural dataset is:
- `MIMIC-IV labevents`

#### Role of that upgrade
While NHANES is excellent for:
- public laboratory measurements;
- population-level structure;
- value normalization and range handling;

`MIMIC-IV labevents` is better for:
- inpatient context;
- longitudinal trajectories;
- links to diagnosis, medication, and hospitalization;
- more situational laboratory comments.

So:
- **NHANES** = best for a public and reproducible MVP
- **MIMIC-IV labevents** = best for advanced clinical expansion

---

### Project architecture

#### 1. Structured input layer
The pipeline receives a compact structured laboratory panel plus an optional `clinical_context`.

This design was chosen because it:
- mirrors LIS/LIMS or middleware integration;
- avoids early dependence on OCR or free-text parsing;
- simplifies validation;
- keeps the workflow deterministic.

#### 2. Reference range layer
Primary file: [reference_ranges.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/reference_ranges.py)

This layer centralizes simplified reference cutoffs for:
- hemoglobin
- white blood cells
- platelets
- creatinine
- eGFR
- ALT
- AST
- HbA1c
- glucose
- LDL
- triglycerides
- CRP

It also exposes:
- `value_flag(name, value)`

which returns:
- `low`
- `normal`
- `high`

This is a small but foundational layer. It makes the repository:
- testable;
- auditable;
- easy to extend toward sex-/age-specific logic.

#### 3. Deterministic clinical interpretation layer
Primary file: [clinical_logic.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/clinical_logic.py)

This layer implements domain-specific interpretation functions:
- `interpret_diabetes`
- `interpret_kidney`
- `interpret_liver`
- `interpret_cbc`
- `interpret_inflammation`
- `interpret_lipids`

##### What each function covers
- **Diabetes**
  - interprets HbA1c and glucose
  - distinguishes prediabetes vs diabetes-range patterns
- **Kidney**
  - combines creatinine and eGFR
- **Liver**
  - summarizes transaminase elevation
- **CBC**
  - comments on hemoglobin, white cells, and platelets
- **Inflammation**
  - uses CRP as a simplified inflammatory signal
- **Lipids**
  - highlights LDL and triglycerides separately

This is the clinical core of the project.

Important:
the system does **not** attempt to infer complex diagnoses. It identifies coherent lab patterns and converts them into concise comment language.

#### 4. Local corpus and knowledge base
Primary file: [data_factory.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/data_factory.py)

This layer creates:

##### A. Local laboratory cases
Each case contains:
- a clinical scenario
- structured values
- a reference comment

##### B. Knowledge snippets
These cover wording for:
- diabetes
- kidney function
- inflammation
- lipid profile

This gives the project a hybrid retrieval architecture:
- **case-based retrieval**
- **knowledge-based retrieval**

#### 5. Retrieval layer
Primary file: [retrieval.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/retrieval.py)

The project indexes cases and documents using:
- `TfidfVectorizer(stop_words="english", ngram_range=(1, 2))`
- `cosine_similarity`

##### Retrieval space
The query combines:
- clinical context;
- serialized laboratory values;
- a fixed generation intent.

Each indexed case includes:
- scenario;
- numeric values;
- reference comment.

This helps the retriever recover not only close numeric values, but also clinically similar interpretive patterns.

#### 6. Comment generation layer
Primary file: [generation.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/generation.py)

Generation combines:
- deterministic interpretation lines;
- similarity to retrieved cases;
- knowledge snippets;
- the nearest-case comment as contextual support.

##### Current generation strategy
This version does **not** call a remote LLM.

The generation strategy is:
- **rule-guided drafting**
- with **retrieved contextual reinforcement**

This was intentional because it:
- keeps the project fully reproducible;
- improves auditability;
- reduces hallucination risk in a clinical setting;
- creates a strong foundation before introducing a more open generative layer.

#### 7. Pipeline orchestration layer
Primary file: [pipeline.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/pipeline.py)

The pipeline:
1. validates plausible numeric ranges;
2. interprets the panel by subdomain;
3. builds an expanded retrieval query;
4. retrieves cases and knowledge snippets;
5. assembles the final comment.

The output contract includes:
- `dataset_source`
- `public_dataset_reference`
- `case_count`
- `knowledge_doc_count`
- `retrieved_count`
- `confidence`
- `best_similarity`
- `draft_comment`
- `suggested_patterns`
- `reference_case_ids`
- `recommendation`
- `evidence`

---

### Defensive validation
An important design choice in this repository is that validation does not live only in the API layer.

The pipeline itself validates plausible ranges in [pipeline.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/src/pipeline.py), so impossible or absurd values do not silently generate misleading comments when the class is used directly from Python.

This makes the project more robust in two distinct scenarios:
- `FastAPI` usage
- direct programmatic usage of the pipeline as a library

---

### RAG strategy used in this project
This repository uses a tabular-interpretation-oriented RAG flow:

#### Input
- structured laboratory values
- optional clinical context

#### Retrieval
- textual query built from values and context
- top-k nearest cases and snippets

#### Augmentation
- similar-case retrieval
- wording/guideline retrieval
- nearest-case comment as stylistic support

#### Generation
- short clinical comment
- grounded in deterministic interpretation and reinforced by retrieved context

#### Human review
- explicit note that clinical review is required before sign-off

This design is especially appropriate for laboratory comments because:
- the interpretation can be partially deterministic;
- the wording can be standardized;
- the system should stay conservative.

---

### Technical output contract
The primary artifact is:

```json
{
  "draft_comment": "...",
  "confidence": "low|medium|high",
  "best_similarity": 0.235,
  "reference_case_ids": ["LAB-1001"],
  "evidence": [...]
}
```

#### Field semantics
- `draft_comment`
  proposed short-form clinical comment
- `confidence`
  heuristic confidence based on retrieval similarity
- `best_similarity`
  top retrieval score
- `reference_case_ids`
  main supporting cases
- `evidence`
  retrieval trace returned by the pipeline

This makes the output:
- reviewable;
- inspectable;
- easy to plug into a future approval UI.

---

### Interfaces

#### API
File: [app.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/app.py)

Endpoints:
- `GET /health`
- `POST /generate-comment`

Expected payload:

```json
{
  "hemoglobin_g_dl": 13.2,
  "wbc_k_ul": 7.4,
  "platelets_k_ul": 250.0,
  "creatinine_mg_dl": 1.8,
  "egfr_ml_min": 46.0,
  "alt_u_l": 32.0,
  "ast_u_l": 29.0,
  "a1c_percent": 8.0,
  "glucose_mg_dl": 162.0,
  "ldl_mg_dl": 140.0,
  "triglycerides_mg_dl": 188.0,
  "crp_mg_l": 4.2,
  "clinical_context": "Outpatient diabetes follow-up with chronic kidney disease concern.",
  "top_k": 5
}
```

#### Streamlit demo
File: [streamlit_app.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/streamlit_app.py)

The demo exposes:
- manual laboratory entry;
- suggested comment;
- confidence;
- reference cases;
- retrieved evidence.

---

### Tools and libraries

#### Main runtime
- `Python`
- `scikit-learn`
- `FastAPI`
- `Streamlit`
- `pydantic`

#### scikit-learn components used
- `TfidfVectorizer`
  - unigram/bigram textual indexing
- `cosine_similarity`
  - case/document ranking

#### Relevant standard library modules
- `json`
- `pathlib`
- `dataclasses`
- `typing`
- `collections.Counter`

#### Testing
- `unittest`

---

### How to run
```bash
python3 main.py
python3 -m unittest discover -s tests -v
streamlit run streamlit_app.py
uvicorn app:app --reload
```

---

### Current example output
The default example currently produces:

- `dataset_source = nhanes_style_local_sample`
- `case_count = 6`
- `knowledge_doc_count = 4`
- `best_similarity = 0.235`
- `confidence = low`

The generated comment highlights:
- renal impairment;
- diabetes-range pattern;
- dyslipidemia.

That is coherent with the sample input:
- elevated creatinine;
- reduced eGFR;
- elevated HbA1c and glucose;
- elevated LDL and triglycerides.

---

### Validation
The project was validated with:

```bash
python3 main.py
python3 -m unittest discover -s tests -v
python3 -m py_compile main.py app.py streamlit_app.py src/reference_ranges.py src/clinical_logic.py src/data_factory.py src/retrieval.py src/generation.py src/pipeline.py tests/test_project.py
```

Tests covered in [test_project.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/clinical-lab-comment-generator/tests/test_project.py):
- diabetes interpretation
- kidney interpretation
- final comment generation
- rejection of implausible numeric values

---

### Current limitations
This MVP still has important limitations:

- uses a local corpus inspired by public datasets;
- does not model sex, age, or age-specific intervals;
- does not use population-specific laboratory ranges;
- does not model longitudinal trends;
- does not integrate real LOINC coding;
- does not replace physician interpretation.

So this repository should be understood as:

**a clinical AI architecture MVP for assisted laboratory comments, not a final diagnostic interpretation engine.**

---

### Recommended next technical steps
1. Integrate real `LOINC` codes.
2. Add sex-/age-aware reference intervals where appropriate.
3. Add longitudinal interpretation.
4. Build specialty-specific templates for:
   - endocrinology
   - nephrology
   - hepatology
   - inflammatory/infectious use cases
5. Evolve toward `MIMIC-IV labevents`.
6. Build a review/approval UI with history.

---

### How to position this project in an interview
A strong summary would be:

> I built an assisted clinical laboratory comment generator that combines deterministic interpretation rules with a RAG pipeline. The system receives a structured laboratory panel, detects relevant patterns such as renal impairment, diabetes-range hyperglycemia, and inflammation, retrieves similar cases and wording snippets, and produces a concise final comment for clinical review. The MVP is fully reproducible using a local NHANES-style corpus, but it is designed to evolve toward MIMIC-IV and real LOINC integration.
