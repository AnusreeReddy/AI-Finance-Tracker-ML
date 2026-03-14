document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault();
            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value;
            const users = JSON.parse(localStorage.getItem("users")) || [];
            const matchedUser = users.find(user => user.email === email && user.password === password);
            if (matchedUser) {
                localStorage.setItem("loggedInUser", matchedUser.name || "User");
                localStorage.setItem("loggedInUserEmail", matchedUser.email);
                window.location.href = "dashboard.html";
            } else {
                alert("Invalid email or password.");
            }
        });
    }
});