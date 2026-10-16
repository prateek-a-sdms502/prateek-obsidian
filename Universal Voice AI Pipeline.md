# Current AI Voice Pipeline (main branch) — PMC Complaint Helpline

A self-hosted voice bot, *Asha*, that takes civic complaints over a phone call in Marathi, Hindi and English (including code-mixed speech), registers them, and shows them live on an admin dashboard.

## 1. Architecture at a glance

![[Untitled Diagram-2026-10-16T06-52-45 1.png]]

## 2. Components

| Layer | What we use | Notes |
|---|---|---|
| Telephony | **Vobiz** (Indian +91 number), Twilio also supported | Raw 8 kHz audio over a websocket. Bolna (managed platform) kept as an alternative setup |
| Orchestration | **Pipecat 1.7.0** on FastAPI | One pipeline per call; every component swappable |
| Turn-taking | **Silero VAD** (+ optional Smart Turn v3) | Waits 1.3 s of silence before treating the caller as finished; 3 words needed to interrupt the bot |
| Speech-to-text | **Sarvam `saaras:v3`** | Marathi pinned (`mr-IN`); ElevenLabs, Soniox, Gladia selectable |
| LLM | **Gemini 2.5 Flash** (Google AI Studio) | OpenRouter selectable (default model there: Claude Haiku 4.5) |
| Text-to-speech | **Sarvam `bulbul:v3`** | Female voice `simran` |
| Complaint filing | **PMC CMS API**, with a local token as fallback | Complaint number read back digit by digit, twice |
| Classification | **PMC's XLM-R model** (PMC's EC2) | 78 departments; runs in the background *after* registration so the caller never waits |
| Storage & UI | SQLite (WAL) + React/Vite dashboard | Live complaint table, category badges, transcripts |

**LLM tools:** `register_complaint` and `end_call`.

## 3. Conversation flow

1. **Greeting**: fixed line, spoken without an LLM round-trip (caller can interrupt it)
2. **Complaint**: caller describes the problem; 1–2 follow-up questions
3. **Name**
4. **Mobile**: caller ID confirmed; a different number is collected digit by digit if asked
5. **Address**: area → road/society → nearby landmark
6. **Summary read-back** → caller confirms → complaint registered
7. **Complaint number** read out character by character, then once more
8. **"Anything else?"** → thank you → call ends

If the caller refuses the name or number, the complaint is still registered with what was given.

## 4. Running cost (estimate, ex-GST)

No live calls on the main branch have been logged with per-call usage, so these are estimates at current verified rates.

| Component | Rate | Per call (~3¼ min) |
|---|---|---|
| Telephony (Vobiz) | ₹0.45/min + ₹0.20/min stream, rounded up to whole minutes | ₹2.60 |
| Speech-to-text (Sarvam) | ₹30/hour | ₹1.63 |
| Text-to-speech (Sarvam bulbul:v3) | ₹3 per 1,000 characters | ₹3.16–4.63 |
| LLM (Gemini 2.5 Flash) | $0.30 in / $2.50 out per 1M tokens | ₹0.32–0.54 |
| **Total** | | **₹7.7–9.4** (₹9.1–11.1 with GST) |

That is ≈ **₹2.4–2.9 per minute**. Text-to-speech is the largest item (~40%), telephony second.

The main branch's own cost doc says ₹2.09/min. That figure missed Vobiz's stream fee and minute round-up, which were found later in the account ledger.

## 5. Known limitations

- **LLM may stop working:** `gemini-2.5-flash` already returns 404 on newly created API keys, and Google retires the 2.5 models on Vertex on 20 Oct 2026.
- **Text-to-speech is the biggest cost:** Sarvam bulbul:v3 at ₹3 per 1,000 characters.
- **No noise or echo protection:** line noise and the bot's own echo can be transcribed as the caller and cut the bot off.
- **No out-of-scope handling:** nothing tells the bot what PMC does *not* handle (electricity, police…), and there are no emergency-number rules.
- **No address checking:** the address is free text as heard; no gazetteer or place-name hints for Pune.
- **Classification happens after registration:** it can't steer the call; the category stays in our dashboard and isn't sent to the CMS.
- **No latency or cost monitoring:** no per-call logs, so speed and spend aren't measured.
- **Vobiz allows only 3 concurrent calls;** a 4th caller gets a busy tone.

---
# What I Built on Top of the Base Pipeline

**Base (main branch, 13 Aug):** a working Pipecat voice bot. It used Sarvam speech-to-text, Gemini 2.5 Flash and Sarvam text-to-speech, had two LLM tools (`register_complaint`, `end_call`), and sent complaints to the CMS and the dashboard.

