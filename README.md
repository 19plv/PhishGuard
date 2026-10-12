# PhishGuard — Phishing Website Detection System

## 1. Project Overview

PhishGuard is a machine-learning-based web application designed to classify URLs as potentially phishing or legitimate. It provides a simple interface where users can enter a URL and view the model's prediction.

## 2. Objectives

- Identify potentially suspicious website URLs.
- Apply machine learning to URL classification.
- Provide an easy-to-use web interface.
- Display predictions through a backend API.
- Help users understand the risks associated with suspicious links.

## 3. Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Machine Learning:** scikit-learn
- **Model:** TF-IDF character n-grams with Linear Support Vector Classification (LinearSVC)
- **Dataset:** A labelled CSV dataset containing URLs classified as good or bad.

## 4. System Workflow

1. The user enters a URL in the website.
2. JavaScript sends the URL to the Flask API.
3. The backend validates the input and analyses URL characteristics.
4. The trained machine learning model predicts the URL's class.
5. The backend returns the result as JSON.
6. The frontend displays the prediction and available indicators.

## 5. Dataset and Model

The dataset contains approximately 507,000 URL records, labelled as good or bad. The model was trained using a stratified train-test split.

The current model achieved approximately 97.78% accuracy on its held-out test split. This result applies to that evaluation setup and does not guarantee equivalent accuracy on unseen websites.

## 6. Limitations

- The model can incorrectly classify legitimate URLs.
- New or previously unseen domains may be misclassified.
- A model prediction is not a guarantee that a website is safe or malicious.
- The system does not replace browser security warnings or other security tools.

## 7. How to Run

1. Install Python and the project's required dependencies.
2. Activate the project's virtual environment. -> .\.venv\Scripts\Activate.ps1
You should see (.venv) at the beginning of your terminal line.
3. Ensure the trained model exists at `model/phishing_model.joblib`.
4. Run `python app.py` from the project directory.
5. Open the local web address printed by Flask in your browser.
( venu, python, live server)


## 8. Future Enhancements

- Improve the quality and diversity of the training dataset.
- Evaluate the model on URLs from previously unseen domains.
- Improve detection of deceptive and lookalike domains.
- Add more comprehensive security tests.
- Deploy the application for online access.

## 9. Disclaimer

PhishGuard is an educational project. Its predictions are indicative only and should not be treated as definitive security verdicts.