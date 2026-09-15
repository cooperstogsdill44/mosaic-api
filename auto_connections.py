"""
auto_connections.py

Instead of manually listing which fields connect to which (as the
earlier demo did), this derives connections automatically from raw
profile data. This is the real version of the "connection mapping"
algorithm - the part that has to generalize to any user's input,
not just one hardcoded example.

Two detection strategies are used:
1. Exact match - the same value appears in two different fields
   (e.g. username and email_prefix are identical).
2. Substring match - one value contains another (e.g. an Instagram
   handle contains the username).
"""

from itertools import combinations


def normalize(value: str) -> str:
    """Lowercase and strip so 'Jstarlight' and 'jstarlight' still match."""
    return value.strip().lower()


def detect_connections(profile: dict) -> list[dict]:
    """
    profile: a dict like {"username": "...", "instagram": "...", ...}
    Returns a list of detected connections between fields, each with
    a plain-English reason - this is what gets fed into both the
    Digital Identity Map (frontend) and the exposure scorer.
    """
    connections = []

    # compare every pair of fields exactly once
    for (field_a, value_a), (field_b, value_b) in combinations(profile.items(), 2):
        if not value_a or not value_b:
            continue

        norm_a, norm_b = normalize(value_a), normalize(value_b)

        if norm_a == norm_b:
            connections.append({
                "field_a": field_a,
                "field_b": field_b,
                "type": "exact_match",
                "reason": f"'{field_a}' and '{field_b}' use the exact same value.",
            })
        elif norm_a in norm_b or norm_b in norm_a:
            connections.append({
                "field_a": field_a,
                "field_b": field_b,
                "type": "partial_match",
                "reason": f"'{field_a}' appears to be reused inside '{field_b}'.",
            })

    return connections


def connection_counts(profile: dict, connections: list[dict]) -> dict:
    """How many connections each individual field participates in."""
    counts = {field: 0 for field in profile}
    for c in connections:
        counts[c["field_a"]] += 1
        counts[c["field_b"]] += 1
    return counts


if __name__ == "__main__":
    # A synthetic (fictional) test profile - no real personal data
    profile = {
        "username": "starlight_j22",
        "instagram": "starlight_j22_official",
        "email_prefix": "starlight_j22",
        "school": "Lincoln High School",
        "city": "Springfield",
    }

    connections = detect_connections(profile)

    print("Raw profile fields:")
    for field, value in profile.items():
        print(f"  {field}: {value}")

    print(f"\nAutomatically detected {len(connections)} connection(s):")
    for c in connections:
        print(f"  - {c['field_a']} <-> {c['field_b']}  [{c['type']}]")
        print(f"      {c['reason']}")

    print("\nConnection counts per field:")
    for field, count in connection_counts(profile, connections).items():
        print(f"  {field}: {count}")
