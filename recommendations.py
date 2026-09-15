"""
recommendations.py

Turns the scorer's triggered rules into prioritized, actionable
recommendations - the "Act" step in Discover -> Understand -> Act -> Measure.
Each rule maps to a specific fix, not a generic "be safer online" tip.
"""

from exposure_score import score_profile

# Maps each rule name to a concrete recommendation.
RECOMMENDATIONS = {
    "reused_username": {
        "action": "Use a different username on at least one of your accounts, especially ones tied to school or hobbies you don't want linked to your main identity.",
        "effort": "low",
    },
    "public_school": {
        "action": "Check your social media privacy settings and remove or hide your school name from public profile fields.",
        "effort": "low",
    },
    "public_location": {
        "action": "Turn off location tagging on posts and remove your city from public bios where it isn't necessary.",
        "effort": "low",
    },
    "many_connections": {
        "action": "Since several pieces of your information link together, prioritize breaking the strongest link first - usually the reused username.",
        "effort": "medium",
    },
}


def generate_recommendations(profile: dict) -> list[dict]:
    result = score_profile(profile)
    # sort triggered rules by point value, highest impact first
    ranked = sorted(result["triggered_rules"], key=lambda r: r["points"], reverse=True)

    recommendations = []
    for rule in ranked:
        rec = RECOMMENDATIONS.get(rule["rule"])
        if rec:
            recommendations.append({
                "priority": len(recommendations) + 1,
                "because": rule["reason"],
                "recommendation": rec["action"],
                "effort": rec["effort"],
                "points_if_fixed": rule["points"],
            })
    return recommendations


if __name__ == "__main__":
    test_profile = {
        "username_reused_count": 2,
        "school_public": True,
        "location_public": True,
        "connection_count": 3,
    }

    recs = generate_recommendations(test_profile)
    print(f"{len(recs)} prioritized recommendation(s):\n")
    for r in recs:
        print(f"#{r['priority']} (fixing this reduces score by {r['points_if_fixed']}, effort: {r['effort']})")
        print(f"   Because: {r['because']}")
        print(f"   Do this: {r['recommendation']}\n")
