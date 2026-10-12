
const scanForm = document.getElementById("scanForm");
const urlInput = document.getElementById("urlInput");

const resultIcon = document.getElementById("resultIcon");
const resultTitle = document.getElementById("resultTitle");
const resultDescription = document.getElementById("resultDescription");
const statusBadge = document.getElementById("statusBadge");
const resultDetails = document.getElementById("resultDetails");
const disclaimer = document.getElementById("disclaimer");

scanForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const url = urlInput.value.trim();

    if (!url) {
        showError("Please enter a website URL.");
        return;
    }

    setLoading();

    try {
        const response = await fetch(
            "http://127.0.0.1:5000/api/scan",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            showError(data.error || "Unable to check this URL.");
            return;
        }

        displayResult(data);

    } catch (error) {
        showError(
            "Could not connect to Python. Make sure Flask is running."
        );
    }
});

function setLoading() {
    resultIcon.textContent = "...";
    resultTitle.textContent = "Analysing URL...";
    resultDescription.textContent =
        "The model is examining the submitted URL.";

    statusBadge.textContent = "Processing";
    resultDetails.textContent = "Please wait...";
    disclaimer.textContent = "No prediction has been returned yet.";
}

function displayResult(data) {
    const isPhishing = data.prediction === "phishing";
    const indicators = Array.isArray(data.indicators)
        ? data.indicators
        : [];

    resultIcon.textContent = isPhishing ? "!" : "✓";
    resultIcon.style.color = isPhishing ? "#b91c1c" : "#078c42";
    resultIcon.style.borderColor = isPhishing ? "#b91c1c" : "#078c42";

    resultTitle.textContent = isPhishing
        ? "Potential phishing detected"
        : "Predicted legitimate";

    resultDescription.textContent =
        "Website checked: " + data.domain;

    statusBadge.textContent = isPhishing
        ? "Phishing prediction"
        : "Legitimate prediction";

    statusBadge.style.backgroundColor = isPhishing
        ? "#fee2e2"
        : "#d1fae5";

    statusBadge.style.color = isPhishing
        ? "#991b1b"
        : "#065f46";

    resultDetails.replaceChildren();

    const message = document.createElement("p");
    message.textContent = data.message;
    resultDetails.appendChild(message);

    if (indicators.length > 0) {
        const heading = document.createElement("p");
        heading.textContent = "Additional URL indicators:";
        resultDetails.appendChild(heading);

        const list = document.createElement("ul");

        indicators.forEach(function (indicator) {
            const item = document.createElement("li");
            item.textContent = indicator;
            list.appendChild(item);
        });

        resultDetails.appendChild(list);
    }

    disclaimer.textContent =
        "Machine-learning predictions can be wrong. " +
        "A legitimate prediction does not guarantee safety.";
}

function showError(message) {
    resultIcon.textContent = "!";
    resultTitle.textContent = "Unable to check URL";
    resultDescription.textContent = message;

    statusBadge.textContent = "Error";
    resultDetails.textContent =
        "Check the URL and make sure the backend is running.";

    disclaimer.textContent = "No prediction was produced.";

    resultIcon.style.color = "#b91c1c";
    resultIcon.style.borderColor = "#b91c1c";
    statusBadge.style.backgroundColor = "#fee2e2";
    statusBadge.style.color = "#991b1b";
}
