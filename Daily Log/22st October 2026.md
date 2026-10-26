## What I did Yesterday

1. Explored the available resources for CMS and Suraksha
2. tested the voice CMS in different scenarios
3. Planned the on prim model deployment plan and costs.

## Plan for the day

1. Further explore the 3 CMS portals.
2. Explore the improved DPDP pipeline
3. Architect a new AI pipeline for DPDP compliance

## Blockers

the office network was acting up on Monday so was not able to test the voice pipeline thoroughly.

---

# Daily Report: 22 Oct 2026 (PMC Voice Bot)

## Summary
- **System restarted:** the laptop had rebooted at 10:14. I brought the bot back up and it took calls.
- **Three test calls analysed.** Two were near-silent on the caller's side.
- **The third call (Varad) found two serious bugs:**
  - The bot **said the complaint was filed but never filed it**. The complaint is lost.
  - The bot **didn't end the call** when the caller said "no / thank you".
- **Cost:** checked against our projection. It came in **lower than planned**: ₹2.03/min against ₹3.12–3.81/min.
- **Latency:** measured where the reply delay goes. Most of it is the fixed 3 s "has the caller finished?" wait.
- **No code was changed today.** Two fixes and one latency decision are waiting for approval.

---

## 1. Restarting the system
- **The laptop rebooted again at 10:14.** The bot stayed down until it was started by hand at 12:38.
- **Started:** backend and ngrok (same public address, so no Vobiz change needed).
- **Already up:** Prometheus and Grafana restarted by themselves through Docker.
- **Health checks:** local and public both 200. Running Sarvam real-time `saaras:v4` for speech-to-text, Gemini 3.1 Flash-Lite (Vertex) for replies, and Murf for the voice.
- **Network:** STARK DIGITAL_5G-1, 0% packet loss, about 6 ms to Google.
- **Bot number:** +91 80 6535 3883.

## 2. Test calls from 8180888478 (12:41 and 12:42)

| Call | What happened |
|---|---|
| 12:41 (7514cc84) | Connected; the greeting started after about 4 s; **the caller hung up 1 s into the greeting** |
| 12:42 (715ec678) | The bot played the **full 14 s greeting**; the caller hung up 2 s after it ended |

- **Our side worked normally.** The bot answered and sent its greeting clearly on both calls.
- **The audio coming from the phone was almost silent:**
  - It peaked at 2–3% of full volume.
  - The voice detector's highest reading was 0.40, below the 0.7 needed to count as speech.
  - So Sarvam heard nothing and the bot never got a turn.
- **Likely cause:** something between the phone and Vobiz (no audio heard, or a muted or very quiet microphone), not the bot.
- **Open question:** did the caller hear the greeting? Not confirmed yet.

## 3. Call with Varad (12:43–12:46, from …9855)

### What went right
- The problem was understood: no water for 7 days.
- The address was captured correctly: Veerbhadra Nagar, Baner, near the Croma showroom and Pyramid Axis.
- The address read-back was confirmed by the caller.

### 🔴 Bug 1: complaint claimed as filed but never filed
- After the name, Gemini said "आपली तक्रार नोंदवली आहे" **without calling the filing tool**.
- Nothing was saved to our database and nothing was sent to PMC's CMS. **The complaint is lost.**
- No code check stops the bot from claiming a filing that didn't happen. The existing guard only covers a different case.

### 🔴 Bug 2: the call didn't end
- After "anything else?", the caller said "Thank you", then "नाही नाही thank you", then spoke once more.
- The bot asked "आणखी काही मदत हवी आहे का?" **four times**. The caller had to hang up.
- **Root cause:** same as bug 1. Gemini replied in plain text and never called `end_call`, although the prompt says a "no" or "thank you" ends the call.
- Ending the call is left entirely to Gemini; there is no code safety net.

### Other issues
- **Name misheard:** "Varad" was transcribed as "भरत अध्यापक".
- **Garbled opening:** "Hello. कोणाला जायचं? कदापासून येतोय?" got a "नीट ऐकू आलं नाही" in reply.

## 4. Cost

### Varad's call: ₹5.00 before GST (₹5.90 with GST)

