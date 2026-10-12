
from pathlib import Path

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "phishing_site_urls.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "phishing_model.joblib"

# 1. Load dataset
print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset columns:", df.columns.tolist())

# 2. Validate required columns
required_columns = {"URL", "Label"}

if not required_columns.issubset(df.columns):
    raise ValueError(
        "CSV must contain columns named URL and Label."
    )

df = df[["URL", "Label"]].dropna()

df["URL"] = df["URL"].astype(str).str.strip()
df["Label"] = df["Label"].astype(str).str.strip().str.lower()

# Keep only the expected labels
df = df[df["Label"].isin(["good", "bad"])]

# Remove empty URLs and duplicate URLs
df = df[df["URL"] != ""]
df = df.drop_duplicates(subset=["URL"])

# bad = phishing (1), good = legitimate (0)
df["target"] = df["Label"].map({
    "good": 0,
    "bad": 1
})

print("\nDataset size:", len(df))
print("Label counts:")
print(df["Label"].value_counts())

# 3. Split before training
X_train, X_test, y_train, y_test = train_test_split(
    df["URL"],
    df["target"],
    test_size=0.20,
    random_state=42,
    stratify=df["target"]
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# 4. Create the machine-learning pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            analyzer="char",
            ngram_range=(3, 5),
            max_features=100000,
            lowercase=True,
            sublinear_tf=True,
            dtype="float32"
        )
    ),
    (
        "classifier",
        LinearSVC(
            class_weight="balanced",
            random_state=42
        )
    )
])

# 5. Train the model
print("\nTraining model. This may take a while...")

model.fit(X_train, y_train)

# 6. Evaluate on unseen test data
predictions = model.predict(X_test)

print("\nAccuracy:", round(
    accuracy_score(y_test, predictions), 4
))

print("\nClassification report:")
print(
    classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Legitimate", "Phishing"],
        digits=4
    )
)

print("Confusion matrix:")
print(
    confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1]
    )
)

# 7. Save the complete pipeline
MODEL_DIR.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("\nModel saved to:", MODEL_PATH)
print("Training complete!")
