
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "phishing_model.joblib"

model = joblib.load(MODEL_PATH)

# Diagnostic examples, not a verified security test set.
test_urls = [
    "chatgpt.com",
    "www.chatgpt.com",
    "google.com",
    "www.google.com",
    "paypal.com",
    "www.paypal.com",
    "openai.com",
    "example.com",
    "paypal.com.example.org/login",
    "google.com.example.org/login",
]

print("\nPHISHGUARD BASELINE EVALUATION")
print("=" * 65)

for url in test_urls:
    prediction = int(model.predict([url])[0])
    score = float(model.decision_function([url])[0])

    label = "PHISHING" if prediction == 1 else "LEGITIMATE"

    print(f"{url:35} {label:12} Score: {score:.3f}")

print("\nReminder:")
print("- These examples are diagnostic, not proof of safety.")
print("- A negative score means the model predicts legitimate.")
print("- A positive score means the model predicts phishing.")
print("- The score is not a probability.")
