from pathlib import Path

from strands import tool


def _read_kv_lines(path: Path) -> list[list[str]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        rows.append([p.strip() for p in line.split("|")])
    return rows


@tool
def get_account_profile(msisdn: str) -> dict:
    """Return account profile signals for a given MSISDN."""
    data_path = Path(__file__).parent / "data" / "account_profiles.txt"
    for parts in _read_kv_lines(data_path):
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
    for parts in _read_kv_lines(data_path):
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
def escalate_to_human(reason: str) -> str:
    """Escalate to a human reviewer with a reason."""
    return f"Escalated to human support: {reason}"
