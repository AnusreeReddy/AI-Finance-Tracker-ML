document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('transaction-form');
    const backBtn = document.getElementById("back-btn");

    if (!form) return;

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const amount = parseFloat(document.getElementById('amount').value);
        const description = document.getElementById('description').value.trim();
        const username = localStorage.getItem("loggedInUserEmail");

        if (!amount || amount <= 0 || !description || !username) {
            alert("Please enter valid details and make sure you are logged in.");
            return;
        }

        fetch('http://127.0.0.1:5000/api/add_transaction', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, amount, description })
        })
        .then(res => {
            if (!res.ok) {
                return res.json().then(errorData => {
                    throw new Error(errorData.message || `HTTP error! Status: ${res.status}`);
                });
            }
            return res.json();
        })
        .then(data => {
            if (data.status === "success") {
                const predictedCategory = data.predicted_category;
                const predictedType = data.predicted_type;
                alert(`Transaction added! Category: ${predictedCategory} (${predictedType})`);
                window.location.href = "dashboard.html";
            } else {
                alert("Failed to add transaction: " + data.message);
            }
        })
        .catch(err => {
            console.error("Error during fetch:", err);
            alert("Error processing your request: " + err.message);
        });
    });

    if (backBtn) {
        backBtn.addEventListener("click", () => {
            window.location.href = "dashboard.html";
        });
    }
});