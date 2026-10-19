# DPDP Policy Compliance Checker: Implementation Plan

| | |
|---|---|
| **Working name** | `dpdp-checker` (product line: Suraksha) |
| **Document version** | 1.0, 19 October 2026 |
| **Status** | Baseline for Phase 0. Changes to decisions in section 16 require a new ADR. |
| **Audience** | Engineers joining the project, reviewers, AI coding agents used for implementation and change requests |
| **Owner** | AI Engineering, Stark Digital |
| **Statutory anchor** | Digital Personal Data Protection Act, 2023 and Digital Personal Data Protection Rules, 2025 (G.S.R. 846(E), 13 Nov 2025). Substantive obligations apply from **13 May 2027**. |

## How to use this document

- **Humans:** read sections 1 to 4 first, about thirty minutes. Then read the phase you are working on in section 13. Sections 5 to 12 are the specification you build against. Appendices are reference material.
- **AI coding agents:** treat sections 4 to 12 as the specification and section 13 as the backlog. Do not alter a decision listed in section 16 without writing an ADR. Every statutory citation you produce must be traceable to the texts in `reference/`; never cite the law from memory.
- **Vocabulary:** "must" is a requirement, "should" is a strong default, "may" is optional. Unfamiliar words are defined in section 18.
- **Quality bar:** this is a production system that organisations will rely on for legal compliance. Nothing ships without the tests and exit criteria in sections 9 and 13. There is no "proof of concept" mode.

---

## 1. Executive summary

**What we are building.** An API service that reviews documents against India's DPDP law and returns evidence-backed findings. A client sends a document such as a consent notice, a privacy policy, a vendor data processing agreement or an internal data policy, together with a short profile of who they are. The service returns, item by item, whether each legal requirement is present, partial, absent or not applicable, with the exact sentence it relied on, the exact section of the law, a plain explanation and suggested wording. A human reviewer at the client accepts or rejects each finding. Nothing is ever auto-approved.

**Who it is for.** Any Data Fiduciary in India, in any sector: government bodies, hospitals, schools and ed-tech, e-commerce, financial services, employers, start-ups, NGOs. It is multi-tenant from day one. It is first consumed by Stark Digital's Suraksha platform and offered to other clients through the same API.

**Why this design.** Accuracy and auditability are the product. A single "is this compliant?" question to a language model fails on both: it bluffs, it is inconsistent, and it cannot show its evidence. We therefore use a **deterministic workflow** in which the model does only small, checkable jobs: name the document type, copy facts into a fixed form with quotes, and give a judgement on a handful of fuzzy items with evidence attached. Ordinary code selects the applicable requirements, marks the form against them, verifies every quote and citation, scores, and reports. A rule-based layer provides a second opinion and a fallback when the model is unavailable.

**Key decisions.**

| # | Decision | Reason |
|---|---|---|
| 1 | Open-weight models only; development through OpenRouter, production on-premise with vLLM | Client security requirements; documents must be reviewable without leaving client infrastructure |
| 2 | Mid-size models, 24 to 31 billion parameters, selected empirically among Gemma 4 31B, Qwen3.8-27B and Sarvam-M 24B | Fits a single 24 GB GPU; the architecture makes the model's job small enough that this class suffices |
| 3 | Deterministic pipeline, not an autonomous agent | Repeatability, auditability, bounded cost; the steps are known in advance |
| 4 | Extract-then-mark: the model fills a fixed fact sheet; code marks it against the checklist | Copying facts is reliable for mid-size models; marking by code never bluffs |
| 5 | Knowledge base as versioned YAML in git, derived clause by clause from the gazette texts | Reviewable by lawyers as diffs; provable coverage; every report stamped with the version used |
| 6 | Fiduciary profile is a first-class input, collected by questionnaire | The same sentence is lawful for a State body and unlawful for a private app; the law itself draws these lines |
| 7 | Every finding carries a verbatim quote with character offsets and a citation from a closed list | Turns "the model said so" into checkable evidence |
| 8 | Human review is the final gate; decisions are stored | Legal responsibility stays with the client; decisions become the evaluation set and later fine-tuning data |
| 9 | Ready-made components for plumbing, custom code only for the knowledge base, marking logic, verification and API | Manager direction; the custom parts are the product's actual value |
| 10 | No model training in Phase 1; light fine-tuning only after a measured behavioural gap and thousands of reviewer decisions | No labelled data exists today; knowledge belongs in files, not weights |

**Indicative timeline.** Phase 0, foundations and knowledge base, three weeks. Phase 1, English production version for consent notices and privacy policies, six weeks. Phase 2, Marathi and other languages, vendor agreements and internal policies, on-premise packaging, six weeks. Phase 3, continuous improvement, ongoing. A client-usable English service exists at the end of Phase 1; the full product is ready well before the 13 May 2027 statutory date.

---

## 2. DPDP background for engineers

You do not need to be a lawyer to work on this project, but you need the following mental model. The authoritative texts are in `reference/`; the register `reference/SOURCES.md` says what counts as a source.

**Two instruments.** The Act (44 sections and one Schedule of penalties) creates obligations. The Rules (23 rules and seven Schedules) say how to perform them. Most checkable detail, such as what a notice must contain or the 90-day grievance period, lives only in the Rules. Note that the final Rules are numbered differently from the January 2025 draft that many online summaries describe; use the gazette text.

**Timeline.** Act assented 11 August 2023. Rules notified 13 November 2025. Board machinery live immediately. Consent Manager registration opens 13 November 2026. All substantive obligations start 13 May 2027.

**Actors.** The individual is the **Data Principal**. The organisation deciding why and how data is processed is the **Data Fiduciary**. Anyone processing on its behalf is a **Data Processor**; the Fiduciary stays liable for the Processor. The government may designate large or sensitive organisations as **Significant Data Fiduciaries** with extra duties. The **Data Protection Board of India** enforces the law. **State** has its constitutional meaning and includes local authorities such as municipal corporations.

**Two lawful bases.** Processing requires either **consent** (sections 4 to 6, with a notice under section 5 and Rule 3) or one of the **"certain legitimate uses"** in section 7, most importantly the State providing a subsidy, benefit, service, certificate, licence or permit (7(b)), the State performing a function under law (7(c)), and employment purposes (7(i)). State processing under 7(b) must follow the standards in Rule 5 and the Second Schedule.

**Obligations that show up in documents.** Notice contents (section 5, Rule 3). Consent quality: free, specific, informed, unconditional, unambiguous, clear affirmative action, withdrawal as easy as giving (section 6). Processor contract (8(2), Rule 6(1)(f)). Accuracy (8(3)). Security safeguards with named minimums including one-year log retention (8(5), Rule 6). Breach intimation to affected people without delay and to the Board within 72 hours (8(6), Rule 7). Erasure when purpose ends, with a one-year minimum retention of data and logs after processing (8(7), 8(8), Rule 8). Published contact person (8(9), Rule 9). Grievance redressal with a published period not exceeding 90 days (8(10), 13, Rule 14(3)). Children: verifiable parental consent, no tracking or targeted advertising, with sector exemptions (9, Rules 10 to 12, Fourth Schedule). Rights of access, correction, erasure, nomination and grievance (11 to 14, Rule 14). Cross-border transfers subject to government orders (16, Rule 15). Significant Data Fiduciary duties (10, Rule 13).

**Exemptions that change verdicts.** Section 17(4): State processing is exempt from the erasure duty in 8(7) and the erasure right in 12(3). Fourth Schedule: hospitals, schools, crèches and school transport are exempt from parental consent and the tracking ban within stated conditions, as are State benefits for children, email account creation, safety location tracking and age verification. Third Schedule: inactivity-based erasure clocks bind only e-commerce with two crore users, gaming with fifty lakh, and social media with two crore.

**Penalties.** Security failures up to 250 crore rupees; breach intimation and children up to 200 crore; Significant Data Fiduciary duties up to 150 crore; everything else up to 50 crore. We use these tiers to weight severity.

**The consequence for this system.** A document cannot be judged from its text alone. The checker needs a **profile** of the organisation whose document it is reading. Section 6 of this document specifies the profile; Appendix C has the questionnaire that collects it.

---

## 3. Product definition

### 3.1 Personas

| Persona | Needs | Touchpoint |
|---|---|---|
| Client privacy officer or Data Protection Officer | Find every gap in a document before publishing; defend decisions with the law | Review screen in the client's platform; our report and decision endpoints |
| Client developer | Integrate document review into their product with little effort | REST API, OpenAPI spec, webhooks, sandbox tenant |
| Suraksha platform | Call the checker as one of its AI agents behind its own gateway | Same API, plus an adapter matching Suraksha's agent contract |
| Our operations engineer | Deploy, monitor, update the knowledge base, support on-premise installations | Install bundle, runbooks, metrics, knowledge base release process |
| Our knowledge base authors and legal reviewer | Edit checklist items safely; see what changed | YAML files, validation scripts, pull requests |

### 3.2 Scope

**Inputs.** A document as PDF (including scanned), DOCX, HTML or URL, or plain text; a tenant profile stored at onboarding with optional per-document overrides; optional document type hint and language hint. Phase 1 limits: 25 MB, 150 pages. Languages: English in Phase 1; Marathi in Phase 2; other Eighth Schedule languages after, driven by client demand.

**Document taxonomy.** The law does not define document types; it defines obligations. We define the taxonomy and anchor each type to the obligations it carries.

| Code | Document type | Legal anchors | Control groups (Appendix B) | Phase |
|---|---|---|---|---|
| T1 | Consent notice shown at the point of asking consent | s.5, s.6(3), Rule 3 | NTC | 1 |
| T2 | Privacy policy published on a website or app | s.5, s.6, s.8(9), ss.11-14, Rules 9 and 14 | NTC, PRV | 1 |
| T3 | Data processor agreement, vendor contract clauses, vendor's own policy | s.8(1), 8(2), 6(6), 8(7)(b), Rules 6(1)(f), 8(3) | PRC | 2 |
| T4 | Retention and erasure policy | s.8(7), 8(8), 17(4), Rule 8, Third Schedule | RET | 2 |
| T5 | Information security policy | s.8(5), Rule 6 | SEC | 2 |
| T6 | Breach response plan and notification templates | s.8(6), Rule 7 | BRE | 2 |
| T7 | Grievance redressal procedure | s.8(10), s.13, Rule 14(3) | GRV | 2 |
| T8 | Data Principal rights handling procedure | ss.11-14, Rule 14 | DPR | 2 |
| T9 | Children's data and age assurance policy | s.9, Rules 10-12, Fourth Schedule | CHD | 2 |
| T10 | Cross-border transfer policy | s.16, Rule 15, Rule 13(4) | XBR | 2 |
| T11 | Governance charter, DPIA and audit reports (Significant Data Fiduciaries) | s.10, Rule 13 | SDF, GOV | 3 |
| T12 | Terms of service, cookie policy, employee privacy notice | overlap sets of NTC and PRV, s.7(i) | subsets | 2 |

**Outputs.** A structured report (Appendix D) with findings, evidence, citations, explanations, remediation text, not-applicable items with reasons, counts, a configurable weighted score, and version stamps. A decisions endpoint to record reviewer actions. Optional PDF rendering in Phase 2.

