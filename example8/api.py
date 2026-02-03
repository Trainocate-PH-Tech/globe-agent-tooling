from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)

DATA_PATH = Path(__file__).parent / "data" / "mock_api.txt"


def load_mock_data() -> dict:
    data = {}
    if not DATA_PATH.exists():
        return data
    for line in DATA_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 3:
            continue
        msisdn, status, risk_band = parts
        data[msisdn] = {"status": status, "risk_band": risk_band}
    return data


@app.get("/health")
def health():
    return jsonify({"ok": True})


@app.get("/fraud-check")
def fraud_check():
    msisdn = request.args.get("msisdn", "")
    if not msisdn:
        return jsonify({"ok": False, "data": {}, "error": "msisdn required"}), 400

    data = load_mock_data()
    record = data.get(msisdn)
    if record is None:
        return jsonify({"ok": False, "data": {}, "error": "not found"}), 404

    if record["status"] != "ok":
        return jsonify({"ok": False, "data": {}, "error": record["risk_band"]}), 502

    return jsonify({"ok": True, "data": {"risk_band": record["risk_band"]}, "error": ""})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=False)
