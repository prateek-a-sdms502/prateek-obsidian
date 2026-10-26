# DPDP Rule Gate — Implementation Plan (v1)

**Working name:** `dpdp-engine` (Suraksha product line) · **Mode first built:** `gate` · **Plan date:** 22 Oct 2026
**Statutory anchor:** DPDP Act 2023 (No. 22 of 2023) + DPDP Rules 2025 (G.S.R. 846(E), 13 Nov 2025). Consent Manager rule from 13 Nov 2026; substantive obligations from **13 May 2027**.
**Base rules = only the two gazette PDFs in the project root.** Nothing is cited from memory or from third-party summaries.

---

## 1. Context

Teams inside the organisation write their own **team rules** (internal policies/SOPs: retention, breach response, rights handling, processor terms, etc.). Every team rule must be **100% compliant with DPDP** — no contradiction, and complete for the topics it covers. A non-compliant rule must be **rejected immediately**, with no human override. Every decision must be auditable and re-checked when the law, the knowledge base or the org's profile changes.

A junior's research document (multi-tenant, advisory reviewer for external client documents) independently arrived at a sound engine core: atlas + controls knowledge base, extract-then-mark, verbatim quote verification, closed citation set, profile-based applicability. This plan **adopts that core** and reshapes everything around it for a **fail-closed internal gate**, while keeping the engine reusable so the junior's advisory multi-tenant mode can be added later on the same code.

**Decisions taken in discussion (locked):**