**Out of scope.** Legal advice or a binding compliance verdict; auto-publishing or auto-editing client documents; Consent Manager licensing requirements (First Schedule); generating DPIAs (Suraksha has a separate agent); scanning source code for compliance; non-Indian privacy laws.

### 3.3 Non-functional requirements

| Area | Requirement |
|---|---|
| Accuracy | Targets in section 9.2, measured on the evaluation corpus on every change. Zero tolerance for invented citations or altered quotes. |
| Latency | p95 under 180 seconds for a 40-page document on the reference on-premise hardware; under 60 seconds for a two-page notice |
| Throughput | 20 concurrent reviews per worker pool on reference hardware; horizontally scalable by adding workers |
| Availability | 99.5 percent monthly for the hosted deployment; on-premise availability is the client's, with our runbooks |
| Degradation | If the model is unavailable, a rule-only report is produced and clearly labelled; the API never fails silently |
| Security | Tenant isolation at the database row level; encryption in transit and at rest; no document text in logs; secrets in a vault; see section 10 |
| Auditability | Every report reproducible from stored inputs, knowledge base version, model id and prompt hash; append-only audit log |
| Portability | Same code runs with OpenRouter in development and vLLM on-premise, by configuration only; installable without internet access after image transfer |
| Internationalisation | Findings renderable in English and Marathi; glossary-driven terminology; UTF-8 throughout; Devanagari-aware segmentation |
| Maintainability | Knowledge base editable without code changes; validation scripts guard coverage and citation integrity |

### 3.4 Guiding principles

1. The model does small jobs; code does the deciding.
2. Every finding has a verbatim quote and a citation from a closed list, or it does not exist.
3. Knowledge lives in versioned files, never in prompts or weights.
4. Profile before judgement: applicability is resolved before any marking.
5. Determinism by default: same input, same knowledge base version, same model, same output within tolerance.
6. A human gates every outcome; the system recommends, it does not decide.
7. Degrade loudly: a reduced-accuracy report is labelled as such; a silent failure is a defect.
8. Measure, do not guess: no model, prompt or rule changes without running the evaluation corpus.
9. Buy the plumbing, build the judgement: ready-made libraries for ingestion, splitting, embeddings, model access, orchestration and tracing; custom code for the knowledge base, marking, verification and API.
10. Our own compliance: we are a Data Processor for our clients and must meet Rule 6 ourselves.

---

## 4. Architecture

### 4.1 Overview

```
Client platform (Suraksha or any client)
        │  POST /v1/reviews  (document + profile)        GET /v1/reviews/{id}   webhook review.completed
        ▼
┌───────────────────────────── API layer (FastAPI) ─────────────────────────────┐
│ auth by tenant API key · idempotency · validation · enqueue · status · report  │
└──────────────────────────────┬────────────────────────────────────────────────┘
                               │ job                                  Postgres (tenants, documents,
                         Redis queue (RQ)                              reviews, findings, decisions,
                               │                                       audit_log) with row-level security
        ┌──────────────────────▼──────────────────────────────┐
        │ Worker: LangGraph pipeline (one run per review)      │
        │                                                      │
        │  1 ingest ──► 2 segment ──► 3 classify ──► 4 resolve │◄── Knowledge base (YAML, versioned)
        │                                   controls          │     atlas · controls · profiles ·
        │  5 retrieve evidence (bge-m3 + keywords, FAISS)      │     glossary · tests
        │  6 extract fact sheet (model, structured output)     │
        │  7 mark (rule interpreter) ──► 8 judge fuzzy items   │◄── Model gateway (LiteLLM)
        │  9 verify (quotes, citations, keyword 2nd opinion)   │     dev: OpenRouter · prod: vLLM
        │ 10 aggregate ──► 11 persist report ──► 12 notify     │
        │  fallback branch: rule-only when model unavailable   │
        └──────────────────────────────────────────────────────┘
   Observability: Langfuse traces (prompts, outputs), Prometheus metrics, structured logs (redacted)
```

### 4.2 Components

| Component | Responsibility | Technology | Custom or ready-made |
|---|---|---|---|
| API | Receive documents, authenticate tenants, enqueue jobs, serve status and reports, accept reviewer decisions, webhooks | FastAPI, Pydantic v2, Uvicorn | Custom, thin |
| Queue and workers | Background execution, retries, concurrency | Redis, RQ | Ready-made |
| Database | Tenants, documents, reviews, findings, decisions, audit log | PostgreSQL 16 with row-level security; pgvector optional | Ready-made; custom schema |
| Object storage | Encrypted document blobs | Local encrypted volume on-premise; S3-compatible (MinIO) where available | Ready-made |
| Ingestion | File type detection, text extraction with layout, OCR gate | Docling; Tesseract or Surya OCR with Marathi; python-magic | Ready-made |
| Segmentation | Clauses with stable ids and character offsets; heading context; language per clause | LangChain recursive splitter plus custom heading and Devanagari sentence rules; fastText language id | Mostly ready-made |
| Classification | Document type and language with confidence | Model call via gateway, structured output | Custom prompt |
| Knowledge base | Atlas, controls, profiles, glossary, tests; loader; applicability resolver; validation | YAML, git, custom loader and validators | Custom, the core asset |
| Retrieval | Per-control evidence bundles | sentence-transformers with bge-m3; FAISS in-process; BM25 keywords via rank-bm25 | Ready-made |
| Extraction | Fill the fact sheet in document windows; merge; attach quotes | Model via gateway; Instructor plus Pydantic in dev; vLLM guided decoding in prod | Custom prompts and merge logic |
| Marking engine | Interpret rule types over the fact sheet; route fuzzy items to judgement; aggregate; score | Custom Python, a few hundred lines | Custom, core logic |
| Verification | Quote exactness, citation whitelist, keyword second opinion, needs-review flags | Custom Python | Custom, core logic |
| Orchestration | Node graph with state, retries, checkpointing, fallback branch | LangGraph | Ready-made |
| Model gateway | One interface for OpenRouter in dev and vLLM in prod; timeouts; retries; cost logging | LiteLLM | Ready-made |
| Translation | Marathi to English for translate-then-judge route; glossary enforcement | IndicTrans2 (self-hosted) | Ready-made |
| Observability | Traces of every model call, metrics, alerts | Langfuse (self-hosted), Prometheus, Grafana, structured JSON logs | Ready-made |
| Evaluation | Unit snippets, field-level extraction accuracy, document-level corpus, regression | pytest, DeepEval, custom harness and HTML report | Mixed |

### 4.3 Request lifecycle

The example client is a hospital chain, MedCare, uploading its patient-app privacy policy. Profile: private company, healthcare, about two million users, children in scope, no cross-border transfers, not a Significant Data Fiduciary.

1. **Receive.** `POST /v1/reviews` with the PDF and optional hints. The API authenticates the tenant key, validates size and type, computes the document's SHA-256, stores the encrypted blob, writes a `reviews` row with status `queued`, enqueues the job and returns `202` with `review_id`. Idempotency key prevents duplicate jobs.
2. **Ingest.** The worker loads the blob, detects type, extracts text with layout using Docling. For scanned pages it runs OCR and records a per-page confidence; pages below the configured threshold are flagged. Output: normalised text plus block metadata.
3. **Segment.** Text becomes clauses: paragraphs and list items, long paragraphs split at sentence boundaries with overlap, each clause carrying its heading path, language tag, and `char_start`, `char_end` in the original text. MedCare yields 118 clauses.
4. **Classify.** One model call on the first pages returns `{doc_type: T2, confidence: 0.96, language: en}`. If confidence is below the configured threshold and no hint was given, the review is set to `needs_input` and the client is asked for the type.
5. **Resolve controls.** The knowledge base loader returns all controls for T2; the applicability resolver applies the profile switches. MedCare: 42 controls apply; 3 are excluded with reasons recorded, for example CHD-02 excluded under Fourth Schedule Part A item 1, clinical establishment providing health services.
6. **Retrieve evidence.** Clause embeddings are computed with bge-m3. For each control, the top five clauses by cosine similarity to the control's `look_for` text are unioned with clauses matching its keyword lists. Output: an evidence bundle per control.
7. **Extract fact sheet.** The document is processed in windows of about 3,000 tokens. For each window the model returns a partial fact sheet constrained to the schema, every filled field carrying quotes with clause ids. Partials are merged by field with deterministic rules (section 8.4). Every quote is immediately checked to be a verbatim substring at the stated offsets; failing quotes drop the field value to `unverified` and are logged.
8. **Mark.** The rule interpreter evaluates each applicable control against its fact sheet field using its declared rule type (section 5.3). Fuzzy controls marked `rule: model_judged` go to step 9.
9. **Judge.** For each fuzzy control, one model call receives the control text, the statute excerpt by atlas id, and the evidence quotes, and returns `{status, rationale, confidence}` under a fixed schema. MedCare: NTC-09 withdrawal ease returns `partial`, because consent was a tap in the app and withdrawal requires an email.
10. **Verify.** Citation whitelist: every statute reference in any finding must be in the control's `atlas_refs`. Keyword second opinion: the glossary keyword layer produces its own status per control; disagreement with the model or the fact sheet sets `needs_review: true` and caps confidence. Status and evidence consistency: `absent` must have no supporting quotes, `present` must have at least one.
11. **Aggregate.** Counts by severity, weighted score from tenant or default configuration, lists of present, not applicable with reasons, needs review. Stamp `kb_version`, `model_id`, `prompt_template_hash`, `method` (`hybrid` or `rule_only`).
12. **Persist and notify.** Findings and summary written to Postgres; audit log entry appended; status `completed`; webhook `review.completed` delivered with HMAC signature; Langfuse trace closed.
13. **Review.** The client's reviewer reads findings and posts decisions to `POST /v1/reviews/{id}/findings/{control_id}/decision`. Decisions are stored, audited, and exported to the evaluation dataset pipeline.

### 4.4 Degraded modes

| Condition | Behaviour | Label in report |
|---|---|---|
| Model gateway unreachable or timing out after retries | Keyword extractor fills a rough fact sheet; marking runs; judgement controls return `needs_review` | `method: rule_only`, banner text, confidence capped at 0.5 |
| Classifier confidence below threshold, no hint | Review paused with `needs_input`; client supplies type | none |
| OCR confidence below threshold on some pages | Review proceeds; affected pages listed; controls whose evidence falls on those pages get `needs_review` | `ocr_warnings` |
| Document exceeds limits | Rejected at API with `413` and guidance | none |
| Knowledge base version mismatch between API and worker | Worker refuses the job; alert raised | none, operational |

### 4.5 Multi-tenancy and isolation

- Every row in every tenant-scoped table carries `tenant_id`; Postgres row-level security policies enforce it; the application role cannot bypass them.
- API keys are hashed at rest; scopes limit keys to review, read, decide or admin.
- Documents are stored encrypted with a per-tenant data key wrapped by a master key in the vault.
- Per-tenant configuration: default profile, retention days for uploaded documents, severity weights, webhook endpoints, rate limits.
- No cross-tenant caches: embeddings and retrieval indexes are per review and discarded after completion unless the tenant enables persistence for re-review.
- On-premise installations are single-tenant by default; the same code runs with one tenant row.

### 4.6 Deployment topologies and sizing

