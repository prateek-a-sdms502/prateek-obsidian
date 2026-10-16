Hi Team,

I've attached a document covering the AI voice pipeline end to end. A quick summary:

**1. Where we started**
The main branch has a working voice bot for the PMC complaint helpline: Sarvam speech-to-text, Gemini 2.5 Flash, and Sarvam text-to-speech. It takes a complaint over the phone and files it into the CMS.

**2. What I've built on top of it**
Over the last two months, all of it tested on live calls:
- **Call quality:** structured address capture backed by a Pune place database (10,640 places), handling of multiple complaints per call, and accurate number read-back.
- **Robustness:** filtering of echo and line noise, recovery when speech-to-text drops, and better handling of interruptions.
- **Languages:** reliable Marathi / Hindi / English switching.
- **Cost:** per-call cost reduced from **₹10–12 to ₹6.3–6.8** (ex-GST estimaed each call will go for 4mins).
- **Operations:** deployment scripts, monitoring dashboards, per-call cost and latency tracking, and 55 test scripts.

**3. What I'm proposing next**
A **reusable voice-bot base for complaint management systems**, so future CMS projects start from configuration instead of fresh code:
- **Configurable base:** opening message, fields to collect, and the conversation steps are all set per project.
- **Decision pipeline (the core):** right after the caller describes the complaint, the bot decides whether it's valid. Valid complaints are registered; invalid ones get a polite reply asking the caller to contact the respective department. Invalid calls then end in about a minute (~₹2.3 instead of ~₹6.5).
- **Plugins as agents:** optional features such as location pinpointing, department classification and the CMS connector are included only when a project needs them.

**4. Open issue**
The cheaper provider setup has made the bot slower to respond: ~5.3 s against ~2 s earlier. Fixing that is the first step of the next phase (1–2 days) and doesn't depend on the larger build.

**5. What I need from you**
- Go-ahead for the latency fix (Phase A).
- Feedback on the reusable-base proposal before I start building it (~3 weeks).
- Whether PMC is okay with the bot naming the right department for invalid complaints (today it declines without any guidance).

Happy to walk through it on a call.

Regards,
Prateek Awate