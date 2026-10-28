# MATACS-TH-2026-02: AI Proposal Triage Design

- **Full name:** Asad Aziz
- **Reference:** MATACS-TH-2026-02
- **Time actually spent:** [WRITE YOUR REAL TIME HERE, e.g. "about 3 hours over 1 day"]

## Files

- [WRITEUP.md](WRITEUP.md): answers to the five questions
- [diagram/flow.png](diagram/flow.png): process flow from upload to ranked output (AI, rule and human steps)
- [PROMPTS.md](PROMPTS.md): extraction prompt and optional reason prompt
- [ranking.json](ranking.json): expected ranking of proposals A–E
- [prototype/](prototype/): optional script that applies the scoring rules (see [prototype/README.md](prototype/README.md))

## Summary of the design

AI only extracts facts (with evidence quotes) and optionally writes the explanation. Mandatory checks, scoring and ranking are plain code, so the same facts always give the same ranking. Suspicious or incomplete proposals are flagged for a human, and a person makes the final decision.

Result on the sample set: A ranked 1st, E ranked 2nd, B ineligible, C and D flagged for human review.

## How I used AI tools

## How I used AI tools

I used Claude to help plan the design, draft the write-up, the prompts and the scoring script, and to generate the diagram. I ran the scoring script myself and checked that its output (A 96.8, E 90.2) matched ranking.json.

One place where I corrected the AI: it first suggested an .env.example file with an API key line. I questioned this because my prototype makes no API calls, so the file was removed.