| Topology | Use | Model serving | Notes |
|---|---|---|---|
| Developer laptop | Development and unit tests | OpenRouter via LiteLLM; only synthetic or public documents | Docker Compose: Postgres, Redis, Langfuse, API, worker |
| Shared staging | Integration tests, evaluation runs, model selection | OpenRouter or a rented GPU with vLLM | Same compose plus evaluation harness; no real client documents |
| On-premise reference node | Client production | vLLM serving the chosen model, 4-bit or FP8; embedding server; OCR | See sizing below; air-gapped knowledge base updates by signed bundle |
| Stark-hosted (optional, later) | Clients who accept hosting in India | vLLM on our GPU nodes | Requires our own DPA and residency commitments |

**Reference on-premise node.** One server with a 24 GB GPU (for example an RTX 4090 or L4 class) runs a 27 to 31 billion parameter model at 4-bit with about 16 to 20 GB of VRAM, leaving room for the embedding model. A 48 GB GPU allows FP8 and higher concurrency. CPU: 16 cores. RAM: 64 GB. Disk: 500 GB NVMe, encrypted. Services: vLLM, embedding server, API, two to four workers, Redis, Postgres, Langfuse, Prometheus. Delivered as container images with a Compose file; a systemd-unit variant is provided for clients who forbid containers.

### 4.7 Orchestration graph

LangGraph nodes, in order, with the state they read and write. State is a typed object persisted at each checkpoint so a crashed worker resumes rather than restarts.

| Node | Reads | Writes | Retry policy |
|---|---|---|---|
| `ingest` | document ref | `text`, `blocks`, `ocr_report` | 2 retries; fail review on persistent error |
| `segment` | `text`, `blocks` | `clauses[]` | none, deterministic |
| `classify` | `clauses` (first N), hints | `doc_type`, `doc_type_confidence`, `language` | 2 retries; branch to `needs_input` on low confidence |
| `resolve_controls` | `doc_type`, `profile`, kb | `controls[]`, `excluded[]` | none |
| `retrieve` | `clauses`, `controls` | `evidence{control_id: clause_ids}` | none |
| `extract` | `clauses`, schema | `fact_sheet` | per-window retry with repair prompt on schema failure; after 3 failures branch to `fallback_extract` |
| `fallback_extract` | `clauses`, glossary | `fact_sheet` (rule-based), `method=rule_only` | none |
| `mark` | `fact_sheet`, `controls` | `findings[]` (code-marked), `judge_queue[]` | none |
| `judge` | `judge_queue`, `evidence`, atlas | `findings[]` (model-marked) | 2 retries; on failure mark `needs_review` |
| `verify` | `findings`, `clauses`, `text`, glossary | `findings[]` (flags), `verification_report` | none |
| `aggregate` | `findings`, config | `summary`, stamps | none |
| `persist_notify` | all | DB rows, webhook delivery | webhook retries with backoff over 24 hours |

Edges: linear, with `classify → needs_input` (terminal until client responds) and `extract → fallback_extract → mark` on model failure. The graph definition is the single place where the pipeline order lives; prompts live in `prompts/` as versioned files, never inline.

---

## 5. Knowledge base design

The knowledge base is the product's core asset. It is a git repository of YAML files, released with a version number, loaded by the service at startup. No database holds the law.

### 5.1 Repository layout

```
kb/
  VERSION                     # e.g. 2026.11.0 ; bumped on every release
  CHANGELOG.md
  sources/                    # provenance: one record per official text, plus the text itself
    dpdp-act-2023.yaml        # url, gazette ref, date, sha256, local text path
    dpdp-rules-2025.yaml
    texts/…
  atlas/                      # the law split into addressable clauses
    act.yaml
    rules.yaml
    schedules.yaml
  controls/                   # one file per control
    NTC-01.yaml … GOV-05.yaml
  profiles/
    switches.yaml             # definition of every profile switch and its legal reason
    presets/                  # healthcare.yaml, ecommerce.yaml, government-body.yaml, …
    applicability.yaml        # rules: switch values → controls excluded or modified, with atlas refs
  factsheet/
    schema.yaml               # field definitions (mirrors the Pydantic model)
  glossary/
    terms.yaml                # EN and MR terms, keyword lists per control
  tests/
    NTC-01/pass.txt, partial.txt, fail.txt …
  scripts/
    validate.py               # coverage, citation integrity, schema checks
    build_index.py            # derived artefacts (control embeddings)
```

### 5.2 Atlas

Every section, sub-section, clause and schedule item of the Act and Rules becomes one record. Ids are stable and human-readable.

```yaml
# atlas/act.yaml (excerpt)
- id: ACT-5-1-iii
  parent: ACT-5-1
  text: "the manner in which she may make a complaint to the Board"
  binds: data_fiduciary
  document_relevant: true
  doc_types: [T1, T2]
  effective_from: 2027-05-13
  source: dpdp-act-2023
  notes: "Read with Rule 3(c)(iii)."

# atlas/rules.yaml (excerpt)
- id: RULE-14-3
  parent: RULE-14
  text: "Every Data Fiduciary and Consent Manager shall prominently publish on its website or app, or both, as the case may be, within a reasonable period not exceeding ninety days under its grievance redressal system for responding to the grievances of Data Principals and shall, for ensuring the effectiveness of the system in responding within such period, implement appropriate technical and organisational measures."
  binds: [data_fiduciary, consent_manager]
  document_relevant: true
  doc_types: [T2, T7]
  effective_from: 2027-05-13
  source: dpdp-rules-2025
  numeric_facts: {grievance_max_days: 90}
```

Rules for the atlas: text is verbatim from the gazette; every record has `document_relevant` set; a record marked `false` must carry a `reason` ("Board procedure", "penalty quantum"); `effective_from` follows Rule 1's phasing.

### 5.3 Controls

```yaml
# controls/NTC-11.yaml
id: NTC-11
title_en: Grievance channel and response period are stated, period not exceeding 90 days
title_mr: ""                       # filled in Phase 2 from the glossary
group: NTC
doc_types: [T1, T2, T7]
applies_when: []                   # empty = always, subject to doc_types
atlas_refs: [ACT-13-1, ACT-13-2, ACT-8-10, RULE-14-3]
severity: critical
penalty_tier: "₹50 crore (any other provision)"
effective_from: 2027-05-13
fact_sheet_fields: [grievance.channel, grievance.response_days]
rule:
  type: composite
  all_of:
    - {type: presence, field: grievance.channel}
    - {type: numeric_bound, field: grievance.response_days, max: 90, missing_status: absent, over_status: contradicts}
status_text:
  present: "Grievance channel and a response period of at most 90 days are stated."
  partial: "A grievance channel is stated but the response period is missing or vague."
  absent: "No grievance channel or response period is stated."
  contradicts: "A response period longer than 90 days is stated."
look_for: "how to raise a complaint or grievance with the organisation and how many days they take to respond"
fallback_keywords:
  en: ["grievance", "complaint", "grievance officer", "respond within", "days"]
  mr: []
remediation_en: >
  Add a 'Grievances' section naming the channel (email, form, phone) and stating that
  grievances are acknowledged and resolved within <N> days, where N is at most 90, and
  that unresolved grievances may be escalated to the Data Protection Board of India.
interpretation_note: null
owner: kb-team
reviewed_by: null                  # legal reviewer initials and date after sign-off
version_added: 2026.11.0
```

**Rule types the marking engine interprets.**

| Type | Semantics | Example |
|---|---|---|
| `presence` | field has a value and at least one verified quote | Board complaint route |
| `numeric_bound` | numeric field within `min`/`max`; missing and over-limit statuses configurable | grievance days ≤ 90; breach report hours ≤ 72 |
| `enumerated` | field contains at least one of `required_any` values | withdrawal means includes `link` or `in_app` |
| `cross_field` | every item in list A has a match in list B | every data item has a purpose |
| `composite` | `all_of` / `any_of` over sub-rules with status precedence | NTC-11 above |
| `model_judged` | route to judgement call with statute excerpt and evidence | plain language; comparable ease of withdrawal; bundling |
| `negative_presence` | finding if a prohibited pattern is present | consent-by-use clauses; "any purpose we deem fit" |

Status precedence for composites: `contradicts` > `absent` > `partial` > `present`. `not_applicable` is decided before marking by the applicability resolver and never by a rule.

### 5.4 Profiles

```yaml
# profiles/switches.yaml (excerpt)
- key: state_body
  question: "Is the organisation a government body or an instrumentality of the State?"
  type: boolean
  legal_basis: [ACT-2-zb, ACT-7-b, ACT-7-c, ACT-17-4, RULE-5]
- key: sector
  type: enum
  values: [healthcare, education, ecommerce, financial, gaming, social_media, government_services, employment, other]
- key: registered_users_band
  type: enum
  values: [lt_50_lakh, 50_lakh_to_2_crore, gt_2_crore]
  legal_basis: [SCH3]
- key: children_in_scope
  type: enum
  values: [yes, no, unsure]
- key: children_context
  type: enum
  values: [health_services, school_education, creche, school_transport, none]
  legal_basis: [SCH4-A]
- key: cross_border
  type: enum
  values: [yes, no, unsure]
- key: sdf_notified
  type: boolean
- key: legal_basis_mix
  type: enum
  values: [consent, legitimate_use, both, unsure]
- key: languages_published
  type: list

# profiles/applicability.yaml (excerpt)
- when: {state_body: true}
  effect: {modify: {RET-01: {severity: advisory}, DPR-03: {severity: advisory}}}
  reason: "Section 17(4): s.8(7) and s.12(3) do not apply to processing by the State."
  atlas_refs: [ACT-17-4]
- when: {sector: healthcare, children_context: health_services}
  effect: {exclude: [CHD-02, CHD-03, CHD-05]}
  reason: "Fourth Schedule Part A item 1: clinical establishments, to the extent necessary for the child's health."
  atlas_refs: [SCH4-A-1]
- when: {registered_users_band: gt_2_crore, sector: ecommerce}
  effect: {include: [RET-04, RET-05]}
  reason: "Third Schedule item 1."
  atlas_refs: [SCH3-1]
- when: {sdf_notified: false}
  effect: {exclude: [SDF-01, SDF-02, SDF-03, SDF-04, SDF-05, XBR-03]}
  reason: "Section 10 duties apply only to notified Significant Data Fiduciaries."
- when: {children_in_scope: unsure}
  effect: {include_with_note: {CHD-01: "Profile answered 'unsure'; stricter reading applied."}}
```

Presets are named bundles of switch values: `government-body`, `hospital`, `school`, `edtech`, `ecommerce-large`, `ecommerce-small`, `bank-nbfc`, `startup-app`, `employer-hr`, `ngo`. The questionnaire in Appendix C maps directly to switches.

### 5.5 Fact sheet schema

The fact sheet is the fixed form the model fills. Fields are listed in Appendix A. Every field has the same envelope:

```yaml
field:
  value: <typed value or null>
  quotes:
    - {clause_id: "c087", text: "…verbatim…", char_start: 10231, char_end: 10282}
  confidence: 0.0-1.0
  source: model | rules | merged
  verified: true | false        # set by the quote verifier
```

### 5.6 Glossary

`glossary/terms.yaml` holds English and Marathi legal terms with preferred renderings, plus per-control keyword lists in both scripts. Marathi terms are sourced from Suraksha's existing language packs and IndicTrans2 output, then human-checked once. The glossary is enforced in Marathi finding text so that "Data Protection Board" is always rendered identically.

