"""
exposure_score.py

Rule-based (not black-box AI) scoring for a profile's exposure.
Every point added is tied to an explicit, explainable rule, per
the project's "transparent results" ethics principle.
"""

RULES = [
    {
        "name": "reused_username",
        "check": lambda p: p.get("username_reused_count", 0) >= 2,
        "points": 15,
        "reason": "Same username reused across multiple accounts makes them easy to link together.",
    },
    {
        "name": "public_school",
        "check": lambda p: p.get("school_public", False),
        "points": 10,
        "reason": "A public school listing narrows down location and age significantly.",
    },
    {
        "name": "public_location",
        "check": lambda p: p.get("location_public", False),
        "points": 10,
        "reason": "Publicly visible location adds another identifying data point.",
    },
    {
        "name": "many_connections",
        "check": lambda p: p.get("connection_count", 0) >= 3,
        "points": 20,
        "reason": "Multiple pieces of information connect to each other, compounding identifiability.",
    },
]


def score_profile(profile: dict) -> dict:
    total = 0
    triggered = []
    for rule in RULES:
        if rule["check"](profile):
            total += rule["points"]
            triggered.append({"rule": rule["name"], "reason": rule["reason"], "points": rule["points"]})
    return {"score": total, "max_score": sum(r["points"] for r in RULES), "triggered_rules": triggered}


if __name__ == "__main__":
    # synthetic test profile, built from the connection_graph.py example
    test_profile = {
        "username_reused_count": 2,
        "school_public": True,
        "location_public": True,
        "connection_count": 3,
    }

    result = score_profile(test_profile)
    print(f"Exposure score: {result['score']} / {result['max_score']}\n")
    print("Why this score:")
    for r in result["triggered_rules"]:
        print(f"  - (+{r['points']}) {r['reason']}")
