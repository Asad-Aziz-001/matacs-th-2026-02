"""Deterministic scoring: same facts in -> same ranking out.
AI only extracts facts (see PROMPTS.md); this script does the maths."""
import json
from pathlib import Path

data = json.loads((Path(__file__).parent / "facts_A_E.json").read_text())
crit = data["criteria"]
W = crit["weights"]
props = data["proposals"]


def experience_score(n):
    for floor, pts in [(12, 100), (8, 80), (5, 60), (3, 40), (1, 20)]:
        if n >= floor:
            return pts
    return 0


def warranty_score(panel, work):
    return (min(panel / 25, 1) * 100 + min(work / 15, 1) * 100) / 2


def team_score(team):
    return 25 * sum(team.values())


# Step 1: mandatory + hard rules
status, notes = {}, {}
for k, p in props.items():
    if not (p["licence"] and p["wsib_insurance"]):
        status[k], notes[k] = "ineligible", "failed mandatory criteria"
    elif p["price"] > crit["budget_ceiling"]:
        status[k], notes[k] = "ineligible", "over budget"
    elif p["weeks"] is not None and p["weeks"] > crit["max_weeks"]:
        status[k], notes[k] = "ineligible", "over 16 weeks"
    elif p["flags"]:
        status[k], notes[k] = "flagged", ", ".join(p["flags"])
    elif p["weeks"] is None:
        status[k], notes[k] = "flagged", "missing timeline"
    else:
        status[k], notes[k] = "ranked", ""

# Step 2: normalisation pool = proposals that passed mandatory with values stated
pool = [p for k, p in props.items() if status[k] != "ineligible"]
min_price = min(p["price"] for p in pool)
min_weeks = min(p["weeks"] for p in pool if p["weeks"] is not None)

# Step 3: weighted scores
scores = {}
for k, p in props.items():
    parts = {
        "experience": experience_score(p["installs_100kw_5y"]),
        "price": 100 * min_price / p["price"],
        "timeline": 100 * min_weeks / p["weeks"] if p["weeks"] else 0,
        "warranty": warranty_score(p["panel_years"], p["workmanship_years"]),
        "team": team_score(p["team"]),
    }
    scores[k] = round(sum(parts[c] * W[c] / 100 for c in W), 1)

# Step 4: rank only the "ranked" ones
ranked = sorted([k for k in props if status[k] == "ranked"], key=lambda k: -scores[k])

print("RANKED:")
for i, k in enumerate(ranked, 1):
    print(f"  {i}. {k}  score={scores[k]}")
print("NOT RANKED:")
for k in props:
    if status[k] != "ranked":
        print(f"  {k}  {status[k]}  ({notes[k]})  shadow_score={scores[k]}")