### 5.7 Validation

`kb/scripts/validate.py` runs in CI and before every release and fails on any of:

- an atlas record without `document_relevant` or, if `false`, without `reason`;
- a `document_relevant: true` record not referenced by at least one control for each of its `doc_types` (coverage);
- a control citing an atlas id that does not exist (citation integrity);
- a control whose `fact_sheet_fields` are not in the fact sheet schema;
- a `model_judged` control without `look_for`;
- a control without the three test snippets, or whose snippets fail the rule interpreter in isolation;
- an applicability rule citing a control that does not exist;
- duplicate ids; schema violations.

### 5.8 Change management

- Semantic versioning by date: `YYYY.MM.patch`. Every report stores the version.
- A change requires a pull request with: changed files, the triggering source (notification, review feedback, legal review), updated snippets, and the validation run.
- Legal reviewer sign-off is required for new or changed controls and applicability rules; `reviewed_by` is filled in the control file.
- `effective_from` lets the report distinguish "readiness gap" (before 13 May 2027) from "statutory gap" (after).
- Monthly regulatory watch: a checklist task to scan egazette.gov.in, meity.gov.in and Board publications for notifications under the Act; findings become issues.
- Re-review: when a release changes controls, tenants may request re-review of stored documents; the report shows the delta between versions.

### 5.9 Authoring process

1. Generate the atlas skeleton from `reference/*.txt` with a script (section numbers, sub-sections, clauses, schedule rows), then annotate by hand.
2. For each `document_relevant` record, draft or map a control. Write status rules, `look_for`, remediation, keywords, and three snippets.
3. Adversarial review: give two different models the statute text and the control set and ask them to find missing or wrong items; triage every flag.
4. External cross-check: diff the control list against two published checklists; investigate every item they have that we lack.
5. Legal review and sign-off.
6. Release with changelog.

---

## 6. Data model

PostgreSQL 16. All tenant-scoped tables have `tenant_id uuid not null` and a row-level security policy `tenant_id = current_setting('app.tenant_id')::uuid`. Primary keys are UUIDv7. Timestamps are `timestamptz`. Enumerations are `varchar` with check constraints.

| Table | Purpose | Key columns |
|---|---|---|
| `tenants` | One row per client | `id, name, status, default_profile jsonb, document_retention_days int default 30, config jsonb, created_at` |
| `api_keys` | Hashed keys with scopes | `id, tenant_id, key_hash, scopes text[], label, created_at, revoked_at, last_used_at` |
| `documents` | Uploaded documents, encrypted blob reference | `id, tenant_id, sha256, filename, mime_type, size_bytes, pages, storage_uri, encryption_key_id, language_detected, uploaded_at, delete_after, deleted_at` |
| `reviews` | One review run | `id, tenant_id, document_id, status (queued, running, needs_input, completed, failed), doc_type, doc_type_confidence, doc_type_source (hint, model, human), profile jsonb, kb_version, model_id, prompt_template_hash, method (hybrid, rule_only), summary jsonb, verification_report jsonb, ocr_warnings jsonb, error jsonb, idempotency_key, created_at, started_at, finished_at` |
| `findings` | One per applicable control per review | `id, review_id, tenant_id, control_id, status, severity, evidence jsonb, rationale_en, rationale_mr, remediation_en, remediation_mr, confidence, rule_status, needs_review bool, atlas_refs text[]` |
| `excluded_controls` | Controls not applied, with reasons | `review_id, tenant_id, control_id, reason, atlas_refs text[]` |
| `decisions` | Reviewer actions | `id, finding_id, tenant_id, reviewer_ref, decision (accept, reject, edit), edited_remediation, note, created_at` |
| `model_runs` | Every model call | `id, review_id, tenant_id, node, model_id, prompt_template_hash, input_tokens, output_tokens, latency_ms, trace_id, outcome` |
| `kb_versions` | Knowledge base releases | `version, git_sha, published_at, changelog` |
| `webhooks` | Tenant endpoints | `id, tenant_id, url, secret_hash, events text[], active` |
| `webhook_deliveries` | Delivery attempts | `id, webhook_id, review_id, attempt, status_code, next_attempt_at` |
| `audit_log` | Append-only, hash-chained | `id, tenant_id, actor, action, entity, entity_id, at, payload_hash, prev_hash, hash` with `REVOKE UPDATE, DELETE` |

Retention: a scheduled job purges document blobs after `delete_after` (default 30 days from upload), keeping reviews and findings, whose quotes are the only document text retained. Tenants may set shorter retention or call `DELETE /v1/documents/{id}` at any time. Embeddings are not persisted by default.

---

## 7. API specification (v1)

Base path `/v1`. JSON everywhere except document upload, which is `multipart/form-data`. Authentication: `Authorization: Bearer <tenant api key>`. All responses carry `X-Request-Id`. Errors use RFC 7807 `application/problem+json`.

### 7.1 Endpoints

| Method and path | Purpose | Notes |
|---|---|---|
| `POST /reviews` | Submit a document for review | multipart fields: `file` or `source_url` or `text`; `doc_type` (optional, T1 to T12); `profile_override` (optional JSON); `language_hint`; `callback_url`; header `Idempotency-Key`. Returns `202 {review_id, status: "queued"}` |
| `GET /reviews/{id}` | Status and, when complete, the report | `status` one of `queued, running, needs_input, completed, failed` |
| `POST /reviews/{id}/input` | Supply missing input, for example document type | used when status is `needs_input` |
| `GET /reviews/{id}/report` | Report only; `?format=json` default, `pdf` in Phase 2 | report schema in Appendix D |
| `POST /reviews/{id}/findings/{control_id}/decision` | Record reviewer decision | body `{decision: accept|reject|edit, edited_remediation?, note?, reviewer_ref}` |
| `GET /reviews` | List reviews | filters: `status, doc_type, from, to`; paginated |
| `DELETE /documents/{id}` | Erase the stored document blob immediately | findings remain |
| `GET /controls` | Catalogue of controls | filters `doc_type`, `profile` to see what would apply |
| `GET /controls/{id}` | One control with statute excerpts | public explanation of a check |
| `GET /profiles/presets` | Preset list and switch definitions | drives the questionnaire UI |
| `PUT /tenant/profile` | Store default profile from questionnaire answers | validated against `switches.yaml` |
| `GET /kb/version` | Current knowledge base version and changelog | |
| `GET /health`, `GET /ready` | Liveness and readiness including model gateway and database checks | unauthenticated, no details leaked |

### 7.2 Webhooks

Events: `review.completed`, `review.failed`, `review.needs_input`. Payload: `{event, review_id, tenant_id, occurred_at, summary}`. Signed with `X-Signature: sha256=<HMAC of body with tenant webhook secret>` and `X-Timestamp`; receivers must reject stale timestamps. Retries with exponential backoff for 24 hours.

### 7.3 Limits and behaviour

- Document limits in Phase 1: 25 MB, 150 pages, one document per review.
- Rate limits per tenant: configurable, default 60 submissions per hour and 600 reads per minute; `429` with `Retry-After`.
- Idempotency: same key within 24 hours returns the original `review_id`.
- Versioning: breaking changes go to `/v2`; the report carries `report_schema_version`.
- Errors: `400` validation, `401` auth, `403` scope, `404`, `409` idempotency conflict, `413` too large, `415` unsupported type, `422` unprocessable document, `429`, `500`, `503` degraded (model unavailable and fallback disabled by tenant config).

---

## 8. Model layer

### 8.1 Candidates and selection

Candidates, all Apache 2.0 licensed, all served by vLLM, all available on OpenRouter for development: **Gemma 4 31B** (Google, April 2026; broadest language coverage), **Qwen3.8-27B** (Alibaba, August 2026; strongest general reasoning in class, long context), **Sarvam-M 24B** (Sarvam AI; Indian-language focus). The smaller gpt-oss-20b is a fallback candidate for constrained hardware but is weak in Indian languages.

Selection protocol (Phase 1, task 1.11): identical prompts, identical corpus, identical decoding settings. Rank by critical-control recall, then overall per-control accuracy, then extraction field F1, then latency and VRAM. Marathi results in Phase 2 may select a different model for Marathi documents; the gateway supports per-language routing. The result is recorded as ADR-007 with the full metrics table.

### 8.2 Gateway

LiteLLM provides one interface. Configuration selects the backend: `openrouter/<model>` in development, `hosted_vllm/<model>` in production. Timeouts, retries with jitter, per-tenant cost accounting and Langfuse tracing are configured once at the gateway. **Real client documents never go to OpenRouter**; development and staging use only synthetic and public documents, enforced by an environment flag that refuses tenant documents when the backend is not local.

### 8.3 Prompt rules

- Prompts are files in `prompts/<node>/<version>.md` with a header listing variables; the hash of the rendered template is stored on every review.
- One job per call. Extraction prompts contain the schema, the window text with clause ids, and the instruction to quote verbatim and leave unknown fields empty. Judgement prompts contain one control, its statute excerpts by id, and the evidence quotes only.
- No law from memory: the prompt states that only the provided statute text may be cited.
- Output is schema-constrained: Instructor with Pydantic validation and automatic repair in development; vLLM guided decoding (JSON schema) in production.
- Temperature 0 or the model's deterministic setting; fixed seeds where supported.
- Prompts are tuned only against the evaluation corpus; a prompt change is a pull request with before and after metrics.

### 8.4 Extraction pass

- Windows of about 3,000 tokens with 200-token overlap, in document order, each with its clause ids.
- Each window returns a partial fact sheet; the merge is deterministic: for scalar fields, keep the value with the highest confidence whose quote verifies, record conflicts; for list fields, union by normalised value, keep all quotes; for numeric fields, prefer the explicit number over text.
- Quote verification happens immediately: exact substring match at the stated offsets after Unicode normalisation; a near-miss within a small edit distance is re-aligned and corrected; anything else is dropped and logged as a model error metric.
- Documents under about 4,000 tokens are processed in one window.

### 8.5 Judgement calls

- Only controls with `rule: model_judged`, typically six to ten per document.
- Output schema: `{status: present|partial|absent|contradicts, rationale: string, confidence: number, cited_atlas_ids: [..]}`; cited ids outside the control's `atlas_refs` fail verification.
- The prompt names the comparison baseline where relevant, for example how consent was given in the same document when judging ease of withdrawal.

### 8.6 Multilingual strategy

Phase 2 evaluates two routes on the Marathi corpus: native reading by the selected model, and translate-then-judge, where Marathi clauses are translated to English with IndicTrans2 for extraction and judgement while quotes are taken from the original clauses by alignment. The route with higher field-level F1 and status accuracy per language is chosen and recorded as ADR-008. Finding text is rendered in both languages using the glossary; Marathi keyword lists power the fallback layer.

### 8.7 Fine-tuning policy

No training in Phases 0 to 2. Fine-tuning is considered only when all three hold: the evaluation corpus shows a gap; the gap is behavioural (schema violations, missed or altered quotes, weak Marathi extraction, miscalibrated judgements), not a missing rule; and at least a few thousand reviewer-labelled examples exist. The method is light supervised fine-tuning of the extraction task on the chosen open model, optionally preference tuning of the judgement step from accept and reject pairs, evaluated on the held-out corpus, and deployed on-premise. Knowledge (law text, thresholds, applicability) is never fine-tuned in. Training never uses tenant data without written consent recorded in the tenant configuration.