**Now (test/latency branch, 17 Aug → 16 Oct):** 22 commits, ~19,000 lines across 98 files in `server/` and `scripts/`, 26 new server modules and 55 test/eval scripts. All of it was driven by live test calls.

## 1. Before → after at a glance

| Area | Main branch | Now |
|---|---|---|
| Speech-to-text | Sarvam `saaras:v3`, no hints | Sarvam `saaras:v3` + 50 Pune place-name hints, language switching, auto-reconnect |
| LLM | Gemini 2.5 Flash (AI Studio) | Gemini 3.1 Flash-Lite via Vertex AI, with fallback; Sarvam 105B also wired in |
| Text-to-speech | Sarvam `bulbul:v3` | **Murf Falcon** (~74% cheaper per call); bulbul:v3 kept as alternative |
| Address | Free text as heard | Structured area → road → landmark + 10,640-place Pune gazetteer + post-call AI reviewer |
| Noise / echo | Nothing | Transcript guard, barge-in gate, tuned voice detection |
| Scope | No rules | Out-of-scope decline + emergency numbers (101/108/112) locked in code |
| Languages | Prompt only | Detection, per-language tagging, mid-call switching |
| Monitoring | None | Per-call latency + cost log, Prometheus + Grafana, call recordings |
| Deployment | Manual | systemd service, Caddy, deploy and server-switch scripts |
| Testing | None | 55 behaviour, eval and probe scripts |

## 2. What I built

### 2.1 Conversation and intake quality
- **Address capture:** step-by-step area → road → landmark, each read back. Accepts "I don't know" instead of looping.
- **Pune gazetteer:** 10,640 localities, roads, landmarks and societies from OpenStreetMap + India Post, with Marathi/English spelling matching.
- **Post-call address reviewer** (`sarvam-105b`): reads the whole transcript and corrects the address against the gazetteer.
- **Multiple complaints in one call:** a second complaint is filed separately; duplicates are caught.
- **Names:** surname follow-up and spelled-out names. If the caller refuses, the complaint still files.
- **Mobile number:** taken from caller ID with no question asked. Changed by voice only if the caller asks. The keypad (DTMF) flow was removed.
- **Number guard / confirm guard:** numbers read back exactly digit by digit, and stray noise is no longer taken as "yes"/"no".
- **Scope rules:** a polite decline for non-PMC issues (electricity, police, bills). **Emergency filter:** the bot can never say any help number except 101/108/112.

### 2.2 Language handling
- Detects the caller's language (Marathi/Hindi/English) and keeps the bot in it.
- Switches the speech-to-text language once the caller's language is known.
- Language lock and tagging so the bot doesn't drift mid-sentence.

### 2.3 Call robustness (noise, echo, dropouts)
- **Transcript guard:** drops the bot's own echo and garbage transcripts from line noise. After repeated phantoms it says once that the line is noisy.
- **Barge-in gate:** the bot pauses the instant the caller speaks, confirms when real words arrive, and resumes if it was only noise.
- **STT watchdog:** reconnects speech-to-text if it goes deaf mid-call, and flushes short answers like "हो" that would otherwise be missed.
- **Voice-detection tuning** from real call recordings: confidence, volume, silence window and interrupt threshold.
- **LLM fallback:** if the main model fails, a second model answers so the call doesn't die.

### 2.4 Speed (latency)
- **LLM warm-up during the greeting:** turn-1 first token went from 5.6 s to 0.6 s (Sarvam).
- **Prompt-cache warm-up**, and the whole prompt kept identical across calls for cache hits.
- **Clause-level speech:** starts speaking at the first comma instead of waiting for the whole sentence.
- **Pre-recorded fixed lines:** greeting and holding line cached as audio, with no text-to-speech wait.
- **Sarvam fast streaming mode** and Smart Turn end-of-speech detection.
- **Per-stage latency log** for every call: STT, LLM and TTS first-byte, and total response delay.

### 2.5 Cost
- **Verified cost analysis:** rates from vendor pricing pages and our own Vobiz ledger. This found the ₹0.20/min stream fee the original estimate missed.
- **Text-to-speech switched to Murf Falcon:** ₹4.63 → ₹1.21 per call.
- **Gemini via Vertex AI:** uses Google Cloud credit, with prompt caching at 69–86% of input tokens.
- **Per-call cost tracking:** every call logs its INR cost split by telephony, STT, TTS and LLM.
- **Result:** ₹10.1–12.2 → **₹6.3–6.8 per call** (ex-GST).

