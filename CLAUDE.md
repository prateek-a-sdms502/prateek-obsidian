# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal Obsidian vault of work notes, versioned with git. It has no code, build, lint, or tests. Most notes cover the PMC (Pune Municipal Corporation) complaint-helpline work: the voice bot "Asha" (Pipecat, Vobiz telephony, Sarvam STT, Gemini LLM, Sarvam/Murf TTS) and the CMS v2 complaint classifier (XLM-R, 78 departments).

## Layout

- `Daily Log/`: older daily notes (13–15 Oct 2026). Newer daily notes (`16th Oct 2026.md`, `19th Oct 2026.md`) sit at the vault root.
- Root-level topic notes: `CMS_v2_AI_Project_Briefing.md` (classifier briefing) and `Universal Voice AI Pipeline.md` (current voice pipeline plus the proposed reusable "plug-and-play" CMS voice pipeline). `Untitled.md` and `Untitled 1.md` are drafts (proposal email / team summary).
- `images/`: exported diagrams. Some mermaid PNGs are still at the root.
- `.obsidian/`: app config (untracked). Core plugins include daily notes, templates, canvas, bases, and sync.

## Conventions

- **Daily note filename:** `<ordinal day> <Mon> <YYYY>.md`, e.g. `19th Oct 2026.md`. (`13 Oct 2026.md` has no ordinal and is the exception.)
- **Daily note structure:** a standup with `## What I did` (or `## What I did yesterday`), `## What I plan to do` (or `## What I have planned for today`), and `## Blockers`. A longer report can follow after a `---` divider, e.g. the "PMC Calling Bot: Daily Report" in `16th Oct 2026.md`.
- **Embeds:** use Obsidian wikilinks, e.g. `![[Untitled Diagram-2026-10-16T06-52-45 1.png]]`. These resolve by filename anywhere in the vault, so moving images into `images/` doesn't break them. Renaming an image does, so update every embed when you rename one.
- **Content style:** short plain-English summary first, then tables for facts and figures: call IDs, ₹ cost breakdowns, latency, accuracy. Keep measured numbers exact and dated; don't round or restate them.
- **Commits:** short lowercase messages describing the notes changed (e.g. "plan for 19th", "updated 16th Oct 2026 V2").