---

## 9. Evaluation and quality

### 9.1 Test pyramid

| Level | What is tested | How | Runs |
|---|---|---|---|
| Unit | Every control's rule against its three snippets; rule interpreter; verifier; merge logic; applicability resolver; segmentation offsets | pytest | every commit |
| Component | Extraction field accuracy on labelled documents; classifier accuracy; retrieval recall (is the gold clause in the evidence bundle) | harness | every pull request touching prompts, models or retrieval |
| End to end | Full pipeline on the evaluation corpus; per-control status accuracy; report schema | harness, DeepEval for judgement rationales | nightly and before release |
| Adversarial | "Right words, wrong meaning" cases; prompt-injection text inside documents; contradictory clauses; scanned and two-column PDFs | curated set | before release |
| Regression | Stored reports for the corpus compared across knowledge base, prompt and model versions | harness diff | before release |
| Load and resilience | 20 concurrent reviews; model gateway outage; worker crash mid-run | locust, chaos scripts | before release |

### 9.2 Metrics and targets

| Metric | Definition | Phase 1 target (English) | Phase 2 target (adds Marathi) |
|---|---|---|---|
| Critical recall | Of critical controls truly absent or contradicted in the corpus, share we report as absent, partial or contradicts | ≥ 0.95 | ≥ 0.95 EN, ≥ 0.90 MR |
| Critical false alarm rate | Of critical controls truly present, share we report as absent or contradicts | ≤ 0.05 | ≤ 0.07 MR |
| Per-control status accuracy | Exact match of status across all applicable controls | ≥ 0.88 | ≥ 0.90 EN, ≥ 0.82 MR |
| Extraction field F1 | Per fact sheet field, value correctness against gold | ≥ 0.90 | ≥ 0.90 EN, ≥ 0.80 MR |
| Quote exactness | Quotes that are verbatim substrings at stated offsets | 1.00 (enforced) | 1.00 |
| Citation validity | Citations within the control's allowed atlas ids | 1.00 (enforced) | 1.00 |
| Classifier accuracy | Document type correct | ≥ 0.95 | ≥ 0.95 |
| Needs-review rate | Share of findings flagged for human review | ≤ 0.15 | ≤ 0.15 |
| Reviewer acceptance | Share of findings accepted or edited rather than rejected, after three months of use | ≥ 0.85 | ≥ 0.85 |
| Latency | p95 for 40 pages on reference hardware | ≤ 180 s | ≤ 180 s |
| Fallback coverage | Share of controls receiving a status in rule-only mode | ≥ 0.70 | ≥ 0.70 |

Releases are blocked if any enforced metric fails or any target regresses by more than two points without an ADR accepting it.

### 9.3 Evaluation corpus

- **Synthetic set, Phase 0:** 40 documents across a matrix of sectors (government, healthcare, education, e-commerce, financial, start-up, NGO, employer) × types (T1, T2 in Phase 0; T3 to T10 in Phase 2) × compliance level (compliant, partially compliant, pre-DPDP) × language (English; Marathi in Phase 2). Generated with a strong model from detailed briefs, then hand-edited so that each document has a gold fact sheet and gold statuses per control.
- **Real set:** the public documents in `samples/` (hospital, e-commerce, ed-tech, fintech, bank, SaaS processor agreement, municipal app), labelled by hand. Grows as clients consent to contribute anonymised documents.
- **Labelling format:** one YAML file per document with `gold_fact_sheet` and `gold_findings: {control_id: status}` plus `gold_clause_ids` for key fields. A labelling guide defines how to judge partial versus absent.
- **Split:** 70 percent development, 30 percent held out and never used for prompt tuning. The held-out score is the headline.
- **Adversarial additions:** documents that mention the right terms but violate the rule, for example "you may withdraw consent by registered post within 180 days"; documents containing instructions aimed at the model, which must be ignored.

### 9.4 Human review loop

Reviewer decisions are exported weekly into the dataset pipeline with document hashes, control ids, model status, human decision and edits. Quarterly, a sample is re-labelled to measure reviewer consistency. Controls with low acceptance are examined first for knowledge base defects, then prompt defects, then model defects, in that order.

---

## 10. Security, privacy and the product's own compliance

We process documents that may contain personal data on behalf of clients; under DPDP we are a Data Processor and the client is the Data Fiduciary. The product must itself satisfy Rule 6.

| Rule 6 element | Our implementation |
|---|---|
| 6(1)(a) encryption, masking, tokens | AES-256-GCM for document blobs with per-tenant keys wrapped by a vault master key; TLS 1.2 or higher everywhere; database encryption at rest; no personal data in URLs |
| 6(1)(b) access control | Tenant API keys with scopes; row-level security; admin access via SSO with MFA; least-privilege service roles; no shared accounts |
| 6(1)(c) logs, monitoring, review | Append-only hash-chained audit log; access logs; alerting on anomalies; quarterly access review |
| 6(1)(d) continuity | Nightly encrypted backups; tested restore; documented RPO 24 hours, RTO 8 hours for hosted; runbooks for on-premise |
| 6(1)(e) one-year log retention | Audit and access logs retained one year minimum, separately from document blobs which default to 30 days |
| 6(1)(f) processor contract | Our standard Data Processing Agreement with clients, including breach notification to the client without delay, sub-processor disclosure, erasure and return at exit, assistance with Data Principal requests |
| 6(1)(g) technical and organisational measures | Security review before GA; dependency pinning and vulnerability scanning in CI; SBOM per release; secure coding checklist; annual penetration test; incident response plan with the Rule 7 timelines pre-filled |

Additional controls: no document text in application logs (redaction middleware, enforced by tests); prompt and output traces in Langfuse are tenant-scoped and purged with the document; no training on tenant data without recorded consent; development and staging never receive real client documents; on-premise installations make no outbound calls except an optional, client-approved update check; signed release artefacts and signed knowledge base bundles; secrets never in images or repositories.

---

## 11. Observability and operations

- **Tracing:** every model call and every pipeline node traced in Langfuse with review id, node, model id, prompt hash, tokens, latency, outcome. Document text in traces is limited to clause ids plus quotes and is purged with the document.
- **Metrics (Prometheus):** reviews by status; node latencies; model latency and token counts; quote verification failure rate; citation rejection rate; needs-review rate; fallback activations; queue depth; webhook delivery success; per-tenant usage.
- **Logs:** structured JSON, request id and review id on every line, redaction of document content and personal data, shipped to the client's log system on-premise.
- **Alerts:** model gateway down; fallback rate above threshold; quote failure rate above threshold; queue age above threshold; webhook failures; disk and GPU memory pressure; knowledge base version mismatch.
- **SLOs:** availability 99.5 percent monthly hosted; p95 latency per section 3.3; webhook delivery within 5 minutes for 99 percent of events.
- **Runbooks:** install and upgrade; knowledge base release and rollback; model swap; GPU node loss; database restore; tenant offboarding and erasure; incident response including client notification duties.
- **Capacity:** sizing guide per expected documents per day; one reference node handles roughly 300 forty-page reviews per day.

---

## 12. Engineering practices

**Repository layout.**

```
dpdp-checker/
  apps/api/              # FastAPI app, routers, schemas, auth, webhooks
  apps/worker/           # RQ worker entry point, LangGraph pipeline
  packages/pipeline/     # nodes: ingest, segment, classify, retrieve, extract, mark, judge, verify, aggregate
  packages/kb/           # loader, applicability resolver, validators, atlas tools
  packages/models/       # gateway config, prompt loader, schemas (fact sheet, judgement)
  packages/eval/         # harness, metrics, corpus tools, report builder
  kb/                    # the knowledge base (section 5.1); may be a git submodule
  prompts/               # versioned prompt templates
  deploy/                # docker compose, systemd units, vLLM configs, install scripts
  docs/                  # this plan, ADRs, runbooks, API docs
  tests/                 # unit, component, e2e
```

**Toolchain.** Python 3.12; `uv` for dependency management with a committed lockfile; `ruff` for lint and format; `mypy` strict on packages; `pytest` with coverage gate 85 percent on `packages/`; `pre-commit` hooks; Alembic migrations; OpenAPI generated from FastAPI and committed; Conventional Commits; semantic versions for the service, date versions for the knowledge base.

**CI pipeline.** Lint and type check → unit tests → knowledge base validation → component tests with recorded model responses → build images → SBOM and vulnerability scan → nightly end-to-end evaluation on the corpus with metrics posted to the pull request → release only from tagged main with signed artefacts.

**Branching and review.** Trunk-based with short-lived branches; every change reviewed by one engineer; knowledge base changes additionally by the legal reviewer; prompt and model changes must attach evaluation results.

**Definition of done for a task.** Code and tests merged; documentation updated; metrics unchanged or improved on the corpus; runbook updated if operations change; ADR written if a decision changed.

**ADRs.** `docs/adr/NNNN-title.md` using the standard context, decision, consequences format. Initial set in section 16.

---

## 13. Phased implementation plan

Indicative calendar assumes a start on 20 October 2026 and a two-week year-end break. Weeks are working weeks.

| Phase | Weeks | Indicative dates | Outcome |
|---|---|---|---|
| 0 Foundations and knowledge base | 1 to 3 | 20 Oct to 7 Nov 2026 | Validated knowledge base backbone, evaluation corpus v1, API contract |
| 1 English production version | 4 to 9 | 10 Nov to 19 Dec 2026 | Deployable service for T1 and T2 in English, model selected, metrics met |
| 2 Multilingual, breadth, on-premise | 10 to 15 | 5 Jan to 13 Feb 2027 | Marathi, T3 to T10, on-premise bundle, Suraksha integration, first pilot |
| 3 Continuous improvement | 16 onward | from 16 Feb 2027 | Feedback loop, regulatory watch, fine-tuning gate, analytics |

### Phase 0: foundations and knowledge base (weeks 1 to 3)

| Id | Task | Deliverable | Owner |
|---|---|---|---|
| 0.1 | Repository, toolchain, CI skeleton, ADRs 001 to 006 | green CI on an empty service | AI engineer |
| 0.2 | Atlas generation script over `reference/*.txt`; hand annotation of `document_relevant`, `doc_types`, `effective_from` | `kb/atlas/*` complete for Act, Rules, Schedules | AI engineer with DPDP guide |
| 0.3 | Controls v0.2 for NTC and PRV groups with status rules, `look_for`, keywords (EN), remediation, three snippets each | about 40 control files passing validation | AI engineer with DPDP guide |
| 0.4 | Profile switches, applicability rules, ten presets; questionnaire text | `kb/profiles/*`, Appendix C finalised | AI engineer |
| 0.5 | Fact sheet schema as Pydantic and YAML; field labelling guide | `packages/models/factsheet.py`, `kb/factsheet/schema.yaml` | AI engineer |
| 0.6 | Evaluation corpus v1: 40 synthetic documents (T1, T2, English) plus the 7 real samples, gold labels for NTC and PRV | `eval/corpus/*` with labels; labelling guide | AI engineer, QA |
| 0.7 | Legal review round 1 of NTC and PRV controls and applicability rules | sign-off recorded in control files | external DPDP reviewer |
| 0.8 | API contract: OpenAPI v1 and report schema; webhook spec | `docs/api/openapi.yaml` approved | AI engineer, backend |
| 0.9 | Adversarial model review and external checklist diff of the control set | issues triaged | AI engineer |

