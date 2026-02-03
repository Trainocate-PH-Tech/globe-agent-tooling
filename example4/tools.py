from strands import tool

INVOICES = {
    "ACC-100": "Duplicate charge flagged.",
    "ACC-200": "Payment pending review.",
}

SYSTEM_STATUS = {
    "login": "All systems operational.",
    "payments": "Minor delays reported.",
}


@tool
def classify_issue(text: str) -> str:
    """Classify a request as billing, technical, or unknown."""
    lowered = text.lower()
    if "charge" in lowered or "invoice" in lowered or "billing" in lowered:
        return "billing"
    if "error" in lowered or "login" in lowered or "down" in lowered:
        return "technical"
    return "unknown"


@tool
def lookup_invoice(account_id: str) -> str:
    """Lookup invoice status by account ID."""
    return INVOICES.get(account_id, "Invoice not found.")


@tool
def check_system_status(service: str) -> str:
    """Check system status for a service name."""
    return SYSTEM_STATUS.get(service, "Service not found.")


@tool
def escalate_to_human(reason: str) -> str:
    """Escalate to a human agent with a reason."""
    return f"Escalated to human support: {reason}"