| Item | Usage | Cost |
|---|---|---|
| Phone line (Vobiz) | 2 min 28 s, billed as 3 min | ₹1.95 |
| Speech-to-text (Sarvam) | 148 s of audio | ₹1.23 |
| AI replies (Gemini 3.1 Flash-Lite) | 113k input tokens (72k cached), 229 output tokens | ₹1.08 |
| Bot voice (Murf) | 837 characters | ₹0.74 |
| **Total** | | **₹5.00** |

**The two short calls:** ₹0.83 and ₹0.95. Most of each is the 1-minute minimum phone charge.

### Against the projection (`docs/cost-analysis.md`, 25 Aug)

| Part | Projected ₹/min | Actual ₹/min |
|---|---|---|
| Phone line | ₹0.80 | ₹0.79 |
| Speech-to-text | ₹0.50 | ₹0.50 |
| **Bot voice** | **₹1.39** | **₹0.30** |
| AI replies | ₹0.43–1.12 | ₹0.44 |
| **Total** | **₹3.12–3.81** | **₹2.03** |

- **About 40% cheaper than projected.** Nearly all of the saving comes from switching the voice from Sarvam bulbul to Murf.
- **Caveats:**
  - These are estimates from our configured rates, not invoices. The Murf rate should be checked against Murf's bill.
  - The language check at the start and the address check after the call are not included. They're small.

## 5. Latency (Varad's call)

**Reply time after the caller stops speaking:** about 4 s typical, 5.8 s at the slow end.

| Stage | Time |
|---|---|
| **Waiting to be sure the caller has finished** | **3.2–5.2 s** (3 s of it is the fixed wait) |
| Gemini's first words | 0.8–1.5 s |
| Murf's first audio | ~0.1 s |

**Options to make replies faster:**

| Option | Time saved | Trade-off |
|---|---|---|
| Lower the wait to 2 s | ~1 s per reply | Slow speakers who pause mid-sentence may be cut off |
| Lower the wait to 1.5 s | ~1.5 s | Same risk, larger |
| Smart end-of-turn detection | 1–2 s | Turned off earlier because it cut off slow speakers; needs a fresh test |
| Gemini | ≤0.4 s | Already on the fastest setting |

## 6. Tooling
- **Logged in** to Claude Code with a new account, and installed several plugins.
- **Two requested commands couldn't run**, because the tools aren't installed:
  - `ant auth status`: no `ant` command on this machine.
  - `claude mcp add tokensave`: no `tokensave` program. Adding it now would register a server that fails at every start.

---

## Waiting for approval
1. **Fix: block false "filed" claims.** If a reply says the complaint is filed and nothing was filed, don't speak that line; force the filing step instead.
2. **Fix: end the call in code.** After "anything else?", a "no", "thank you" or "बस" makes the code say goodbye and hang up.
3. **Latency:** keep the 3 s wait, or try 2 s on a test call?

## Still remaining
1. **Varad's lost complaint** (no water, Veerbhadra Nagar, Baner) needs filing by hand or a callback.
2. **PMC CMS clean-up** (from 19 Oct):
   - Find and delete the duplicate PMC-2026-00007 (mobile 8180888478, 19 Oct about 16:27 and 16:32 IST).
   - Delete the old duplicates CZ000327–329.
3. **Silent-caller audio** on 8180888478: confirm whether the greeting was heard. If not, raise it with Vobiz.
4. **Auto-start after reboot:** run the backend and ngrok as system services. That's 4 manual restarts so far.
5. **Coping with network blips:** reuse the Google login token, and retry failed connections to Sarvam and Murf.
6. **Test ai-coustics noise filtering** once its licence key is added; then Picovoice and Krisp.
7. **Rotate secrets:** `SARVAM_TOOL_SECRET`, plus the keys shared in chat earlier.
8. **Commit the work:** the 19 Oct changes and 4 new test scripts are still uncommitted.
9. **Long term:** host on a cloud server in India.

## Blockers
- **Gemini sometimes skips its tools** and answers in plain text. That caused both of today's serious bugs, and fixes 1–2 above guard against it in code.
- **CMS duplicates need PMC dashboard access.** The API has no lookup or delete.
- **Vendor keys pending:** ai-coustics licence, Picovoice key, and Krisp access.

---


# Work Report — DPDP Rule Gate Planning

**Date:** 22 October 2026
**Project:** Suraksha DPDP compliance (`suraksa_dpdp-compliance`)
**Outcome:** Design discussion completed; a review-ready plan, a plain-language legal guide and verified official sources were produced. **No implementation code was written** — the plan awaits leadership approval.

