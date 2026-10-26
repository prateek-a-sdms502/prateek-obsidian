## What I did yesterday

1. did final check of voice CMS
2. read and started creating the DPDP compliance plan

## What I'll do today

1. Finalizing the DPDP plan
2. KT of all CMS from Amit and Sarthak

## blockers

no

---
# Complaint Resolution Verifier: Work Report (23 Oct 2026)

## Summary

We planned the **Complaint Resolution Verifier**, a service that compares a citizen's complaint photo with the "work done" photo. It decides whether the issue is **fixed, partially fixed or not fixed**, and rejects AI-generated, reused or wrong-location photos. It started as a general "is the object missing from Image 2?" question and became a PMC complaint-closure check after discussion.

The result is a detailed plan note in the vault: `Complaint Resolution Verifier.md`. It covers the architecture, costs, CMS integration, a task breakdown and starter code.

## What we did

| # | Activity | Outcome |
|---|---|---|
| 1 | Compared detection approaches: an object detector (Grounding DINO / OWLv2) vs a vision-language model | Chose a **VLM judge on Ollama Cloud**, with rules enforced in Python. A local detector isn't possible with cloud-only compute. |
| 2 | Redefined the problem | From "object removed" to **"complaint resolved"**, with 4 check types for the 84 categories: removal, repair, state change, not photo-verifiable |
| 3 | Designed the pipeline | 10 stages: intake, then metadata and duplicate checks, AI-image check, same-place check, issue list, fixed/partial verdict, decision and en/hi/mr report |
| 4 | Designed the model cascade | Small model first. The big model (`qwen3-vl:235b-cloud`) confirms every "fixed" verdict and every AI rejection, and steps in on low confidence or an uncertain location. |
| 5 | Researched Ollama Cloud pricing and models | Pro plan $20/month, includes $60 of usage credits. Per-token rate estimated from OpenRouter's price for the same model. |
| 6 | Built the cost exploration | Fixed, per-verification, one-time and people costs, plus the reduction options |
| 7 | Wrote and expanded the plan note | 11 sections, worked examples, CMS integration, operations, a 20-day task breakdown, risks and a glossary |
| 8 | Checked the starter code in the note | All 14 code blocks compile, the service code loads, 7/7 tests on the decision rules pass, and the JSON and YAML examples are valid. The full pipeline hasn't been run on a photo pair yet. |

## Key decisions

| Area | Decision |
|---|---|
| Photo source | CCTV or mobile, same place. Can arrive by any upload or WhatsApp. |
| AI-generated photos | Always auto-reject, but only when **2 models agree**. An AI-generated complaint photo rejects the whole verification. |
| Duplicate photos | Perceptual hash of every past submission (SQLite) |
| On "fixed" (v1) | AI posts a "Verified resolved by AI reviewer" comment; **an officer closes the complaint** |
| Auto-close | Later, turned on **category by category** once each proves accurate |
| Not fixed / partial / unclear | Officer review |
| Non-visual categories | `not_verifiable` |
| Languages | English, Hindi, Marathi |
| Packaging | FastAPI microservice |
| Volume | ~100 complaints/day, ~70 resolved/day; results can take minutes |

## Cost snapshot

| Item | Amount |
|---|---|
| Fixed monthly cost | **₹1,760–3,260** (Ollama Pro + optional VM) |
| Full check, worst case | **₹1.34** per verification |
| Monthly model usage, worst case | ₹3,350 (~2,500 runs), **inside the Pro credits, no extra charge** |
| Usage exceeds the credits at | ~3,900 full runs/month (≈1.9× today) |
| One-time build | ~20 working days (~4 weeks), one engineer |
| Biggest real cost | **Officer review time**: ~7–35 h/month at a 10–50% review rate |

## Files

| File | Status |
|---|---|
| `Complaint Resolution Verifier.md` | **New**: the full plan note, about 1,500 lines |
| Git | Nothing committed |

## Open items

- Confirm the Ollama Cloud per-token rates and the small-model and text-model names
- Get the list of 84 categories and fill in `categories.yaml`
- Native-speaker review of the Hindi and Marathi templates
- Tune the duplicate-photo threshold on real WhatsApp photos
- Decide how long photos are kept for audit
- Decide who builds the officer review screen (CMS team or this project)