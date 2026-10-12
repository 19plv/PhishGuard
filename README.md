# PhishGuard — Phishing Website Detection System

A machine-learning-based web application that classifies website URLs as potentially phishing or legitimate, with SHA-256 file integrity verification for the trained model.

## 1. Project Overview

PhishGuard combines machine learning, web development, and a cryptographic integrity check to demonstrate two security concepts:

- **Phishing URL detection:** predicts whether a submitted URL resembles phishing or legitimate examples in the training dataset.
- **File integrity verification:** uses SHA-256 to check whether the trained model matches a previously recorded hash.

PhishGuard is an educational project. Its predictions do not guarantee that a website is safe or malicious.

## 2. Objectives

- Identify potentially suspicious website URLs.
- Apply machine learning to URL classification.
- Provide an easy-to-use web interface.
- Connect the frontend to a Flask API.
- Demonstrate SHA-256-based file integrity verification.
- Evaluate model performance and document its limitations.

## 3. Technologies Used

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| API | Flask JSON endpoints |
| Machine learning | scikit-learn |
| Feature extraction | TF-IDF character n-grams |
| Classifier | Linear Support Vector Classification (LinearSVC) |
| Cryptography | SHA-256 |
| Model storage | Joblib |

## 4. System Workflow

### Phishing detection

1. The user enters a URL in the web interface.
2. JavaScript sends the URL to the Flask API.
3. The backend validates the input and analyses basic URL characteristics.
4. The trained model predicts the URL's class.
5. The backend returns the prediction and indicators as JSON.
6. The frontend displays the result.

### SHA-256 integrity verification

1. PhishGuard calculates the SHA-256 hash of the saved model file.
2. It compares the calculated hash with the saved reference hash.
3. If the hashes match, the file is reported as matching the reference.
4. If the hashes differ, the integrity check fails.

**Security limitation:** The reference hash is stored alongside the model. This is suitable for demonstrating the concept, but it is not tamper-proof if an attacker can modify both files.

## 5. Dataset and Model

The dataset used for training contains approximately 507,000 URL records labelled as `good` or `bad`.

The model uses character-level TF-IDF features and a LinearSVC classifier. The trained model is saved as `model/phishing_model.joblib`.

In the recorded held-out test evaluation, the model achieved approximately **97.78% accuracy**. This metric applies to that particular evaluation setup and does not guarantee equivalent performance on previously unseen domains.

The dataset is not included in this GitHub repository. The trained model is included.

## 6. Cryptographic Experiment

The SHA-256 integrity checker calculates a 256-bit cryptographic hash, represented as 64 hexadecimal characters.

The integrity experiment produced these results:

| Test | Expected result | Observed result |
|---|---|---|
| Verify an unchanged test file | Hashes match | Passed |
| Verify a modified test file against the original hash | Hashes differ | Passed |
| Verify the saved model against its recorded hash | Integrity verified | Passed |

The tamper-detection experiment used a temporary test file. The actual trained model was not modified during that experiment.

A matching hash establishes consistency with the recorded reference; it does not independently establish that the file is trustworthy.

## 7. Project Structure

```text
PhishGuard/
├── app.py
├── train_model.py
├── check_model.py
├── evaluate_urls.py
├── integrity_checker.py
├── test_integrity.py
├── index.html
├── style.css
├── script.js
├── requirements.txt
├── README.md
├── .gitignore
├── data/                 # Dataset excluded from Git
└── model/
    ├── phishing_model.joblib
    └── trusted_model_hash.txt
```

## 8. How to Run Locally

### Prerequisites

- Python installed on your computer
- Git installed if cloning the repository
- The trained model and its reference hash

### Step 1: Clone the repository

```bash
git clone https://github.com/19plv/PhishGuard.git
cd PhishGuard
```

### Step 2: Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Start the application

```powershell
python app.py
```

Open the local address printed by Flask in your browser, usually `http://127.0.0.1:5000`.

### Step 5: Check model integrity

With the Flask application running, open:

`http://127.0.0.1:5000/api/integrity`

A successful response reports `"integrity": "verified"`.

**Note:** The dataset is excluded from the repository. To retrain the model, obtain the dataset from its original source, subject to its licence and availability.

## 9. API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Check backend status |
| `/api/scan` | POST | Submit a URL for classification |
| `/api/integrity` | GET | Verify model-file integrity |

## 10. Limitations

- The model can incorrectly classify legitimate URLs.
- New or previously unseen domains may be misclassified.
- Accuracy on the recorded test split may not represent real-world performance.
- SHA-256 verification depends on the integrity of the saved reference hash.
- A model prediction does not guarantee that a website is safe.
- PhishGuard does not replace browser security warnings or professional security tools.

## 11. Future Enhancements

- Evaluate the model using previously unseen domains.
- Improve the quality and diversity of the training dataset.
- Reduce false positives on legitimate websites.
- Protect the trusted hash using a stronger trust mechanism.
- Add further security tests and improve error handling.
- Deploy the application for online access.

## 12. Disclaimer

PhishGuard is an educational project developed to demonstrate machine learning-based URL classification and cryptographic file integrity verification. Its outputs are indicative only and should not be treated as definitive security verdicts.