---

## 1. Summary

Today we went from two legal PDFs to a full plan for an internal **DPDP Rule Gate**. The gate checks every team-authored rule or policy against India's data protection law and rejects any that is not fully compliant, with no human override.

| Area | Result |
|---|---|
| Legal analysis | Read the DPDP Act 2023 and DPDP Rules 2025 in full; found and verified three later official instruments that change the text or the dates |
| Design | Explored 12 design topics; about 40 decisions taken and recorded |
| Plan | A 790-line plan with a leadership brief (Part A), technical plan (Part B) and appendices |
| Legal guide | `rules.md`: a plain-language explainer of the Act and Rules, including the latest corrections |
| Research | Model landscape, licences, Indic-language tooling, hosted-model privacy, regulatory status |

---

## 2. What we did, in order

1. **Read both statutes in full.** We extracted the full text of the Act (44 sections + penalty Schedule) and the Rules (23 rules + 7 Schedules) and wrote a plain-language explanation of each.
2. **Defined the product.** We settled on an internal tool for one organisation. Team rules must be 100% compliant (no contradiction, and complete for their topic), and non-compliant rules are rejected immediately with no override.
3. **Shaped the design through Q&A.** Topics covered:
   - rule format (a required template with a header and numbered statements);
   - enforcement points;
   - storage and authentication;
   - effective dates;
   - catalog sign-off;
   - org profile;
   - lifecycle.
4. **Compared with the junior engineer's research.** We adopted its engine core (atlas + controls knowledge base, extract-then-mark, verbatim quotes) and reshaped it from an advisory reviewer into a fail-closed gate. We also fixed one legal omission: the s.17(4) exemption also covers s.12(2).
5. **Retrieval approach.** We chose KAG + CAG with **no RAG in the gate**, so an obligation can never be silently skipped because a search failed to find it.
6. **Multi-model checking.** We designed dual-key acceptance: Claude Opus 5.5 as primary, with **Qwen3.8-27B and Gemma 4 31B** as local verifiers from different vendors. Any outcome-relevant disagreement means rejection.
7. **Model recommendations.** We checked the Claude API reference and current open-weight models. One finding: the Claude API stopped accepting `temperature` on 21 Oct 2026, so repeatable results are now designed through caching and code-side decisions instead.
8. **Tiny-model track.** A fine-tuned small model acts as a reject-only "tripwire", not a decision-maker:
   - shadow mode until it reaches 99% per fact;
   - a span-plus-parser split, so code reads numbers and units;
   - a hard-routed **mixture of LoRA experts** by language and task.
9. **Prompt / CAG design.** We defined the cache-friendly prompt layout and estimated **about $0.40–1.00 per rule check**.
10. **Test corpus.** About 1,300 documents, including about 1,000 deliberately non-compliant "mutants" across 15 mutation families, with labels produced by construction.
11. **API and lifecycle.** Roles via SSO, rule states, knowledge-base release with impact preview, automatic revocation, and reports such as obligation coverage and readiness.
12. **25 languages.** English, the 22 Eighth Schedule languages, Rajasthani and Tulu, rolled out in tiers. The approach is native reading plus an English pivot translation, with versioned language packs.
13. **Official sources located and verified** (§4). This led to a recommended change to the definition of "base rules".
14. **Machine translation only.** No human translators are available, so the language plan was rebuilt around multi-engine consensus. A ready-to-use limitation statement was added for the plan report.

---

## 3. Key decisions

| Area | Decision |
|---|---|
| Product | Shared engine; internal **gate mode** first, advisory multi-tenant mode later |
| Verdict | Fail-closed; no override; ambiguity = reject; technical failure = retry, never a rejection |
| Input | Required template (header + numbered statements); Markdown, DOCX or text-layer PDF |
| Knowledge base | Two-layer YAML (atlas of verbatim law + ~90 controls), signed versions, owner sign-off |
| Retrieval | Deterministic selection (KAG) + whole document in context (CAG); no RAG in the gate |
| Effective dates | Check all obligations now; label readiness vs statutory gaps |
| Models | Claude Opus 5.5 primary + Qwen3.8-27B + Gemma 4 31B verifiers; unanimous acceptance |
| Pre-check | Runs the full multi-model check; unchanged passed documents are accepted from cache |
| Shadow audit | 100% of rejections re-checked in the background for false rejects |
| Tiny LM | Encoder for integrity; LoRA tripwire; mixture of LoRA experts; rented GPU for training |
| Languages | 25 languages, phased; **machine translation only**; English-authoritative fallback |
| Hosted models | Ollama Cloud only with written per-model terms on retention and region |
| Stack | Python (FastAPI) core, TypeScript UI later; SQLite to start; SSO via OIDC |
| Plan location | Edit only `so-i-am-buildin-frolicking-lecun.md` locally; nothing on the web |

