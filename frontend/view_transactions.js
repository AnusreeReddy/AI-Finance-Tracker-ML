document.addEventListener("DOMContentLoaded", () => {
    const username = localStorage.getItem("loggedInUserEmail");
    const savingsList = document.getElementById("savings-list");
    const expensesList = document.getElementById("expenses-list");
    const savingsTotal = document.getElementById("savings-total");
    const expensesTotal = document.getElementById("expenses-total");
    const backBtn = document.getElementById("back-btn");

    const prevBtn = document.getElementById("prev-btn");
    const nextBtn = document.getElementById("next-btn");
    const pageInfo = document.getElementById("page-info");

    let allTransactions = []; // Store all fetched transactions
    let currentPage = 1;
    const transactionsPerPage = 10; // You can change this number

    if (savingsList && expensesList && savingsTotal && expensesTotal) {
        if (!username) {
            alert("Please login first");
            window.location.href = "login.html";
            return;
        }

        fetch(`http://127.0.0.1:5000/api/get_transactions/${username}`)
            .then((res) => {
                if (!res.ok) {
                    throw new Error(`HTTP error! Status: ${res.status}`);
                }
                return res.json();
            })
            .then((data) => {
                if (data.status === "success") {
                    allTransactions = data.transactions;
                    renderTransactions();
                } else {
                    alert("Failed to load transactions.");
                }
            })
            .catch((err) => {
                console.error(err);
                alert("Error loading transactions. Check the browser console for details.");
            });
    }

    if (backBtn) {
        backBtn.addEventListener("click", () => {
            window.location.href = "dashboard.html";
        });
    }

    function renderTransactions() {
        let totalSavings = 0;
        let totalExpenses = 0;

        savingsList.innerHTML = "";
        expensesList.innerHTML = "";

        const start = (currentPage - 1) * transactionsPerPage;
        const end = start + transactionsPerPage;
        const transactionsToDisplay = allTransactions.slice(start, end);

        if (allTransactions.length === 0) {
            savingsList.innerHTML = "<li>No savings transactions.</li>";
            expensesList.innerHTML = "<li>No expenses transactions.</li>";
        } else {
            transactionsToDisplay.forEach((txn) => {
                const li = document.createElement("li");
                li.textContent = `${txn.description}: ₹${txn.amount} (Category: ${txn.category})`;

                if (txn.type && txn.type.toLowerCase() === "savings") {
                    savingsList.appendChild(li);
                } else {
                    expensesList.appendChild(li);
                }
            });
        }

        // Calculate totals from ALL transactions, not just the displayed ones
        allTransactions.forEach((txn) => {
            if (txn.type && txn.type.toLowerCase() === "savings") {
                totalSavings += parseFloat(txn.amount);
            } else {
                totalExpenses += parseFloat(txn.amount);
            }
        });
        
        savingsTotal.textContent = `Total Savings: ₹${totalSavings.toFixed(2)}`;
        expensesTotal.textContent = `Total Expenses: ₹${totalExpenses.toFixed(2)}`;

        // Update pagination controls
        const totalPages = Math.ceil(allTransactions.length / transactionsPerPage);
        pageInfo.textContent = `Page ${currentPage} of ${totalPages || 1}`;

        prevBtn.disabled = currentPage === 1;
        nextBtn.disabled = currentPage === totalPages;
    }

    // Event listeners for pagination buttons
    if (prevBtn) {
        prevBtn.addEventListener("click", () => {
            if (currentPage > 1) {
                currentPage--;
                renderTransactions();
            }
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", () => {
            const totalPages = Math.ceil(allTransactions.length / transactionsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                renderTransactions();
            }
        });
    }
});