
from pathlib import Path
import pandas as pd
import joblib

BASE_DIR = Path(__file__).resolve().parent

df = pd.read_csv(
    BASE_DIR / "data" / "phishing_site_urls.csv"
)

model = joblib.load(
    BASE_DIR / "model" / "phishing_model.joblib"
)

# Inspect examples containing familiar domain names
for domain in ["google.com", "paypal.com", "openai.com", "chatgpt.com"]:
    matches = df[
        df["URL"].astype(str).str.contains(
            domain, case=False, regex=False, na=False
        )
    ]

    print(f"\n--- {domain} ---")
    print("Matching rows:", len(matches))

    if not matches.empty:
        print("Label counts:")
        print(matches["Label"].value_counts().to_string())
        print("\nExamples:")
        print(matches.head(5).to_string(index=False))

# Compare model predictions and decision scores
test_urls = [
    "google.com",
    "www.google.com",
    "paypal.com",
    "www.paypal.com",
    "openai.com",
    "chatgpt.com",
    "example.com"
]

print("\n--- Model diagnostics ---")

for url in test_urls:
    prediction = int(model.predict([url])[0])
    score = float(model.decision_function([url])[0])

    label = "PHISHING" if prediction == 1 else "LEGITIMATE"

    print(
        f"{url:22} Prediction: {label:10} "
        f"Decision score: {score:.4f}"
    )
