
from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import urlparse
from pathlib import Path
import hashlib
import hmac
import ipaddress
import joblib

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "phishing_model.joblib"
HASH_PATH = BASE_DIR / "model" / "trusted_model_hash.txt"


def calculate_sha256(file_path):
    """Calculate a file's SHA-256 hash."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def verify_model_integrity():
    """Compare the model hash with the saved reference."""
    if not MODEL_PATH.is_file():
        return False, "Model file not found."

    if not HASH_PATH.is_file():
        return False, "Trusted hash reference not found."

    try:
        trusted_hash = HASH_PATH.read_text(
            encoding="utf-8"
        ).strip()

        if len(trusted_hash) != 64:
            return False, "Trusted hash reference is invalid."

        # Ensure the reference contains hexadecimal characters.
        try:
            int(trusted_hash, 16)
        except ValueError:
            return False, "Trusted hash reference is invalid."

        current_hash = calculate_sha256(MODEL_PATH)

        if hmac.compare_digest(current_hash, trusted_hash.lower()):
            return True, "Model integrity verified."

        return False, "Model hash differs from the trusted reference."

    except OSError:
        return False, "Unable to read the model or hash reference."


# Refuse to load the model if integrity verification fails.
if not MODEL_PATH.is_file():
    raise FileNotFoundError(
        f"Trained model not found: {MODEL_PATH}. "
        "Run train_model.py first."
    )

integrity_ok, integrity_message = verify_model_integrity()

if not integrity_ok:
    raise RuntimeError(
        f"Model integrity verification failed: {integrity_message} "
        "Check the model and restore a trusted reference before starting."
    )

# Load the model only after its integrity check succeeds.
model = joblib.load(MODEL_PATH)


def analyse_url(url):
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()
    indicators = []

    try:
        ipaddress.ip_address(hostname)
        indicators.append(
            "The hostname is an IP address rather than a domain name."
        )
    except ValueError:
        pass

    if "@" in url:
        indicators.append(
            "The URL contains an @ symbol that may be misleading."
        )

    if len(url) > 100:
        indicators.append("The URL is unusually long.")

    if len(hostname.split(".")) > 4:
        indicators.append(
            "The hostname contains many domain components."
        )

    if "xn--" in hostname:
        indicators.append(
            "The hostname contains an internationalized domain encoding."
        )

    if parsed.scheme == "http":
        indicators.append(
            "The URL uses HTTP rather than encrypted HTTPS."
        )

    return indicators


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to PhishGuard API",
        "status": "Backend is running",
        "model_loaded": True
    })


@app.route("/api/integrity", methods=["GET"])
def model_integrity():
    # Recheck the file against the saved reference.
    verified, message = verify_model_integrity()

    if not verified:
        return jsonify({
            "integrity": "failed",
            "message": message
        }), 503

    return jsonify({
        "integrity": "verified",
        "message": message,
        "algorithm": "SHA-256"
    })


@app.route("/api/scan", methods=["POST"])
def scan_url():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "")

    if not isinstance(url, str):
        return jsonify({"error": "URL must be text."}), 400

    url = url.strip()

    if not url:
        return jsonify({"error": "Please enter a website URL."}), 400

    if any(char.isspace() for char in url):
        return jsonify({"error": "Please enter a valid URL."}), 400

    if "://" not in url:
        url = "https://" + url

    parsed = urlparse(url)

    try:
        parsed.port
    except ValueError:
        return jsonify({"error": "The URL contains an invalid port."}), 400

    hostname = parsed.hostname

    if (
        parsed.scheme not in ("http", "https")
        or not hostname
        or "." not in hostname
        or hostname.startswith(".")
        or hostname.endswith(".")
        or len(hostname) > 253
    ):
        return jsonify({"error": "Please enter a valid website URL."}), 400

    indicators = analyse_url(url)
    model_input = url.split("://", 1)[1]

    prediction = int(model.predict([model_input])[0])

    if prediction == 1:
        verdict = "phishing"
        message = (
            "The machine-learning model predicts that this URL "
            "resembles phishing examples in its training data."
        )
    else:
        verdict = "legitimate"
        message = (
            "The machine-learning model predicts that this URL "
            "resembles legitimate examples in its training data. "
            "This does not guarantee that the website is safe."
        )

    return jsonify({
        "url": url,
        "domain": hostname,
        "prediction": verdict,
        "status": verdict,
        "message": message,
        "indicators": indicators,
        "detection_method": "LinearSVC with character-level TF-IDF",
        "model_used": True
    })


if __name__ == "__main__":
    app.run(debug=True)
