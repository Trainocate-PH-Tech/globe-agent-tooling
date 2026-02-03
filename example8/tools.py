from pathlib import Path

from strands import tool


def _read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


@tool
def call_fraud_api(msisdn: str) -> dict:
    """Mock API call returning {ok, data, error}."""
    data_path = Path(__file__).parent / "data" / "mock_api.txt"
    if not data_path.exists():
        return {"ok": False, "data": {}, "error": "mock_api.txt missing"}

    for line in _read_lines(data_path):
        if line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 3:
            continue
        row_msisdn, status, risk_band = parts
        if row_msisdn == msisdn:
            if status != "ok":
                return {"ok": False, "data": {}, "error": risk_band}
            return {"ok": True, "data": {"risk_band": risk_band}, "error": ""}

    return {"ok": False, "data": {}, "error": "not found"}


@tool
def update_case_record(msisdn: str, status: str) -> str:
    """Append a case status update to a local record file."""
    record_path = Path(__file__).parent / "data" / "case_records.txt"
    record_path.write_text(
        record_path.read_text() + f"{msisdn}|{status}\n"
        if record_path.exists()
        else f"{msisdn}|{status}\n"
    )
    return f"Case updated: {status}"


@tool
def escalate_to_human(reason: str) -> str:
    """Escalate to a human reviewer with a reason."""
    return f"Escalated to human support: {reason}"