| Area | Decision |
|---|---|
| Product | Shared engine; **gate mode** (internal, one org) first; advisory multi-tenant mode later |
| Base rules | DPDP Act + Rules only |
| Compliant | No contradiction **and** complete for each declared topic |
| Outcome | Fail-closed auto-reject; **no override**; ambiguity = reject; technical failure ≠ reject |
| Input | Mandatory template (header + numbered statements) as **Markdown, DOCX or text-layer PDF** |
| Knowledge base | Two layers — **atlas** (verbatim law, addressable) + **controls** (checkable items) — YAML in git |
| Retrieval | Deterministic control selection; **whole team document in context**; no vector search |
| Effective dates | Check against **all** obligations now; label readiness vs statutory gap |
| Org facts | Central, versioned **org profile** owned by compliance |
| KB sign-off | Project owner (you) signs each KB release |
| Base update | Re-check all accepted rules; failures **auto-revoked** |
| LLM | Claude API and/or local OpenAI-compatible (Ollama / vLLM) via one gateway, arranged as a **primary + ≥1 cross-family verifier** ensemble |
| Multi-check | An `ACCEPT` is final only if every verifier model independently agrees (blind re-evaluation + audit of the primary's reasoning); any disagreement → reject |
| Tiny LM | Fine-tune a small model later as a reject-only "tripwire" (fact extraction, injection detection) and an instant lint; never a sole acceptor |
| Stack | Python core (FastAPI) + TypeScript web UI later on the API |
| Storage / auth | SQLite to start (Postgres-ready) · Org SSO via OIDC |
| `rules.md` | Plain-language explainer + generated obligation catalog |

---

## 2. What this plan adds beyond the junior's plan

| # | Enhancement | Why it matters for a gate |
|---|---|---|
| 1 | **Formal fail-closed verdict algebra** (§6) | Binary accept/reject must be defined precisely; junior's plan never emits a verdict |
| 2 | **Blocking only for statute-traceable controls** | Base rules are DPDP only; hygiene items (CERT-In, owner fields) can't reject a rule |
| 3 | **No keyword "rule-only" fallback in gate mode** | A degraded checker must never accept; model outage → `EVAL_FAILED`, retry |
| 4 | **Anti-gaming layer**: prompt-injection detection, header↔body consistency, model never outputs the verdict | Authors have an incentive to pass; the gate must be adversarially robust |
| 5 | **Mutation-generated bad corpus** | Every compliant example spawns violating variants (number over bound, deleted statement, "shall"→"may", injected instruction, flipped header flag); False Accept Rate must be **0** |
| 6 | **Model qualification gate** | A provider/model/prompt combination may run the gate only after passing the corpus thresholds for the active KB version; enforced at startup |
| 7 | **KB release impact preview** | Before activating a new KB version, a dry run shows exactly which accepted rules would be revoked |
| 8 | **Re-validation on org-profile change** | Applicability changes (e.g. org notified as SDF) must re-check every accepted rule |
| 9 | **Reproducible verdicts** | Cache key = (document hash, KB version, org-profile version, model id, prompt-bundle hash); identical input can never flip |
| 10 | **Model-clause library** | Pre-approved compliant statements per control, which teams can copy and which are guaranteed in the pass corpus; keeps false rejects low under "no override" |
| 11 | **Pre-check (dry run)** | Authors iterate privately before submitting; essential when there is no appeal |
| 12 | **Simpler, fewer moving parts** | Plain-Python staged pipeline (no LangGraph), DB-backed job queue (no Redis), SQLite (WAL) → Postgres by config |
| 13 | **License-aware parsing** | Avoid AGPL PyMuPDF; use permissive `pypdfium2`/`pdfplumber` |
| 14 | **Dual-key acceptance (multi-model)** | No single model can approve a rule; a second model from a different family must reach the same result blind and also sign off on the primary's reasoning (§7.3) |
| 15 | **Determinism without sampling control** | Claude API rejects `temperature`/`top_p`/`top_k` since 2026-10-21, so repeatability comes from the verdict cache, structured outputs, code-side decisions and measured verdict stability, not from temperature 0 |
| 16 | **Purpose-trained tiny LM** | Mutation corpus provides thousands of labelled examples by construction, so a small specialised model becomes feasible early, as an extra reject-only check and a sub-second lint (§7.5) |

Also corrected from the junior's document: s.17(4) State exemption also covers **s.12(2)** where no decision affecting the Data Principal is made; candidate model names/dates (e.g. "Qwen3.8-27B, Aug 2026") must be verified at qualification time, not assumed.

---

## 3. Architecture

```
                       Org SSO (OIDC) ──► roles: author · compliance_owner · auditor · admin
                                   │
   Web UI (TS, later) / CLI ──► FastAPI  /v1  ──► SQLite (WAL) via SQLAlchemy + Alembic
                                   │              rules · rule_versions · evaluations · findings
                                   │              kb_releases · org_profiles · jobs · audit_log (hash-chained)
                                   ▼
                          DB-backed job queue ──► worker process(es)
                                   │
   ┌─────────────────────── Gate pipeline (plain Python, typed state) ───────────────────────┐
   │ 1 ingest      MD / DOCX / PDF → RuleDocument (header, sections, numbered statements,     │
   │               canonical text with char offsets)                                          │
   │ 2 template    JSON-Schema header + required sections + statement numbering → or REJECT   │
   │ 3 resolve     org profile + header flags + topics → applicable controls / excluded+reason │◄─ KB bundle
   │ 4 extract     LLM fills per-topic fact sheet; every value has statement id + verbatim     │   (signed,
   │               quote (full doc in context)                                                │   versioned)
   │ 5 verify      quotes exact-match canonical text; near-miss realign; else drop value      │
   │ 6 mark        code evaluates control rules over fact sheet                               │
   │ 7 judge       LLM for model_judged controls only; statute excerpt + closed citation list │◄─ LLM gateway
   │ 8 integrity   header↔body consistency · intra-document contradiction · injection scan    │   Claude API |
   │ 9 verdict     fail-closed algebra (§6) on the primary's findings                         │   OpenAI-compat
   │10 cross-check only if primary says ACCEPT: each verifier (different model family)        │   (Ollama/vLLM)
   │               (a) blind re-run of 4–8 and (b) audit of the primary's findings;           │
   │               optional tiny-LM tripwire; any disagreement → REJECT (verification)         │
   │11 persist     findings of every model, report, audit entry, verdict cache                │
   └──────────────────────────────────────────────────────────────────────────────────────────┘
```

**Two retrieval problems, two answers.** (a) *Finding the law*: deterministic — topics + profile select an exact control list; each control carries its atlas text. No RAG anywhere near the law. The atlas's parent/child links, `atlas_refs` and applicability rules form a knowledge graph stored as YAML (KAG without a graph DB). (b) *Finding evidence in the team document*: templated rules are short, so the full document goes into each extraction/judgement call. Hybrid retrieval (bge-m3 + BM25) is deferred to advisory mode, where documents run to 150 pages.

**Engine modes.** Findings are mode-independent; the verdict policy is a pluggable layer: `GatePolicy` (binary, blocking) now, `AdvisoryPolicy` (junior's present/partial/absent statuses + human decisions + weighted score) later.

---

## 4. Knowledge base (`kb/`)

```
kb/
  VERSION                       # date-semver, e.g. 2026.11.0
  CHANGELOG.md
  sources/  act.yaml rules.yaml # gazette ref, date, sha256 of PDF and extracted text
  texts/    act.txt rules.txt   # pdftotext output + recorded normalisations
  atlas/    act.yaml rules.yaml schedules.yaml
  topics.yaml                   # topic → control groups → mandatory controls
  controls/<GROUP>/<ID>.yaml
  clauses/<ID>.md               # model-clause library (pre-approved compliant wording)
  profile/  switches.yaml applicability.yaml
  template/ header.schema.json sections.yaml
  tests/<ID>/ pass.md fail.md [partial.md]
  signoff/<VERSION>.yaml        # signer, timestamp, bundle sha256
```

**Atlas.** One record per section/sub-section/clause/schedule item, with a stable id (`ACT-8-7-a`, `RULE-7-2-b-vi`, `SCH4-A-3`), verbatim text, `binds`, `team_rule_relevant` (+ `reason` if false), `effective_from` per Rule 1 phasing, `normalisation_note`. Generated by script from `pdftotext` output, then hand-corrected. Known extraction defects to fix by hand and record: s.19–20 sub-section numbering jumble; garbled Rule 14(3) sentence; Third/Fourth Schedule table rows scrambled by column layout; Devanagari header noise.

**Out of scope for team rules (recorded with reasons):** Board constitution/salaries/procedure (s.18–26, R.17–21, Fifth/Sixth Schedules), appeals (s.29–32), penalty quantum (s.33–34, Schedule — kept only as severity metadata), Consent Manager registration (R.4, First Schedule) unless `is_consent_manager`, State/government powers (s.36–37, R.23, Seventh Schedule — except the R.8(3) retention duty it feeds).

**Topics → control groups** (header `topics` must be chosen from this list):

| Topic | Group | Key sources |
|---|---|---|
| `notice_consent` | NTC | s.5, s.6, R.3 |
| `lawful_basis` | LAW | s.4, s.7, R.5 + Second Schedule (State) |
| `security` | SEC | s.8(4)(5), R.6 |
| `breach` | BRE | s.8(6), R.7 |
| `retention` | RET | s.8(7)(8), s.17(4), R.8, Third Schedule |
| `rights` | DPR | s.11–12, s.14, R.14 |
| `grievance` | GRV | s.8(10), s.13, R.14(3), R.9 |
| `children_pwd` | CHD | s.9, R.10–12, Fourth Schedule |
| `processors` | PRC | s.8(1)(2), s.6(6), R.6(1)(f), R.8(3) |
| `cross_border` | XBR | s.16, R.15, R.13(4) |
| `sdf` | SDF | s.10, R.13 (only when org is SDF) |

Seeded from the junior's Appendix B groups, **rephrased as policy commitments** ("the policy requires breach intimation to the Board with a detailed report within 72 hours"), with non-statutory items (CERT-In, GOV hygiene) set to `blocking: false`. Estimated ~90 controls.

**Control schema** (extends the junior's): `id, title, group, topic, atlas_refs[], blocking (true iff atlas_refs non-empty), severity, penalty_tier, effective_from, applies_when, fact_sheet_fields[], rule{type…}, look_for, fix_hint, clause_ref, reviewed_by, version_added`.
Rule types: `presence`, `numeric_bound` (explicit `min`/`max`; e.g. log retention `min: 365d`, Board report `max: 72h`, grievance `max: 90d`, pre-erasure warning `min: 48h`), `enumerated`, `cross_field`, `composite`, `negative_presence` (prohibited patterns: consent by use, complaint waiver, child targeted ads), `model_judged` (plain-language commitment, withdrawal ease parity).
Precedence rules are encoded explicitly, e.g. erasure (s.8(7)) vs legal hold vs the 1-year floor (R.8(3)) vs State carve-out (s.17(4)).

**Org profile** (`profile/switches.yaml`, values set via API by `compliance_owner`, versioned): `entity_type` (private / state_instrumentality), `sector`, `third_schedule_class` (none / ecommerce_2cr / gaming_50l / social_2cr), `sdf_notified`, `is_consent_manager`, `startup_exemption_notified`, `languages_published`. `applicability.yaml` maps switch values → include/exclude/modify controls, each with `reason` + `atlas_refs`.

**Validators** (`dpdp kb validate`, run in CI; any failure blocks a release):
- each atlas text is a verbatim substring of the normalised source text;
- every `team_rule_relevant` atlas record is covered by ≥1 control, or carries an out-of-scope reason;
- control `atlas_refs` exist; every blocking control has atlas refs; fact-sheet fields exist;
- every control has pass/fail snippets that produce the expected status in isolation;
- every model clause passes its control;
- topics reference existing groups; applicability references existing controls; ids unique; schemas valid.

**Release flow:** edit → `validate` → adversarial review (Claude Opus 5.5 + one open model asked to find missing/wrong controls against the atlas; every flag triaged) → `dpdp kb build` (bundle + sha256) → `dpdp kb signoff` (you; writes `signoff/<v>.yaml`) → `POST /v1/kb/releases/{v}/impact` (dry-run over all accepted rules) → `activate` (auto-revoke failures). The engine only loads signed bundles whose hash matches.

**`rules.md`** (project root): Part 1 = hand-written plain-language explainer (the earlier summary, kept current); Part 2 = obligation catalog **generated** by `dpdp kb render` from atlas + controls (grouped by topic: id, obligation, source clause, bound, applicability, effective date, blocking). It is never edited by hand, so it cannot drift.

---

## 5. Team rule template

**Header** (YAML front-matter in MD; 2-column table in DOCX; PDFs must be exported from the DOCX template):
`rule_id, version, title, owner_team, approver, effective_from, topics[], data_principals[], data_categories[], lawful_basis{basis, s7_clause?}, processes_children_data, processes_pwd_data, uses_processors, cross_border_transfer{enabled, countries[]}`.

**Body sections (required, in order):** 1 Purpose & scope · 2 Definitions (optional) · 3 **Policy statements**, numbered `3.1, 3.2…`, one requirement each · 4 Responsibilities · 5 Exceptions (each citing its legal basis) · 6 Review & approval · 7 References.

Ingest produces a `RuleDocument` with canonical NFC text, each statement's id and char offsets. Scanned or image-only PDFs are rejected as `TEMPLATE_INVALID` (no OCR). Deliverables: `templates/team-rule.md`, `templates/team-rule.docx`, worked examples per topic.

---

## 6. Gate verdict algebra (fail-closed)

Per applicable control, the finding status is one of `satisfied | violated | missing | partial | ambiguous`, plus `excluded` (decided by applicability, with a reason).

| Condition | Outcome |
|---|---|
| Header schema / required sections / numbering invalid, or no text layer | `REJECTED` (template_invalid); no LLM call |
| Any **blocking** control `violated`, `missing`, `partial` or `ambiguous` | `REJECTED` |
| Header↔body inconsistency (e.g. body covers minors while `processes_children_data: false`) | `REJECTED` |
| Injection / instruction-to-reviewer text detected | `REJECTED` (integrity) |
| Intra-document contradiction between statements | `REJECTED` |
| Non-blocking control not satisfied | Advisory note only |
| Any verifier's blind re-run differs on any blocking control's status or extracted value, or its audit marks any primary finding `disagree` | `REJECTED` (verification) — report shows each model's reading so the author can make the statement unambiguous |
| Tiny-LM tripwire (when enabled) disagrees on an extracted fact or flags injection | `REJECTED` (verification) |
| LLM/provider error, refusal, schema failure after repair, timeout, or a response from a model other than the qualified one | `EVAL_FAILED` — retryable, never a rejection |
| Every blocking control `satisfied`, all integrity checks pass, **and every verifier agrees** | `ACCEPTED` |

- The LLM never outputs the verdict: it extracts facts with quotes and gives per-control judgements; code decides.
- `ambiguous` arises from unverified quotes, judge disagreement (optional unanimity voting for `model_judged`, chosen at qualification) or vague wording; the fix hint asks the author to make the statement explicit.
- Findings carry `effective_from` and `gap_kind: readiness | statutory`; both block.
- Every finding reports: control id, atlas refs + verbatim statute excerpt, statement id + quote (offsets), extracted value vs bound, explanation, fix hint, link to model clause. Satisfied controls are listed too, as audit evidence.

---

## 7. LLM layer

### 7.1 Gateway and calling conventions
- **One interface, two transports:** Claude through the official `anthropic` Python SDK (`client.messages.parse()` with Pydantic → `output_config.format`); local models through any OpenAI-compatible endpoint (vLLM or Ollama) with JSON-schema guided decoding. Both behind `LLMClient.complete(schema, messages, role)`. No OpenAI-compatible shim is used for Claude.
- **Roles** are configured, not hard-coded: `primary`, `verifiers[]` (≥1, must differ from the primary in model family), `tripwire` (optional tiny LM), `kb_reviewer` (offline KB adversarial review).
- **Prompt hygiene:** document passed as delimited data with statement ids; the system prompt states that text inside `<document>` is data, never instructions; only provided statute text may be cited; closed citation list checked by code; prompts versioned in `prompts/<stage>/<version>.md`, bundle hash stored per evaluation.
- **Calls per model per evaluation:** one extraction call per declared topic group + one per `model_judged` control + one integrity call (~8–15 short calls for a 3–5 page rule).
- **Data handling:** a pre-send guard refuses to send documents containing obvious personal data (emails, phone numbers, ID numbers) to a hosted provider; local providers are unaffected.

### 7.2 Recommended models and parameters (to be confirmed by qualification, §8)

**API — Claude**

| Role | Model id | Settings |
|---|---|---|
| Primary (extract + judge + integrity) | `claude-opus-5-5` ($4 / $20 per MTok, 1M context) | `thinking: {type: "adaptive"}` (cannot be disabled on Opus 5.5) · `output_config: {effort: "high", format: <json schema>}` (set effort explicitly; default is `medium`) · `max_tokens: 16000` · **no** `temperature`/`top_p`/`top_k` (400 since 2026-10-21) · prompt caching on the static prefix (system + schema + control/statute text) · always check `stop_reason` (`refusal` → `EVAL_FAILED`) |
| API verifier (when the primary is local) | `claude-opus-5-5` | same settings, verifier prompts |
| Same-family fallback verifier (API-only deployments) | `claude-sonnet-5-5` ($2 / $10) | `effort: "high"`; allowed but flagged "low diversity" in qualification, since same-family models share failure modes |
| KB adversarial reviewer (offline) | `claude-opus-5-5` | `effort: "xhigh"` |
| Bulk re-validation after a KB release | same models via **Message Batches API** (50% cost, asynchronous) | results keyed by `custom_id` |

- **Server-side refusal fallback is deliberately left off.** The skill default is to enable `fallbacks: "default"`, but in a gate a silent switch to another model would bypass qualification. The response's `model` is checked; any mismatch → `EVAL_FAILED`. It can be enabled later if the fallback model is also qualified.
- **Cost:** roughly $0.5–1.5 per evaluation for the Claude primary at `effort: high` (thinking tokens bill as output). Measured at qualification and shown in `model_calls`.

**Local — open-weight** (serve with vLLM in production, Ollama for laptops; verify the licence on each Hugging Face model card before adoption)

| Role | Model | Why |
|---|---|---|
| Local primary, or verifier when Claude is primary | **Qwen3.8-27B** (dense, ~27.8B, released 14 Aug 2026, 262K context, multimodal) | Strongest 30B-class general extractor currently reported; a different family from Claude |
| Second local verifier / fully air-gapped pair | **Gemma 4 31B** (dense, released 2 Apr 2026, 256K context) | A different family from Qwen, so a Qwen-primary + Gemma-verifier pair stays cross-family without any API |
| Fallback candidate | Qwen3.6-27B / Qwen3-32B | Older and well benchmarked on nested-JSON extraction |

**vLLM serving parameters** (per model):
```
--max-model-len 32768            # rules are short; avoids paying for 256K KV cache
--quantization fp8               # 48 GB GPU (L40S / A6000); use an AWQ 4-bit checkpoint on 24 GB (RTX 4090 / L4)
--gpu-memory-utilization 0.90
--enable-prefix-caching          # static instructions + control text shared across calls
--max-num-seqs 16
--guided-decoding-backend xgrammar
--seed 42
```
**Request parameters (local):** `temperature: 0`, `top_p: 1`, `seed: 42`, `max_tokens: 4096`, `response_format: {type: "json_schema", …}`; reasoning/thinking mode **off** for extraction. For judgement, compare thinking on vs off at qualification and keep the more stable setting. Memory: ~16–18 GB at 4-bit, ~28–30 GB at FP8 for a 27B model. One 48 GB GPU holds Qwen3.8-27B + Gemma 4 31B together at 4-bit.
**Ollama (dev):** Q4_K_M GGUF, `options: {temperature: 0, seed: 42, num_ctx: 32768}`, `format: <json schema>`.

**Recommended ensembles**

| Configuration | Primary | Verifier(s) | Use |
|---|---|---|---|
| **A (recommended)** | `claude-opus-5-5` | Qwen3.8-27B (local) | Best accuracy plus true cross-vendor independence |
| B (air-gapped) | Qwen3.8-27B | Gemma 4 31B | No data leaves the network |
| C (API-only) | `claude-opus-5-5` | `claude-sonnet-5-5` | No GPU available; lower diversity, flagged |
| + tripwire | any of the above | + fine-tuned tiny LM (§7.5) | Additional reject-only check |

### 7.3 Multi-check: dual-key acceptance
1. **Primary pass** produces findings and a provisional verdict. A provisional `REJECT` is final (fail-closed), so no extra spend.
2. On a provisional `ACCEPT`, each verifier runs two steps:
   - **Blind re-evaluation:** the verifier runs extract → mark → judge on the same document and controls **without seeing the primary's output**, which avoids anchoring. Code compares per-control status (must be `satisfied` for all blocking controls) and extracted values (numbers and units must match exactly after normalisation; supporting statement ids must overlap).
   - **Reasoning audit:** the verifier receives the primary's findings (quotes, extracted values, rationales, statute excerpts). For each blocking control it returns `{agree | disagree, reason, conflicting_statement_ids[]}`, checking that the quote actually supports the finding, the value is read correctly, the rationale matches the statute text, and no other statement contradicts it.
3. **Acceptance requires unanimity** across verifiers (and the tripwire, if enabled). Any disagreement → `REJECTED (verification)`. The report shows each model's reading, the statement involved and a fix hint ("statement 3.4 is read as 30 days by one model and 3 months by another — state the period explicitly").
4. **Shadow rejection audit (non-blocking):** a sample of primary rejections is re-run by a verifier asynchronously. Disagreements are logged as likely false rejects, feeding KB and prompt improvement. Never changes a verdict.
5. **Qualification covers the whole ensemble**, and each member is also measured alone (§8). A verifier must be a different family from the primary unless the deployment is explicitly marked "low diversity".

### 7.4 Determinism and qualification
- Claude offers no sampling control, so repeatability is achieved by:
  - the **verdict cache** (same document + KB + profile + models + prompts → stored verdict, never re-rolled);
  - structured outputs, so the shape of every answer is fixed;
  - code making every decision, with the LLM only extracting;
  - the cross-model check;
  - a measured **verdict-stability** score at qualification (5 uncached reruns per corpus document). Controls whose result flips are reworded or re-prompted until stable.
- Local models additionally run at `temperature 0` with a fixed seed.
- `dpdp eval --ensemble <config> --kb <v>` produces a signed qualification record for the (primary, verifiers, tripwire, prompt bundle, KB version) tuple. The service refuses to run the gate with an unqualified tuple.

### 7.5 Tiny LM track (fine-tuned specialist)
- **Purpose:** narrow tasks only, and **never a sole acceptor**:
  - (a) **fact tripwire**: statement → `{quantity, unit, duration, modality (shall/may/must not), negation, actor}`, cross-checked against the primary's extracted values;
  - (b) **integrity classifier**: injection or instruction-to-reviewer text, and header↔body topic consistency;
  - (c) **instant lint** for the future web editor (sub-second, can run on CPU).
- **Base models (verify licences):** Qwen3.5-4B is the strongest evidence for LoRA JSON extraction (96.6% F1 in a 2026 study); NuExtract3, a Qwen3.5-4B extraction fine-tune, is a good starting checkpoint; SmolLM2-1.7B for the CPU lint; Gemma 4 E4B as an alternative.
- **Data:**
  - KB snippets and model clauses;
  - mutation-generated violations, which are labelled by construction (the generator knows which value or word it changed);
  - synthetic team rules written by `claude-opus-5-5` in varied styles, labelled by the qualified ensemble and kept only when all models and the code checks agree (distillation).
  - The hand-labelled held-out set is **never** used for training.
- **Training:** LoRA SFT (rank 16, alpha 32, dropout 0.05, lr 2e-4, 2–3 epochs, max sequence 4096, cosine schedule) with Unsloth or TRL on one 24 GB GPU. Optionally DPO later on ensemble-disagreement pairs. The law stays in the KB; the model learns only the task format.
- **Release criteria:**
  - on held-out data: numeric-fact exact match ≥ 0.99, injection recall 1.00, false-positive rate ≤ 2%;
  - adding it must keep ensemble FRR ≤ 5%.
- **Packaging:** served via vLLM/Ollama, or GGUF Q8 for CPU lint, with a model card, dataset version and training config in the repo. Retrained after a KB major release.

---

## 8. Evaluation & qualification

**Corpus (`eval/`):** per topic ≥6 hand-written compliant rules (varied phrasing, stricter-than-required values, model clauses) and ≥6 hand-written non-compliant rules; **mutants** auto-generated from every compliant rule (numeric bound crossing, statement deletion, modal weakening "shall→may", exception without legal basis, added prohibited clause, injected instruction, header-flag flip, contradictory statement pair), each labelled with the expected failing control. 70/30 dev/held-out split; the held-out score is the headline.

| Metric | Gate threshold |
|---|---|
| False Accept Rate (hand-bad + mutants) | **0** (hard) |
| False Reject Rate (compliant set) | ≤ 3% target, ≤ 5% max |
| Per-control status accuracy | ≥ 0.95 |
| Quote exactness / citation validity | 1.00 (enforced in code) |
| Integrity detection (injection, header↔body) | 1.00 on corpus |
| Verdict stability (5 uncached reruns of the full ensemble) | identical verdict 100% (unstable controls are fixed before qualification) |
| Primary-alone False Accept Rate | measured and reported; the ensemble must strictly reduce it |
| Verifier disagreement rate on compliant set | ≤ 5% (above this, the verifier adds false rejects rather than safety) |
| Latency p95, 3–5 page rule, ensemble A | ≤ 120 s; recorded per local hardware |

Test pyramid: unit (rule interpreter, verdict algebra with property tests via `hypothesis`, verifier, parsers, resolver) → KB snippet tests → component (extraction field F1 with recorded LLM responses) → end-to-end corpus run → adversarial suite → regression diff of verdicts across KB/prompt/model versions.

---

## 9. Service: API, data, lifecycle, security

**Rule lifecycle (per version):** `SUBMITTED → EVALUATING → ACCEPTED | REJECTED | EVAL_FAILED`; `ACCEPTED → SUPERSEDED` (newer version accepted) `| REVOKED` (KB or org-profile re-validation) `| RETIRED` (team withdraws). Versions are immutable (original file, sha256, canonical text, header). Pre-checks run the same pipeline but never change rule state.

**Triggers for re-validation:** KB activation, org-profile change → re-evaluate all `ACCEPTED` versions; failures → `REVOKED`, linked to the evaluation. A model change → shadow re-evaluation and discrepancy report only (verdicts are bound to the KB version, not the model).

**API `/v1`** (OpenAPI generated and committed; TS client types generated for the future UI):

| Endpoint | Role |
|---|---|
| `POST /rules/precheck` · `POST /rules` (multipart, returns 202 + evaluation id) | author |
| `GET /evaluations/{id}` (status + report) | author (own team), auditor |
| `GET /rules`, `/rules/{rule_id}`, `/rules/{rule_id}/versions`, `POST /rules/{rule_id}/retire` | author / auditor |
| `GET /kb/version`, `/kb/topics`, `/kb/controls?topic=`, `/kb/controls/{id}`, `/kb/clauses/{id}` | all |
| `POST /kb/releases/{v}/impact`, `POST /kb/releases/{v}/activate` | compliance_owner |
| `GET/PUT /org/profile`, `POST /org/profile/impact` | compliance_owner |
| `GET /reports/coverage` (org topic coverage map), `/reports/teams`, `/reports/revocations`, `/reports/top-failures`, `/audit` | auditor, compliance_owner |
| `GET /templates/{md\|docx}` · `GET /health`, `/ready` | all / none |

**Data model (SQLAlchemy 2 + Alembic, SQLite WAL; Postgres by URL):** `teams, users` (from OIDC claims), `rules, rule_versions, evaluations` (mode, kb_version, org_profile_version, provider, model_id, prompt_bundle_hash, verdict, timings, error), `findings, excluded_controls, model_calls` (tokens, latency, outcome), `kb_releases` (bundle sha, signoff, impact summary, activated_at), `org_profile_versions, qualifications, jobs, verdict_cache, audit_log` (append-only, hash-chained; update/delete blocked by trigger).

**Security:** OIDC via Authlib, roles mapped from IdP groups; authors are scoped to their own team; secrets via env/secret store; files stored on an encrypted volume; no document text in logs (redaction, enforced by test); nightly SQLite backup (`.backup`) with tested restore; logs and audit retained ≥1 year (we follow R.6 ourselves).

---

## 10. Repository layout

```
suraksa_dpdp-compliance/
  rules.md                          # explainer + generated catalog
  DPDPA_2023_official.pdf  DPDP_Rules_2025_English_only.pdf   # unchanged originals
  kb/                               # §4
  src/dpdp_engine/
    kb/        loader, models, validators, resolver, render, bundle, signoff
    ingest/    markdown.py, docx.py, pdf.py, canonical.py   # → RuleDocument
    pipeline/  template.py, extract.py, verify.py, mark.py, judge.py, integrity.py, verdict.py, run.py
    llm/       client.py (anthropic SDK + OpenAI-compatible local), schemas.py, prompts.py,
               guards.py, ensemble.py (blind re-run, audit, unanimity), qualification.py
    policy/    gate.py, (advisory.py later)
    api/       app.py, routers/, auth.py (OIDC + RBAC), deps.py
    store/     models.py, repo.py, migrations/ (alembic)
    jobs/      queue.py (DB-backed), worker.py
    reports/   coverage.py, revocations.py, audit.py
    cli.py     # dpdp kb {validate,build,render,signoff} | check | eval | serve | worker
  prompts/     extract/ judge/ integrity/   (versioned .md)
  templates/   team-rule.md, team-rule.docx, examples/
  eval/        corpus/, mutants/ (generator), harness/, reports/
  train/       tinylm/ (dataset builder, LoRA configs, model cards)   # Phase 5b
  deploy/      vllm/ (per-model serve configs), ollama/ (Modelfiles), compose.yaml
  tests/       unit/, kb/, component/, e2e/, adversarial/
  docs/        adr/, api/openapi.yaml, runbooks/
  web/         (later — TypeScript UI)
  pyproject.toml uv.lock .pre-commit-config.yaml .github/workflows/ci.yml
```

**Toolchain:** Python 3.12, `uv`, FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, `anthropic` SDK, `openai` client (local endpoints only), python-docx, pypdfium2/pdfplumber, python-frontmatter, markdown-it-py, Authlib, structlog, ruff, mypy (strict on `src/`), pytest + hypothesis, coverage gate 85%. CI: lint → types → unit → `kb validate` → component tests (recorded LLM responses) → nightly corpus eval with metrics artifact.

---

## 11. Phased delivery (indicative; go-live target end Feb 2027, buffer before 13 May 2027)

| Phase | Weeks | Deliverables | Exit criteria |
|---|---|---|---|
| **0 Foundations** | 1–2 | `git init`, scaffold, CI, ADR-001…015; `rules.md` Part 1 (explainer); `kb/sources` + `kb/texts` with sha256; atlas generator + hand-corrected atlas | atlas verbatim check passes for 100% of records; ADRs merged |
| **1 Knowledge base** | 3–5 | `topics.yaml`; ~90 controls with rules, snippets, fix hints; model-clause library; org profile switches + applicability; template schema + MD/DOCX templates + examples; validators; `kb render` → `rules.md` Part 2; adversarial review; **sign-off of KB 2026.12.0** | `kb validate` green with full coverage of relevant atlas records; every control has passing snippets; signed bundle |
| **2 Engine** | 6–9 | ingest (MD/DOCX/PDF), template validation, resolver, LLM client (Claude + OpenAI-compatible), schemas + prompts, extract, verify, mark, judge, integrity, gate verdict, **ensemble stage (blind re-run, audit, unanimity)**, `dpdp check <file>` CLI; vLLM/Ollama serve configs for Qwen3.8-27B and Gemma 4 31B | examples accept; hand-bad rules reject with the expected controls; a seeded disagreement fixture rejects as `verification`; unit + component suites green |
| **3 Evaluation & qualification** | 8–10 (overlaps) | corpus, mutant generator, harness + HTML metrics report; qualify ensemble A (Claude + Qwen), B (Qwen + Gemma) and, if needed, C; record each member's solo metrics | §8 thresholds met on held-out set for ≥1 ensemble; qualification records stored |
| **4 Service** | 10–13 | API + OpenAPI + TS types; persistence + migrations; job queue + worker; lifecycle; OIDC/RBAC; KB release impact/activate; org-profile impact; revalidation + auto-revoke; reports; audit log | e2e: submit → accept/reject → KB release → revoke flow passes; RBAC tests pass |
| **5 Hardening & pilot** | 14–17 | adversarial/injection suite; load test; backup/restore drill; runbooks (KB release, model swap, restore); pilot with 2 teams; FRR review | pilot teams get accepted rules using only templates + fix hints; FAR still 0 |
| **5b Tiny LM** | 14–18 (parallel, off critical path) | dataset builder from KB + mutants + distillation; LoRA runs on Qwen3.5-4B / NuExtract3 (tripwire) and SmolLM2-1.7B (lint); evaluation; model cards; add as tripwire to a qualified ensemble | §7.5 release criteria met; ensemble FRR still ≤ 5% with the tripwire on |
| **6 Later** | — | TS web UI (with tiny-LM instant lint); advisory mode (junior's multi-tenant reviewer: Postgres RLS, queue, hybrid retrieval, client doc types); Marathi; cross-rule org consistency; notifications; monthly regulatory-watch task | — |

---

## 12. ADRs (initial set, `docs/adr/`)

001 shared engine, gate mode first · 002 plain-Python staged pipeline (no LangGraph) · 003 two-layer YAML KB, compiled to a signed bundle · 004 deterministic law selection, full document in context, no vector search in gate mode · 005 extract-then-mark; LLM never emits the verdict · 006 fail-closed algebra; ambiguity rejects; no override; technical failure ≠ rejection · 007 only statute-traceable controls block · 008 LLM roles (primary, cross-family verifiers, tripwire) over Claude SDK + OpenAI-compatible local; whole-ensemble qualification required · 009 check all obligations including future ones, labelled · 010 central versioned org profile; changes re-validate · 011 KB release impact preview + auto-revoke · 012 SQLite WAL + DB job queue, Postgres-ready · 013 OIDC + RBAC · 014 MD/DOCX/text-PDF template input, no OCR · 015 reproducibility cache key · 016 dual-key acceptance: unanimous blind re-evaluation + reasoning audit by cross-family verifiers · 017 Claude determinism without sampling params (cache, structured outputs, stability metric); server-side refusal fallback off · 018 tiny LM as reject-only tripwire and lint, trained on mutants + distillation, never on the held-out set.

---

## 13. Risks

| Risk | Mitigation |
|---|---|
| KB encodes an obligation wrongly → every verdict on it is wrong | verbatim atlas check, coverage validator, snippets, adversarial review, your sign-off; recommend one external DPDP lawyer review before go-live |
| High false-reject rate under "no override" frustrates teams | pre-check, model-clause library, precise fix hints, FRR threshold in qualification, template examples |
| Authors game the gate (injection, false header flags) | integrity stage, header↔body checks, code-only verdicts, adversarial corpus |
| Local model too weak | qualification blocks it; Claude remains available |
| Ensemble unanimity raises false rejects | verifier disagreement-rate threshold (≤ 5%); shadow rejection audit; disagreement reports drive prompt/KB fixes |
| Correlated errors between primary and verifier | cross-family requirement; same-family pairs flagged "low diversity" |
| Claude output varies between runs (no temperature control) | verdict cache, code-side decisions, stability metric at qualification |
| Licence terms of open models (Qwen licences have varied) | verify each Hugging Face model card before adoption; record in ADR |
| Model/version drift on the API | pinned model id, response `model` checked, re-qualification on any change |
| Regulatory change (SDF notification, s.16 blacklist, Schedule amendment) | versioned KB, impact preview, auto-revoke, monthly regulatory-watch checklist |
| Single sign-off person (bus factor) | sign-off records + CHANGELOG; designate a backup signer later |
| PDF/DOCX parsing quirks | official templates only, text-layer PDFs only, golden parser tests |

---

## 14. Verification (end-to-end)

1. `uv run dpdp kb validate` → green; `uv run dpdp kb render` regenerates `rules.md` with no diff in CI.
2. `uv run pytest` → unit, KB-snippet, component (recorded LLM) and verdict-algebra property tests pass, coverage ≥85%.
3. `uv run dpdp check templates/examples/retention-compliant.md` → `ACCEPTED` with every blocking control listed as satisfied; `uv run dpdp check eval/mutants/retention-logs-180d.md` → `REJECTED` citing the R.8(3) control with the offending statement quote.
4. `uv run dpdp eval --ensemble A --kb <v>` and `--ensemble B` → metrics report; FAR = 0, FRR ≤ 5%, verdict stability 100%, verifier disagreement ≤ 5%, and each member's solo metrics alongside.
5. Ensemble fault injection: a recorded-response fixture where the verifier reads "3 months" while the primary reads "30 days" → `REJECTED (verification)` with both readings shown; a fixture where the API returns a different `model` id → `EVAL_FAILED`.
6. `uv run dpdp serve` + `dpdp worker` with a local OIDC mock (Keycloak dev container): submit via `curl` as author → poll evaluation → report JSON; as compliance_owner run KB impact → activate → mutated-KB fixture revokes a previously accepted rule; audit log hash chain verifies.
7. Change the org profile `sdf_notified: true` → impact preview lists rules that now need SDF controls → apply → revocations appear in `/reports/revocations`.
