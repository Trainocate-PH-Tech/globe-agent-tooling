from pathlib import Path
from strands import tool


def _read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


@tool
def get_account_profile(msisdn: str) -> dict:
    """Return account profile signals for a given MSISDN."""
    data_path = Path(__file__).parent / "data" / "account_profiles.txt"
    for line in _read_lines(data_path):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 4:
            continue
        row_msisdn, region, tenure_months, kyc_level = parts
        if row_msisdn == msisdn:
            return {
                "region": region,
                "tenure_months": int(tenure_months),
                "kyc_level": kyc_level,
            }
    return {}


@tool
def get_recent_events(msisdn: str) -> dict:
    """Return recent security events for a given MSISDN."""
    data_path = Path(__file__).parent / "data" / "recent_events.txt"
    for line in _read_lines(data_path):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 4:
            continue
        row_msisdn, last_sim_swap_days, device_change_days, failed_logins_24h = parts
        if row_msisdn == msisdn:
            return {
                "last_sim_swap_days": int(last_sim_swap_days),
                "device_change_days": int(device_change_days),
                "failed_logins_24h": int(failed_logins_24h),
            }
    return {}


@tool
def score_risk(profile: dict, events: dict) -> dict:
    """Return a simple risk score and band based on signals."""
    score = 0
    if not profile:
        return {"score": 0, "band": "unknown"}
    if profile.get("tenure_months", 0) < 3:
        score += 25
    if profile.get("kyc_level") == "basic":
        score += 20
    if events.get("last_sim_swap_days", 999) < 7:
        score += 30
    if events.get("device_change_days", 999) < 7:
        score += 10
    if events.get("failed_logins_24h", 0) >= 3:
        score += 10
    band = "low"
    if score >= 70:
        band = "high"
    elif score >= 40:
        band = "medium"
    return {"score": score, "band": band}


@tool
def build_review_summary(msisdn: str, profile: dict, events: dict, risk: dict) -> dict:
    """Build a simple review packet for a human reviewer."""
    return {
        "msisdn": msisdn,
        "profile": profile,
        "events": events,
        "risk": risk,
        "recommendation": "review",
    }


@tool
def create_review_ticket(payload: dict) -> str:
    """Create a review ticket and return its ID."""
    return "R-1001"


@tool
def route_to_queue(queue_name: str, ticket_id: str) -> str:
    """Route a ticket to a named queue."""
    return f"queued:{queue_name}:{ticket_id}"
