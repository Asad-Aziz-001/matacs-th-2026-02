# Write-up: AI Proposal Triage Design (MATACS-TH-2026-02)

Proposals are referred to by letter (A–E) only.

## 1. AI vs. rules

**AI is used for two things only:**
- **Extraction:** reading messy proposal text and copying facts into a fixed JSON format, each with an exact evidence quote.
- **Explanation (optional):** turning an already-computed score breakdown into 2–3 plain sentences.

**Plain code and rules do everything else:** PDF-to-text, injection scan, schema validation, mandatory pass/fail checks, budget and 16-week limits, weighted scoring, ranking and the audit log.

**Why this line:** proposals are free text in many styles, which AI reads well. Pass/fail decisions, arithmetic and ranking must be exact and repeatable, so code does them. The AI never gives a score or a rank.

**Sample set:** B is ineligible because the licence must be held by the bidder, and B leaves electrical work to a subcontractor named only after award. C and D are flagged (see Q5). A and E are ranked, A first.

## 2. Consistency and explainability

- Extraction runs at temperature 0 with a versioned prompt and a strict JSON schema.
- Scoring uses fixed formulas in code. Same facts in means same scores out.
- Extracted facts are saved. Re-ranking reads the saved facts and makes no new AI call, so ranking twice gives an identical result. If extraction is re-run, differences from the saved facts are flagged.
- Code checks that every evidence quote really appears in the proposal text. If not, the field becomes null and is flagged.

**Same proposals ranked twice?** Yes, the same result, because scoring is deterministic and facts are stored.

**How a reviewer sees why:** each proposal has a breakdown table showing, per criterion, the extracted fact, the evidence quote, the sub-score (0–100), the weight and the points added. For example, A scores 96.8 and E scores 90.2. A leads on experience (14 vs 8 qualifying installs) and timeline (12 vs 13 weeks), while E has the longer workmanship warranty.

## 3. Human in the loop

A person is involved at four points:
1. **Upload:** the reviewer selects the category and sees any extraction warnings.
2. **Flagged and ineligible queue:** the reviewer can confirm an exclusion, ask the bidder for clarification, or reinstate a proposal (for example D, once a timeline is provided).
3. **Ranked list:** the reviewer can confirm or override any position. A written reason is required for every override.
4. **Final award:** always a human decision. The tool only recommends.

**Logged for audit:** who did what and when; file hash of each upload; criteria version; prompt version; model name and settings; extracted JSON with evidence; scores; flags; every override with its reason; the final decision.

## 4. Changing criteria

- Criteria are stored in the database and versioned. An edit creates a new version and never alters the old one.
- Every scoring run records the criteria version it used. Old results stay as they were, labelled with their version.
- After an edit, the screen shows that criteria changed since scoring and offers a re-score. Facts are already stored, so re-scoring is code only, with no new AI cost.
- If the new criteria need a fact that was never extracted, only that field is extracted again.
- The reviewer can compare old and new rankings side by side.
- Weights must total 100%, checked on save. A changed mandatory rule can change eligibility, so affected proposals are flagged for review.
- Nothing is silently re-ranked once an award decision is recorded. Admin edits are logged too.

## 5. Risks and safeguards

| Risk | Safeguard |
|---|---|
| **Wrong extraction** (wrong number, misread table) | Evidence quote required for every fact and checked against the source text. Schema validation. Missing or unclear values become null and are flagged, never guessed. Reviewer sees quotes beside scores. |
| **Made-up facts** | Prompt says extract only what is stated. Unquotable values are rejected. The AI does not do the maths. |
| **Vague or deferred promises** (B's subcontractor, D's open schedule) | Conditional wording is treated as unclear, not confirmed. B fails the mandatory licence check. D is flagged because the 16-week limit cannot be confirmed. |
| **Manipulation** (C contains hidden text telling automated reviewers to rank it first) | Proposal text is treated as data, not instructions. A code-level scan flags such phrases and the extractor reports them. The instruction is ignored, C is not ranked, and a human reviews it. The AI cannot change scores anyway, because code scores. |
| **Bias** (favouring polished writing or large firms) | AI extracts facts only and does not judge writing quality. Scoring uses numbers and fixed rubrics. Bidder name is not a scoring input. Reviewer can override with a logged reason. |
| **Cost** | One small AI call per proposal. No AI in scoring or re-ranking. Results cached by file hash. File size and page limits. |
| **Bad PDFs or scans** | OCR fallback. If text is unreadable, the file is flagged instead of scored. |

## Assumptions

- Qualifying installs means commercial installs of 100 kW or more in the last 5 years, as stated in the proposal.
- Price and timeline are scored relative to the best valid bid among proposals that pass mandatory checks.
- A proposal with no stated completion time is flagged instead of scored as zero, because a human may resolve it.
- Experience bands, warranty caps and team points are my own simple choices that an admin could change.