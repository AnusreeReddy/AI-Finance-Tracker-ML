document.addEventListener("DOMContentLoaded", function () {
    const userGreeting = document.getElementById("user-greeting");
    const savingsEl = document.getElementById("summary-savings");
    const expensesEl = document.getElementById("summary-expenses");
    const balanceEl = document.getElementById("summary-balance");
    const addTransactionBtn = document.getElementById("add-transaction-btn");
    const viewTransactionsBtn = document.getElementById("view-transactions-btn");
    const logoutBtn = document.getElementById("logout-btn");
    const username = localStorage.getItem("loggedInUserEmail");
    const user = localStorage.getItem("loggedInUser");

    if (!user || !username) {
        alert("Please login first.");
        window.location.href = "login.html";
        return;
    }

    userGreeting.textContent = `Welcome, ${user}!`;

    fetch(`http://127.0.0.1:5000/api/get_transactions/${username}`)
        .then(res => res.json())
        .then(data => {
            if (data.status === "success" && data.transactions.length > 0) {
                let totalSavings = 0;
                let totalExpenses = 0;

                data.transactions.forEach(t => {
                    if (t.type.toLowerCase() === "savings") totalSavings += parseFloat(t.amount);
                    else totalExpenses += parseFloat(t.amount);
                });

                savingsEl.textContent = `Total Savings: ₹${totalSavings.toFixed(2)}`;
                expensesEl.textContent = `Total Expenses: ₹${totalExpenses.toFixed(2)}`;
                balanceEl.textContent = `Net Balance: ₹${(totalSavings - totalExpenses).toFixed(2)}`;
            } else {
                savingsEl.textContent = "Total Savings: ₹0.00";
                expensesEl.textContent = "Total Expenses: ₹0.00";
                balanceEl.textContent = "Net Balance: ₹0.00";
            }
        })
        .catch(err => {
            console.error("Error fetching transactions:", err);
            savingsEl.textContent = "Total Savings: ₹0.00";
            expensesEl.textContent = "Total Expenses: ₹0.00";
            balanceEl.textContent = "Net Balance: ₹0.00";
        });

    addTransactionBtn.addEventListener("click", () => {
        window.location.href = "add_transaction.html";
    });

    viewTransactionsBtn.addEventListener("click", () => {
        window.location.href = "view_transactions.html";
    });

    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("loggedInUser");
        localStorage.removeItem("loggedInUserEmail");
        window.location.href = "login.html";
    });
});