**Exit criteria.** `validate.py` passes with 100 percent coverage of document-relevant atlas records for T1 and T2; at least 40 controls with passing snippets; corpus v1 labelled; OpenAPI approved; legal sign-off on NTC and PRV.

### Phase 1: English production version (weeks 4 to 9)

| Id | Task | Deliverable |
|---|---|---|
| 1.1 | Service skeleton: FastAPI, RQ, Postgres with Alembic and row-level security, tenants and API keys, idempotency, health and readiness | running API and worker in Compose |
| 1.2 | Ingestion: Docling integration, OCR gate with confidence, normalisation; segmentation with offsets, heading context, language id; golden tests on the samples | `ingest`, `segment` nodes |
| 1.3 | Classification node with structured output and `needs_input` branch | `classify` node |
| 1.4 | Knowledge base loader, applicability resolver, control catalogue endpoints | `resolve_controls` node, `/controls`, `/profiles/presets` |
| 1.5 | Retrieval: bge-m3 embeddings, FAISS, keyword union; retrieval recall test | `retrieve` node |
| 1.6 | Extraction: windowing, structured output through LiteLLM and Instructor, merge rules, immediate quote verification | `extract` node, merge tests |
| 1.7 | Marking engine: rule interpreter for all rule types, composite precedence, aggregation, configurable weights | `mark`, `aggregate` nodes |
| 1.8 | Judgement node with closed citation set and schema | `judge` node |
| 1.9 | Verification: citation whitelist, keyword second opinion, consistency checks, needs-review flags; fallback extraction | `verify`, `fallback_extract` nodes |
| 1.10 | LangGraph assembly with checkpointing, retries, fallback branch; persistence; webhooks with signatures; decisions endpoint; audit log | end-to-end run on the corpus |
| 1.11 | Evaluation harness and HTML report; model selection experiment across the three candidates; ADR-007 | metrics table, chosen model |
| 1.12 | Observability: Langfuse, Prometheus, redacted logging, alerts | dashboards |
| 1.13 | Security baseline: encryption, vault, retention purge job, rate limits, dependency scanning, redaction tests | security checklist signed |
| 1.14 | Documentation: README, API guide, runbook v1, labelling guide | `docs/` |

**Exit criteria.** All Phase 1 metric targets met on the held-out corpus with the chosen model; fallback mode demonstrated under a simulated gateway outage; the seven real documents produce reports judged sensible by the DPDP reviewer; load test at 20 concurrent reviews passes; security checklist complete; a client developer can integrate from the docs alone.

### Phase 2: multilingual, breadth, on-premise (weeks 10 to 15)

| Id | Task | Deliverable |
|---|---|---|
| 2.1 | Marathi: glossary from Suraksha language packs and IndicTrans2, human-checked; Marathi keyword lists; 10 Marathi corpus documents with labels | `kb/glossary`, corpus extension |
| 2.2 | Native versus translate-then-judge experiment; per-language routing; ADR-008 | chosen route, metrics |
| 2.3 | Controls for T3 to T10 (PRC, RET, SEC, BRE, GRV, DPR, CHD, XBR) with snippets; corpus extension; legal review round 2 | about 60 more controls signed off |
| 2.4 | Remediation text in EN and MR: templates plus model phrasing constrained by glossary | remediation fields populated |
| 2.5 | EN and MR consistency check between two versions of one document (GOV-03) | new node, optional |
| 2.6 | On-premise packaging: vLLM configuration for the chosen model with quantisation choice, guided decoding, embedding server, Compose and systemd variants, offline install, signed knowledge base bundle updates, sizing guide, backup and restore | install bundle validated on reference hardware |
| 2.7 | Suraksha integration: adapter to their agent contract, HMAC, webhook mapping; joint test | integration signed off by Suraksha team |
| 2.8 | PDF report rendering; report delta between knowledge base versions; re-review endpoint | `?format=pdf`, `/reviews/{id}/rereview` |
| 2.9 | Hardening: penetration test, disaster recovery drill, quota enforcement, chaos tests | reports and fixes |
| 2.10 | First client pilot with real documents on-premise; weekly review of decisions | pilot report |

**Exit criteria.** Phase 2 metrics met for English and Marathi; on-premise installation completed by an operations engineer following only the runbook; pilot client processes real documents with reviewer acceptance above 0.80 in the first month.

### Phase 3: continuous improvement (week 16 onward)

| Id | Task |
|---|---|
| 3.1 | Weekly export of reviewer decisions to the dataset; quarterly evaluation report per tenant |
| 3.2 | Fine-tuning gate review each quarter against the criteria in section 8.7; if passed, run the fine-tuning protocol and redeploy |
| 3.3 | Monthly regulatory watch; knowledge base releases; re-review notifications to tenants |
| 3.4 | Tenant analytics: common failures by document type, trend of score over time |
| 3.5 | Optional module: assisted rewrite of a document from accepted findings, built as a separate agent over the checker's tools, never replacing it |
| 3.6 | Additional languages by demand (Hindi first) |

---

## 14. Team and responsibilities

| Role | Responsibility | Allocation |
|---|---|---|
| AI engineer (lead) | Pipeline, knowledge base engineering, evaluation, model selection, this plan | full time |
| Backend engineer | API, persistence, tenancy, webhooks, security baseline | full time from Phase 1 |
| DPDP guide (Claude, in session) | Statutory interpretation, control drafting, review of knowledge base changes, teaching | on demand |
| External DPDP reviewer (lawyer or DPO) | Legal sign-off of controls and applicability rules; pilot review | about two days per phase; **to be arranged, the one unfilled role** |
| QA and evaluation engineer | Corpus labelling, harness, regression, adversarial sets | half time from Phase 0 |
| DevOps engineer | On-premise packaging, vLLM, observability, security operations | half time from Phase 1, full time in Phase 2 |
| Product owner | Priorities, client pilots, Suraksha coordination, pricing | part time |

---

## 15. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Open model hallucinates section numbers or quotes | high | high | Closed citation set and verbatim quote verification, both enforced; invented citation rate must be zero |
| Mid-size model weak at Marathi extraction | medium | high | Translate-then-judge route with IndicTrans2; Marathi corpus; glossary; possible per-language model routing; fine-tuning gate |
| Knowledge base error or gap | medium | high | Atlas-driven coverage validation; legal sign-off; adversarial review; external checklist diff; reviewer feedback loop |
| Over-flagging State or sector-exempt processing | medium | medium | Profile switches with cited legal basis; applicability tests; "unsure" handled conservatively with notes |
| Scanned or badly laid-out PDFs | medium | medium | Docling layout handling; OCR confidence gate; flagged pages; adversarial PDFs in corpus |
| Regulatory change after release | high | medium | Versioned knowledge base; `effective_from`; monthly watch; re-review endpoint |
| Clients read findings as legal advice | medium | medium | Wording, disclaimers, human gate; no "compliant" verdict ever emitted |
| On-premise hardware weaker than reference | medium | medium | Quantisation options; sizing guide; smaller fallback candidate; latency targets per hardware class |
| Real client documents leaking to a hosted model in development | low | very high | Environment flag refusing tenant documents on non-local backends; code review; tests |
| Legal reviewer unavailable | medium | high | Arrange in Phase 0; budget two days per phase; fall back to a retained law firm |
| Dependency on framework internals (LangGraph, LiteLLM) | medium | low | Thin wrappers; prompts and schemas in our files; pinned versions; exit path documented |

---

## 16. Decision log (ADR summaries)

| ADR | Decision | Status |
|---|---|---|
| 001 | Deterministic LangGraph workflow, no autonomous agent in the review path | accepted |
| 002 | Extract-then-mark architecture with a fixed fact sheet | accepted |
| 003 | Knowledge base as versioned YAML derived from an atlas of the gazette texts | accepted |
| 004 | Open-weight models only; OpenRouter in development, vLLM on-premise in production; no real client documents to hosted models | accepted |
| 005 | Python 3.12, FastAPI, RQ and Redis, PostgreSQL with row-level security, Docling, bge-m3, FAISS, LiteLLM, Instructor, Langfuse | accepted |
| 006 | Evidence rules: verbatim quotes with offsets, citations from a closed set, human gate, labelled fallback | accepted |
| 007 | Model selection result for English | pending Phase 1 experiment |
| 008 | Marathi route: native or translate-then-judge | pending Phase 2 experiment |
| 009 | Fine-tuning gate criteria | accepted as policy, section 8.7 |
| 010 | Report schema v1 and API v1 | pending Phase 0 approval |

---

## 17. Open questions

1. Who is the external DPDP reviewer, and when can they start? Needed in Phase 0 week 3.
2. Which GPU class will the first pilot client provide? Determines quantisation and latency expectations.
3. Suraksha's exact agent contract, authentication and webhook expectations; a joint session with their team is needed in Phase 2 week 1, or earlier if their Claude-assisted answers are available.
4. Pricing model and SLA tiers for external clients.
5. Whether a Stark-hosted deployment in India is offered, which triggers our own residency and DPA work.
6. Target second language after Marathi.

---

## 18. Glossary for newcomers

| Term | Meaning here |
|---|---|
| API, REST, JSON | A web address programs call; the common style of such calls; the text format of the messages |
| Tenant | One client organisation with its own isolated data and configuration |
| Queue, worker | A waiting line of jobs; a program that takes jobs from the line and runs them |
| OCR | Software that reads letters from an image of a page |
| Clause, segment | A paragraph-sized piece of the document with a stable id and character positions |
| Embedding, vector | A list of numbers representing the meaning of a sentence, so similar meanings are numerically close |
| Hybrid retrieval | Finding relevant clauses by meaning (embeddings) and by exact keywords, combined |
| LLM, model | A language model; here, an open-weight model such as Gemma 4 or Qwen3.8 |
| Prompt, token | The text sent to the model; a token is roughly three quarters of a word |
| Schema, Pydantic, structured output, guided decoding | A fixed shape for data; the Python library that defines and validates it; forcing the model's answer into that shape; the server-side way of forcing it |
| Fact sheet | The fixed form the model fills from a document, every field with quotes |
| Control | One checklist item: what a document must say, which law clause requires it, how to judge it |
| Atlas | The law split into addressable clauses with ids |
| Profile, switch, preset | Facts about the client that decide which controls apply; one such fact; a named bundle of facts |
| Marking engine | Code that applies each control's rule to the fact sheet |
| Verification | Code that checks quotes are verbatim and citations are allowed |
| Fallback, rule-only | The degraded path using keyword lists when the model is unavailable |
| LangGraph, LiteLLM, vLLM, OpenRouter | Pipeline orchestration library; one interface to many model providers; a server for running open models; a hosted gateway to open models used in development |
| Quantisation, 4-bit, FP8 | Shrinking a model's numbers to use less GPU memory with small accuracy loss |
| Fine-tuning, preference tuning | Lightly training an existing model on our examples; training it from pairs of better and worse answers |
| RLS | Row-level security: the database itself enforces that a tenant sees only its rows |
| Idempotency key | A client-supplied token so a retried request does not create a duplicate job |
| Webhook, HMAC | A callback to the client's URL when something happens; a signature proving we sent it |
| SLO, p95 | A service level objective; the latency that 95 percent of requests beat |
| ADR | Architecture decision record: a short document recording a decision and why |
| Data Fiduciary, Data Principal, Data Processor, Board, SDF | The organisation deciding how data is used; the individual; the organisation processing on another's behalf; the Data Protection Board of India; Significant Data Fiduciary |
| Notice, consent, legitimate use | The information shown before asking consent; the lawful basis built on agreement; the lawful bases that need no consent (section 7) |
| Eighth, Third, Fourth Schedule | The Constitution's list of 22 languages; the Rules' table of large platforms with inactivity erasure clocks; the Rules' table of exemptions for children's data |

