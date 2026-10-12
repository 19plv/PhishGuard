
from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import urlparse
from pathlib import Path
import ipaddress
import joblib

app = Flask(__name__)
CORS(app)

# Load the trained model once when Flask starts
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "phishing_model.joblib"

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Trained model not found: {MODEL_PATH}. "
        "Run train_model.py first."
    )

model = joblib.load(MODEL_PATH)


def analyse_url(url):
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()
    indicators = []

    # Check whether the hostname is an IP address
    try:
        ipaddress.ip_address(hostname)
        indicators.append(
            "The hostname is an IP address rather than a domain name."
        )
    except ValueError:
        pass

    # Check for a potentially misleading @ symbol
    if "@" in url:
        indicators.append(
            "The URL contains an @ symbol that may be misleading."
        )

    # Check URL length
    if len(url) > 100:
        indicators.append("The URL is unusually long.")

    # Check number of domain components
    if len(hostname.split(".")) > 4:
        indicators.append(
            "The hostname contains many domain components."
        )

    # Check for punycode
    if "xn--" in hostname:
        indicators.append(
            "The hostname contains an internationalized domain encoding."
        )

    # Check whether HTTPS is used
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

    # Add a scheme if the user omitted it
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

    # Run the basic URL checks
    indicators = analyse_url(url)

    # The model was trained on URL strings, often without a scheme.
    # Remove only the leading scheme to better match its training format.
    model_input = url.split("://", 1)[1]

    # Model labels: 0 = good (legitimate), 1 = bad (phishing)
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