---

## 4. Important findings

**Official instruments that change the base text** (verified from MeitY's signed Gazette copies):

| Instrument | Effect |
|---|---|
| Corrigendum **G.S.R. 892(E)** (10 Dec 2025) | 8 wording corrections to the English Rules; our PDF is the uncorrected print |
| Commencement **G.S.R. 843(E)** (13 Nov 2025) | Sets in-force dates for the Act's sections (immediately / 13 Nov 2026 / 13 May 2027) |
| Removal of Difficulties Order **S.O. 5458(E)** (in force 6 Oct 2026) | Amends Act s.9(1) and s.10(2)(c)(ii) ("data audit") |
| Bilingual Rules Gazette | Official Hindi text exists (pp. 1–23); our English PDF matches pp. 24–41 |

**Other findings:**
- **Timeline proposal:** MeitY floated cutting the compliance window from 18 to 12 months in January 2026. It had **not been notified** as of mid-October 2026, so it's listed as a watch item.
- **Unverified:** a possible second corrigendum "G.S.R. 113(E)"; the Act's official Hindi text; NLLB coverage of Tulu and Rajasthani.
- **Model licences:**
  - Gemma 4: Apache 2.0.
  - Qwen3.8-27B: reported as Apache 2.0; confirm from its LICENSE file.
  - IndicTrans2 and IndicBERT v2: MIT.
  - NuExtract3 and Bodhan: unconfirmed.
- **Hosted-model privacy:** Ollama Cloud says it doesn't retain prompts, but hosting is mainly in the US and an open issue questions how some models are served. Hence the "written terms" condition.

---

## 5. Files produced

| File | Location | Purpose |
|---|---|---|
| `so-i-am-buildin-frolicking-lecun.md` | project root | **The plan** — leadership brief, technical plan, appendices (the only plan file to edit) |
| `rules.md` | project root | Plain-language guide to the Act and Rules (Part 1); Part 2 to be generated from the knowledge base |
| `session-report-2026-10-22.md` | project root | This report |
| `PLAN.md` | project root | Duplicate of an earlier plan version — **awaiting your decision to delete** |
| Official Gazette PDFs | session scratch folder (not in project) | Corrigendum, commencement, bilingual Rules, Removal of Difficulties Order; to be added to `kb/sources/` in Phase 0 |
| Web doc "DPDP Rule Gate — Plan for Review" | claude.ai (private) | Partly filled before you asked to keep everything local — **awaiting your decision to delete** |

---

## 6. Decisions waiting for leadership (from the plan, Part A)

| # | Decision | Recommendation |
|---|---|---|
| D1 | Build the gate as specified | Approve |
| D2 | Base rules = Act + Rules as officially corrected and amended (replaces "two PDFs only") | Approve |
| D3 | Claude API as the primary model (no personal data leaves the network) | Approve |
| D4 | One 48 GB-class GPU server for the local verifiers | Approve; quote needed |
| D5 | Ollama Cloud only with written terms | Approve the condition |
| D6 | 25 languages, phased | Approve the phasing |
| D7 | Machine translation only, no human translators | Accept the limitation |
| D8 | Knowledge-base sign-off: owner + backup signer + one external lawyer review | Approve |
| D9 | Budget envelope (≈ $0.40–1.00 per check; GPU; ≈ $200–600 language packs) | Approve |

---

## 7. Next steps

1. Review and circulate the plan; collect decisions D1–D9.
2. Confirm whether to delete `PLAN.md` and the partly filled web doc.
3. On approval and an explicit go-ahead: Phase 0.
   - Repository setup.
   - Official sources into `kb/sources/`.
   - Consolidated legal text with the corrigendum and order applied.
   - Atlas.
   - Verify "G.S.R. 113(E)".
4. Target: English go-live in late February to early March 2027, about 10 weeks before obligations start on 13 May 2027.