---

## Appendix A: Fact sheet fields

Each field uses the envelope in section 5.5. Grouped by area; `T3` and `T4` groups are populated only for those document types.

| Group | Field | Type | Used by controls |
|---|---|---|---|
| document | `fiduciary_name`, `scope_services`, `effective_date`, `version`, `languages_available`, `pre_dpdp_markers` | text, list | NTC-01, NTC-14, PRV-01, PRV-11, PRV-12 |
| data | `data_items[]` {name, category} | list | NTC-04, NTC-06, NTC-05 |
| purposes | `purposes[]` {purpose, data_items[], service_enabled, legal_basis_claimed} | list | NTC-05, NTC-20, PRV-02 |
| consent | `consent.mechanism`, `consent.affirmative_action`, `consent.bundling_text` | text, bool, text | NTC-07, NTC-08, PRV-13 |
| withdrawal | `withdrawal.exists`, `withdrawal.means[]`, `withdrawal.link`, `withdrawal.ease_text`, `withdrawal.consequences_text` | bool, list, text | NTC-09, NTC-15 |
| rights | `rights.access`, `rights.correction`, `rights.erasure`, `rights.nomination` each {described, means, identifiers_required} | objects | NTC-10, PRV-08, DPR-* |
| grievance | `grievance.channel`, `grievance.response_days`, `grievance.escalation_text` | text, int, text | NTC-11, PRV-09, GRV-* |
| board | `board_complaint_route.described`, `board_complaint_route.text` | bool, text | NTC-12 |
| contact | `contact.role`, `contact.name`, `contact.email`, `contact.phone`, `contact.address`, `contact.in_rights_responses` | text, bool | NTC-13, PRV-10 |
| retention | `retention.statements[]`, `retention.triggers[]`, `retention.legal_exceptions[]`, `retention.inactivity_rule`, `retention.min_one_year_logs` | list, text, bool | NTC-17, RET-* |
| security | `security.measures[]` | list | PRV-03, SEC-* |
| breach | `breach.commitment_to_notify`, `breach.timeline_text`, `breach.content_elements[]` | bool, text, list | PRV-04, BRE-* |
| processors | `processors.categories[]`, `processors.contract_statement` | list, text | PRV-05, NTC-16 |
| recipients | `recipients.categories[]`, `recipients.purposes[]` | list | NTC-16 |
| cross_border | `cross_border.mentioned`, `cross_border.destinations[]`, `cross_border.safeguards_text` | bool, list, text | PRV-07, XBR-* |
| children | `children.addressed`, `children.age_threshold`, `children.parental_consent_method`, `children.tracking_or_ads_text` | bool, int, text, text | NTC-18, PRV-14, CHD-* |
| legal_basis | `legal_basis_statements[]` {basis, scope} | list | NTC-20, PRV-02, PRV-16 |
| legacy | `legacy_data_notice.present` | bool | NTC-19 |
| prohibited | `prohibited_clauses[]` {kind, text} | list | NTC-21 |
| T3 processor | `vendor.roles_defined`, `vendor.instructions_only`, `vendor.security_flowdown[]`, `vendor.breach_notice_to_df_hours`, `vendor.cease_on_withdrawal`, `vendor.erase_or_return`, `vendor.log_retention_one_year`, `vendor.subprocessor_controls`, `vendor.processing_locations[]`, `vendor.audit_rights`, `vendor.assistance_rights_requests`, `vendor.confidentiality`, `vendor.liability` | mixed | PRC-01 to PRC-14 |
| T4 internal | per policy type: `retention_policy.*`, `security_policy.*`, `breach_plan.*`, `grievance_policy.*`, `rights_sop.*`, `children_policy.*`, `xbr_policy.*`, `governance.*` | mixed | RET, SEC, BRE, GRV, DPR, CHD, XBR, SDF, GOV |

## Appendix B: Initial control list (v0.2 scope)

Severity: C critical, M major, m minor, A advisory. Statute references abbreviated; full `atlas_refs` live in the control files. Rule type in brackets where it is model-judged (MJ) or hybrid (H); all others are code-marked.

**NTC: notice and consent (T1, T2, T12)**

| Id | Title | Statute | Sev |
|---|---|---|---|
| NTC-01 | Fiduciary identity and website or app link stated | Rule 3(c); s.6(3) | M |
| NTC-02 | Notice understandable independently of other documents | Rule 3(a) | M |
| NTC-03 | Clear and plain language (MJ) | s.6(3); Rule 3(b) | M |
| NTC-04 | Itemised description of personal data | Rule 3(b)(i) | C |
| NTC-05 | Specified purposes and services enabled, per data item or group | s.5(1)(i); Rule 3(b)(ii) | C |
| NTC-06 | Data limited to what the purpose needs | s.6(1) | M |
| NTC-07 | Consent specific and unbundled (MJ) | s.6(1) | C |
| NTC-08 | Clear affirmative action; no consent by use or pre-ticked boxes | s.6(1) | C |
| NTC-09 | Withdrawal route described, ease comparable to giving (H) | s.5(1)(ii); s.6(4); Rule 3(c)(i) | C |
| NTC-10 | How to exercise rights: access, correction, erasure, nomination | s.5(1)(ii); ss.11-14; Rule 3(c)(ii); Rule 14(1) | C |
| NTC-11 | Grievance channel and response period, at most 90 days | s.13; s.8(10); Rule 14(3) | C |
| NTC-12 | How to complain to the Data Protection Board | s.5(1)(iii); Rule 3(c)(iii) | C |
| NTC-13 | Business contact of DPO or authorised person | s.6(3); s.8(9); Rule 9 | C |
| NTC-14 | Available in English or an Eighth Schedule language | s.5(3); s.6(3) | M |
| NTC-15 | Consequences of withdrawal explained; prior processing lawful | s.6(5) | m |
| NTC-16 | Recipients disclosed: categories of fiduciaries and processors, with purpose | s.11(1)(b); s.8(2) | M |
| NTC-17 | Retention and erasure statement consistent with s.8(7) and Rule 8 | s.8(7), (8); Rule 8 | M |
| NTC-18 | Children: verifiable parental consent path; no tracking or targeted ads | s.9; Rule 10 | C when children in scope |
| NTC-19 | Legacy data: notice for data collected before commencement | s.5(2) | M |
| NTC-20 | Legal basis correctly chosen per purpose | s.4; s.7 | A, C when s.7 misused |
| NTC-21 | No clause contradicting the Act (MJ) | s.6(2) | C |

**PRV: privacy policy additions (T2)**

| Id | Title | Statute | Sev |
|---|---|---|---|
| PRV-01 | Scope: portals, apps, services covered; fiduciary named | s.5; Rule 3(c) | M |
| PRV-02 | Per-purpose legal basis stated | s.4; s.7 | M |
| PRV-03 | Security safeguards statement covering Rule 6 themes | s.8(5); Rule 6 | M |
| PRV-04 | Breach notification commitment with Rule 7 elements | s.8(6); Rule 7(1) | M |
| PRV-05 | Processors engaged under contract; categories listed | s.8(2) | M |
| PRV-06 | Accuracy commitment where data drives decisions or is shared | s.8(3) | m |
| PRV-07 | Cross-border transfers disclosed with compliance commitment | s.16; Rule 15 | M when cross-border |
| PRV-08 | Rights section complete with means and identifiers | ss.11-14; Rule 14(1), (4) | C |
| PRV-09 | Grievance response period stated, at most 90 days | Rule 14(3) | C |
| PRV-10 | Contact prominently published and included in rights responses | s.8(9); Rule 9 | C |
| PRV-11 | Effective date, version, change notification | governance | m |
| PRV-12 | Governing framework is DPDP, not IT Rules 2011 vocabulary | hygiene | m, M if SPDI framework relied on |
| PRV-13 | Cookie and tracker consent not by implication | s.6(1) | M |
| PRV-14 | Children's processing addressed | s.9 | C when children in scope |
| PRV-15 | Duties of the Data Principal mentioned | s.15 | info |
| PRV-16 | State transparency: intimation with contact and rights link for s.7(b) processing | Second Schedule (g) | M when state body |

**PRC: processor agreements and vendor policies (T3)**

| Id | Title | Statute | Sev |
|---|---|---|---|
| PRC-01 | Written contract identifies roles, purposes, data, duration | s.8(2) | C |
| PRC-02 | Processor acts only on instructions; no own-purpose use | s.8(1), (2) | C |
| PRC-03 | Security safeguards flowed down with Rule 6 minimums | s.8(5); Rule 6(1)(f) | C |
| PRC-04 | Breach notice to fiduciary without delay enabling the 72-hour report | s.8(6); Rule 7 | C |
| PRC-05 | Cease processing on consent withdrawal | s.6(6) | M |
| PRC-06 | Erase or return on instruction, purpose end, exit | s.8(7)(b) | M |
| PRC-07 | Retain data and logs at least one year then erase | Rule 8(3) | M |
| PRC-08 | Sub-processors only with approval; obligations flowed down | s.8(1) | M |
| PRC-09 | Processing locations disclosed; cross-border per s.16 and Rule 15; SDF data localised | s.16; Rule 15; Rule 13(4) | M |
| PRC-10 | Assistance with rights requests, DPIA, audit | ss.11-14; s.10 | M |
| PRC-11 | Audit and inspection rights | s.8(1) | m |
| PRC-12 | Personnel confidentiality and access limitation | Rule 6(1)(b) | M |
| PRC-13 | Logs and access visibility for the fiduciary | Rule 6(1)(c) | m |
| PRC-14 | Liability and indemnity for processor-caused breach | s.8(1) | A |

**RET, SEC, BRE, GRV, DPR, CHD, XBR, SDF, GOV: internal policies (T4 to T11)**

