from pathlib import Path

from strands import tool


def _read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


@tool
def get_account_profile(msisdn: str) -> dict:
    """Return {ok, data, error} for account profile lookup."""
    data_path = Path(__file__).parent / "data" / "account_profiles.txt"
    if not data_path.exists():
        return {"ok": False, "data": {}, "error": "account_profiles.txt missing"}

    for line in _read_lines(data_path):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 4:
            continue
        row_msisdn, region, tenure_months, kyc_level = parts
        if row_msisdn == msisdn:
            return {
                "ok": True,
                "data": {
                    "region": region,
                    "tenure_months": int(tenure_months),
                    "kyc_level": kyc_level,
                },
                "error": "",
            }
    return {"ok": False, "data": {}, "error": "profile not found"}


@tool
def get_recent_events(msisdn: str) -> dict:
    """Return {ok, data, error} for recent events lookup."""
    data_path = Path(__file__).parent / "data" / "recent_events.txt"
    if not data_path.exists():
        return {"ok": False, "data": {}, "error": "recent_events.txt missing"}

    for line in _read_lines(data_path):
        if line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 4:
            continue
        row_msisdn, last_sim_swap_days, device_change_days, failed_logins_24h = parts
        if row_msisdn == msisdn:
            try:
                return {
                    "ok": True,
                    "data": {
                        "last_sim_swap_days": int(last_sim_swap_days),
                        "device_change_days": int(device_change_days),
                        "failed_logins_24h": int(failed_logins_24h),
                    },
                    "error": "",
                }
            except ValueError:
                return {
                    "ok": False,
                    "data": {},
                    "error": "recent events parse error",
                }
    return {"ok": False, "data": {}, "error": "events not found"}


@tool
def score_risk(profile: dict, events: dict) -> dict:
    """Return a risk score and band based on signals."""
    score = 0
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