### 2.6 Integrations
- **CMS:** submission with automatic retry if the CMS is down; the caller never waits on it.
- **Managed-platform adapters:** tool endpoints so Sarvam Voice Agents and Gnani can file into the same backend.
- **Outbound calling script** via Vobiz.

### 2.7 Operations
- **Deployment:** systemd service, Caddy reverse proxy, `deploy.sh`, and scripts to switch between servers.
- **Monitoring:** Prometheus metrics + Grafana dashboard (latency, cost, errors).
- **Call recorder** + recording inspector, so live calls can be replayed and debugged.

### 2.8 Testing
55 scripts in `scripts/`, in five groups:
- **Behaviour tests:** scope, emergency, names, second complaint, vague address, language lock, end call, etc.
- **Evaluations:** a 22-case address eval and a turn-replay harness.
- **Provider probes:** Murf, Gemini, Google Chirp, Sarvam realtime STT.
- **A/B harnesses:** noise processing (DSP), STT tuning.
- **Reports:** latency and cost.

## 3. Tried and rejected (measured, not guessed)

| Experiment | Result |
|---|---|
| Noise suppression (RNNoise) + gain boost | Cut 31–74% of real caller speech and flipped "हो" into "नाही". Kept off |
| Sarvam `saaras:v4` | Passed short tests, then failed after ~150 s of continuous streaming |
| In-call address matching | Wrong on 25% of lookups, so moved to the post-call reviewer |
| Google Chirp 3 / ElevenLabs Scribe speech-to-text | A/B tested as alternatives; Sarvam kept |
| Gemini 3.5 Flash-Lite | Can't turn thinking off, 3–4 s per reply; kept only as fallback |

## 4. Where it stands now

| Metric | Value |
|---|---|
| Cost per call (~3¼ min) | **₹6.3–6.8** ex-GST (from ₹10.1–12.2 on the Sarvam-only stack) |
| Response delay | **~5.3 s** on Murf + Gemini; was 1.8–2.5 s on the Sarvam-only stack |

**Open issue:** the cost cut came with a speed loss. Gemini's first token is ~4× slower than Sarvam's. This is the first thing the next phase fixes.

FYI: This is still in progress while making this plan and the target costs per min calls is oing to be further lower then mentioned above

---
# Proposal: A Reusable Voice-Bot Base with a Plugin System

## 1. The idea

Instead of building each voice project from scratch, we keep **one base pipeline** and configure it per project.

- The base ships the common things every voice bot needs.
- Anything project-specific is a **plugin**: included when the project needs it, left out when it doesn't.
- The conversation itself is set in a config file. That covers which questions are asked, in what order, and where AI decisions are made.

**First target: Complaint Management Systems (CMS) only.** The base is kept deliberately small and grows only as real needs come up.


![[Untitled Diagram-2026-10-16T06-55-19.png]]

## 2. The base (always included)

| Feature | What it does | Configurable |
|---|---|---|
| Opening message | Pre-recorded greeting; the bot  | Text, language, voice |
| Field collection | Asks for the fields a project required / optional / skippable (e.g. name skipped if refused) |
| Conversation flow | The steps the call goes throuAI is applied at each step |
| **Decision pipeline** | Decides if the complaint ies, reply messages, decision model |
| Voice stack | Speech-to-text, LLM, text-to-speechni, Murf, …), API-based or on-prem |
| Safeguards | Echo/noise filtering, barge-in, recok | On/off per guard |
| Monitoring | Per-call latency, cost, transcript,

## 3. The core: Decision pipeline

The one critical job of the base in a CMS is to decvalid **as soon as the complaint is heard**, before
spending time on address and other details.

![[Untitled Diagram-2026-10-16T06-58-17.png]]

| Outcome | When | Bot's reply |
|---|---|---|
| **Valid** | Complaint is in this CMS's scope (e.g. potholes, garbage, water supply for PMC) | Continues the intake and registers it |
| **Not valid: other department** | Real complaint, but someone else handles it (e.g. electricity, police) | "This complaint is handled by the respective department. Kindly contact them to lodge it." |
| **Not valid: can't process** | Not a complaint at all (status query, test call, unrelated request) | "Sorry, we can't process this request on this line." |
| **Not sure** | Speech unclear or too short | Asks once more, so a valid complaint isn't rejected because of a bad line 

The existing emergency rule stays as-is: fire, medi 112.

**How the decision is made (pluggable):**