| Id | Title | Statute | Sev |
|---|---|---|---|
| RET-01 | Retention per purpose with triggers: withdrawal, purpose served | s.8(7)(a) | C (A for State) |
| RET-02 | Legal retention exceptions enumerated with law cited | s.8(7) proviso | M |
| RET-03 | Erasure cascades to processors | s.8(7)(b) | M |
| RET-04 | Inactivity rule and Third Schedule applicability assessed | s.8(8); Rule 8(1) | M |
| RET-05 | 48-hour warning before inactivity erasure | Rule 8(2) | M when Third Schedule applies |
| RET-06 | Minimum one-year retention of data, traffic data and logs after processing | Rule 8(3) | C |
| RET-07 | State carve-out from erasure applied explicitly | s.17(4) | M when state body |
| RET-08 | Erasure method, verification, certificate | s.8(4) | m |
| SEC-01 | Encryption, obfuscation, masking or virtual tokens | Rule 6(1)(a) | C |
| SEC-02 | Access control to computer resources | Rule 6(1)(b) | C |
| SEC-03 | Logs, monitoring, review for detection and remediation | Rule 6(1)(c) | C |
| SEC-04 | Backups and continuity | Rule 6(1)(d) | M |
| SEC-05 | One-year retention of logs and personal data for investigation | Rule 6(1)(e) | C |
| SEC-06 | Processor contracts require safeguards | Rule 6(1)(f) | M |
| SEC-07 | Technical and organisational measures: ownership, review, training | Rule 6(1)(g); s.8(4) | M |
| SEC-08 | Linkage to breach plan | s.8(6) | m |
| SEC-09 | CERT-In directions alignment | advisory | A |
| BRE-01 | Breach definition matches s.2 | s.2 | M |
| BRE-02 | "Becoming aware" defined; clock start | Rule 7 | M |
| BRE-03 | Data Principal intimation without delay via account or registered channel | Rule 7(1) | C |
| BRE-04 | Data Principal content: nature, extent, timing; consequences; mitigation; safety steps; contact | Rule 7(1)(a) to (e) | C |
| BRE-05 | Board initial intimation without delay with nature, extent, timing, location, impact | Rule 7(2)(a) | C |
| BRE-06 | Board detailed report within 72 hours with the six elements | Rule 7(2)(b)(i) to (vi) | C |
| BRE-07 | Extension request process in writing | Rule 7(2)(b) | m |
| BRE-08 | Processor-to-fiduciary notification path and SLA | s.8(1); Rule 7 | M |
| BRE-09 | Roles, decision authority, DPO involvement | s.8(4) | M |
| BRE-10 | Evidence and records retained | Rule 6(1)(e) | M |
| BRE-11 | CERT-In six-hour reporting coordinated | advisory | A |
| BRE-12 | Plain-language citizen templates in EN and MR | Rule 7(1); s.5(3) | m |
| GRV-01 | Means to raise a grievance published on website and app | s.8(10); Rule 14(1) | C |
| GRV-02 | Identifiers required to verify the person stated | Rule 14(1)(b), (5) | M |
| GRV-03 | Response period published, at most 90 days | Rule 14(3) | C |
| GRV-04 | DPO or authorised contact given | s.8(9); Rule 9 | C |
| GRV-05 | Escalation to the Board after exhaustion described | s.13(3) | M |
| GRV-06 | Measures for timeliness: tracking, SLAs | Rule 14(3) | M |
| GRV-07 | Nomination requests handled | s.14; Rule 14(4) | M |
| GRV-08 | Frivolous grievances handled without chilling genuine ones | s.15 | A |
| DPR-01 | Access: summary, processing activities, identities of all recipients | s.11(1) | C |
| DPR-02 | Correction, completion, updating | s.12(1), (2) | C |
| DPR-03 | Erasure with legal exceptions; State carve-out | s.12(3); s.17(4) | C (A for State) |
| DPR-04 | Identity verification before acting | Rule 14(1)(b) | M |
| DPR-05 | Nomination | s.14 | M |
| DPR-06 | Timelines consistent with Rule 14(3) | Rule 14(3) | M |
| DPR-07 | Contact in every response | Rule 9 | M |
| DPR-08 | Consent withdrawal handling with processor cascade | s.6(6) | C |
| CHD-01 | Approach to determining whether a user is a child | s.9; Fourth Schedule B item 6 | M |
| CHD-02 | Verifiable parental consent via Rule 10(1)(a) or (b) | Rule 10(1) | C |
| CHD-03 | Due diligence that the parent is an identifiable adult | Rule 10(1) | C |
| CHD-04 | No processing detrimental to a child's well-being | s.9(2) | C |
| CHD-05 | No tracking, behavioural monitoring or targeted ads at children | s.9(3) | C |
| CHD-06 | Fourth Schedule exemptions applied only within their conditions | Rule 12; Fourth Schedule | M |
| CHD-07 | Lawful guardian verification for persons with disability | s.9(1); Rule 11 | C |
| XBR-01 | Inventory of transfers and destinations | s.16 | M |
| XBR-02 | Compliance with Central Government orders | Rule 15 | M |
| XBR-03 | SDF-notified data and traffic data kept in India | Rule 13(4) | C when SDF |
| XBR-04 | Processor location clauses | s.8(2) | M |
| SDF-01 | DPO based in India, reporting to the board, grievance contact | s.10(2)(a) | C when SDF |
| SDF-02 | Independent data auditor appointed | s.10(2)(b) | C when SDF |
| SDF-03 | DPIA and audit every 12 months; observations reported to the Board | Rule 13(1), (2) | C when SDF |
| SDF-04 | Due diligence on algorithmic software | Rule 13(3) | M when SDF |
| SDF-05 | Localisation of notified data categories | Rule 13(4) | C when SDF |
| GOV-01 | Policy owner, approver, approval date | s.8(4) | m |
| GOV-02 | Review cycle and trigger on legal change | s.8(4) | m |
| GOV-03 | EN and MR versions exist and are consistent | s.5(3) | M |
| GOV-04 | Training and awareness | s.8(4) | m |
| GOV-05 | RTI section 8(1)(j) alignment for public authorities | s.44(3) | A when state body |

## Appendix C: Tenant onboarding questionnaire

Answers map to profile switches (section 5.4). "Unsure" is allowed and applies the stricter reading with a note in reports.

1. Is your organisation a government body or an instrumentality of the State, such as a municipal corporation, a public university or a government-owned company? Yes / No. → `state_body`
2. In the documents you will submit, does your organisation decide why and how personal data is used, process it on another organisation's behalf, or both? → fiduciary / processor / both
3. Which sector best describes the service? Healthcare / Education / E-commerce / Financial services / Online gaming / Social media / Government services / Employment and HR / Other. → `sector`
4. Approximately how many registered users in India? Under 50 lakh / 50 lakh to 2 crore / Over 2 crore. → `registered_users_band`
5. Do people under 18 use the service or is data about them collected? Yes / No / Unsure. → `children_in_scope`
6. If yes, is that in the context of health services, school education, crèche care or school transport? → `children_context`
7. Does any personal data leave India, including to cloud or support providers abroad? Yes / No / Unsure. → `cross_border`
8. Has the Central Government notified your organisation as a Significant Data Fiduciary? Yes / No. → `sdf_notified`
9. Do your documents rely on consent, on a legitimate use such as a legal duty or a State service, or both? Consent / Legitimate use / Both / Unsure. → `legal_basis_mix`
10. In which languages do you publish these documents? Multiple choice. → `languages_published`

Per document: document type (T1 to T12, or "let the system decide"); product or service covered; published or draft.

## Appendix D: Report JSON (schema v1, abbreviated)

```json
{
  "report_schema_version": "1.0",
  "review_id": "0192f0a4-…",
  "tenant_id": "…",
  "document": {"sha256": "…", "doc_type": "T2", "doc_type_confidence": 0.96, "doc_type_source": "model",
               "languages": ["en"], "pages": 6, "clauses": 118, "ocr_warnings": []},
  "profile": {"state_body": false, "sector": "healthcare", "registered_users_band": "50_lakh_to_2_crore",
              "children_in_scope": "yes", "children_context": "health_services", "cross_border": "no",
              "sdf_notified": false, "legal_basis_mix": "both", "languages_published": ["en", "mr"]},
  "versions": {"kb_version": "2026.11.0", "model_id": "gemma-4-31b-it", "prompt_template_hash": "…",
               "method": "hybrid", "effective_date_basis": "2027-05-13"},
  "summary": {"applicable": 42, "present": 31, "partial": 5, "absent": 5, "contradicts": 1,
              "not_applicable": 3, "needs_review": 2,
              "by_severity": {"critical": 6, "major": 4, "minor": 1, "advisory": 0},
              "weighted_score": 58},
  "findings": [
    {"control_id": "NTC-12", "title": "How to complain to the Data Protection Board",
     "status": "absent", "severity": "critical",
     "atlas_refs": ["ACT-5-1-iii", "RULE-3-c-iii"],
     "statute_excerpts": [{"id": "ACT-5-1-iii", "text": "the manner in which she may make a complaint to the Board"}],
     "evidence": [{"clause_id": "c055", "quote": "You may write to our Grievance Officer at privacy@medcare.example.",
                   "char_start": 9120, "char_end": 9188, "verified": true}],
     "rationale_en": "The policy names a grievance officer but never tells users that unresolved grievances can be taken to the Data Protection Board of India, nor how.",
     "rationale_mr": "",
     "remediation_en": "Add: 'If your grievance is not resolved within 30 days, you may complain to the Data Protection Board of India at <link>.'",
     "remediation_mr": "",
     "confidence": 0.93, "rule_status": "absent", "needs_review": false,
     "effective_from": "2027-05-13", "gap_kind": "readiness"}
  ],
  "not_applicable": [
    {"control_id": "CHD-02", "reason": "Fourth Schedule Part A item 1: clinical establishment providing health services", "atlas_refs": ["SCH4-A-1"]}
  ],
  "disclaimer": "Assistive review. Findings require confirmation by the organisation's reviewer and are not legal advice."
}
```

## Appendix E: Prompt skeletons

**Extraction (per window).**

```
System: You are a careful clerk. You copy facts from a document into a form. You never infer facts that are not written. You quote verbatim.
Rules:
- Fill only fields supported by the text in this window. Leave others null.
- Every filled field must include at least one quote: the exact text, and the clause id it came from.
- Quotes must be copied character for character. Do not paraphrase, translate or fix typos.
- Do not cite any law. Do not judge compliance.
- Output must match the JSON schema exactly.
User:
<schema>{fact sheet JSON schema}</schema>
<window clauses="c040-c061">
[c040] (heading: Your rights) You may access, correct or delete your information by logging in…
[c041] You may withdraw your consent by emailing privacy@medcare.example.
…
</window>
```

**Judgement (per fuzzy control).**

```
System: You judge one checklist item about a document, using only the statute text and the evidence provided. You may cite only the statute ids given. If the evidence does not support a conclusion, answer "absent" and say why.
User:
<control id="NTC-09">Withdrawal of consent must be described and must be as easy as giving consent.</control>
<statute>
[ACT-6-4] …the ease of doing so being comparable to that with which such consent was given.
[RULE-3-c-i] …the particular communication link for accessing the website or app… using which such Data Principal may withdraw her consent…
</statute>
<baseline>Consent is given by tapping "Accept" in the app (clause c012).</baseline>
<evidence>
[c041] You may withdraw your consent by emailing privacy@medcare.example.
</evidence>
Answer with: {"status": present|partial|absent|contradicts, "rationale": "...", "confidence": 0-1, "cited_atlas_ids": [...]}
```

## Appendix F: Reference folder contents at the time of writing

```
reference/
  SOURCES.md                       # register of sources and cross-check material
  DPDP-Act-2023.pdf / .txt         # gazette text of the Act
  DPDP-Rules-2025-GSR-846E.pdf / .txt
  dsci-rules-summary.txt           # cross-check only
samples/
  README.md                        # index of real public documents used as test inputs
  hospital-apollo.txt, ecommerce-flipkart.txt, edtech-unacademy.txt, fintech-zerodha.txt,
  bank-icici.txt, saas-dpa-freshworks.txt, pmccare-privacy-policy.txt
```