| Option | Delay added | Best for |
|---|---|---|
| LLM decides inside the same turn (default) | None | Any new project, works from day one with just a list of valid categories |
| On-prem model on our server | < 0.1 s | Data mustundred labelled examples |
| Client's own classifier via API (e.g. PMC's 78-category model) | 2.5–22 s, so it runs in the background | Department tagging after
a complaint is accepted |

**Per project, we only set:** the list of valid comges, and which decision option to use. Every decision
is logged with the transcript, so wrong decisions ctuned.

## 4. Plugins (opt-in)

| Plugin                    | What it does                                                                             | Include when                                             |
| ------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| Location pinpointing      | Area → road → landmark, matched against a local place database, corrected after the call | The complaint needs a site visit (civic complaints)      |
| Department classification | Tags the accepted complaint with a department/category                                   | The CMS routes by department                             |
| CMS connector             | Files the complaint into the client's system with retries                                | Always for CMS projects; one connector per client system |
| *Future*                  | Outbound feedback calls, SMS confirmation, ward mapping, …                               | Built only when a project needs it                       |

A project without a site visit (e.g. a billing complaint line) simply leaves out the location plugin.

## 5. Example: what a project config looks like

```yaml
project: pmc_complaints
opening: "Namaskar, PMC helpline…"
￼fields:
  - name:      {required: false, skip_if_refused: true}
  - complaint: {required: true}
￼decision:
  method: llm                      # or: onprem_model | client_api
  valid: [roads, garbage, water_supply, drainage, street_lights, …]
  reply_other_department: "This is handled by the respective department…"
  reply_cannot_process: "Sorry, we can't process this request…"
plugins: [location, department_classification, pmc_cms]
```

## 6. Why this helps

- **Faster calls for invalid complaints:** they end after the full address flow. Cost per call drops
from ₹6.3–6.8 to about ₹2.3.
- **Faster, cheaper replies:** each step carries on, not one large prompt.
- **New CMS projects** (another city, another depar code.
- **No unused features shipped:** plugins come in oem.

## 7. Scope

- **Now:** base pipeline + decision pipeline + the ation, classification, CMS connector).
- **Later, only when needed:** outbound calls, othenagement, a UI for building flows.
 
## Plugins as Agents

Each plugin is a small, self-contained **agent** with its own instructions, model and tools. The main voice agent (the one talking to the caller) calls a plugin agent only when it is needed, the same way it calls a tool. A project includes only the agents it needs.

![[Untitled Diagram-2026-10-16T07-11-53.png]]

### When each agent runs

On a phone call, every extra agent call adds silence, so each agent declares how it runs:

| Mode | How it works | Caller waits? | Example |
|---|---|---|---|
| **Inline** | Decided inside the main agent's own turn | No | Decision pipeline (valid / not valid) |
| **Blocking** | Main agent waits for the result; a short filler line ("one moment, checking…") covers the gap | Yes, ~1–2 s | Confirming a location when the caller is unsure |
| **Background** | Starts while the conversation continues; result is ready by the time it is needed | No | Department classification while the address is being asked |
| **After call** | Runs once the call has ended | No | Address correction, CMS filing retries, call summary |

### Who triggers an agent

- **The flow (fixed):** must-run agents fire at a set point, e.g. the decision agent always runs after the complaint is heard. Predictable and testable.
- **The main agent (on demand):** optional agents are called only when the conversation needs them, e.g. the location agent when the caller gives a vague address.

### What every plugin agent defines

| Field | Example (Location agent) |
|---|---|
| Name and when to use it | "Use when the caller's address is vague or unrecognised" |
| Input | Caller's words about the place |
| Output | Matched area, road, landmark + confidence |
| Mode | Background or after-call |
| Model | Any: small/fast LLM, on-prem model, or no LLM at all |
| Time limit + fallback | 2 s; on timeout keep the caller's own words |

### Cost and speed

- An agent call with a small prompt (1–3k tokens) costs about **₹0.02–0.10**. The cost is negligible; the real constraint is speed, which is why the mode matters.
- Agents with no LLM (a database lookup, an API call) cost nothing extra and add almost no delay.

### Reuse across projects

Agents can run inside the bot or as separate services over HTTP. A separately hosted agent (e.g. location pinpointing for Pune) can be shared by several projects and updated without touching the bots that use it.

My recommendation is to keep the decision pipeline inline in the main agent's turn, not a separate agent. It runs on every call, so a separate agent would add a delay to every caller. The other plugins work well as agents because most of them can run in the background or after the call.


