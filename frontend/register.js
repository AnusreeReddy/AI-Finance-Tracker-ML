document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("register-form");
    if (registerForm) {
        registerForm.addEventListener("submit", function (event) {
            event.preventDefault();
            const name = document.getElementById("name").value.trim();
            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value;
            const confirmPassword = document.getElementById("confirm-password").value;
            if (password !== confirmPassword) {
                alert("Passwords do not match!");
                return;
            }
            const users = JSON.parse(localStorage.getItem("users")) || [];
            const userExists = users.some(user => user.email === email);
            if (userExists) {
                alert("User already exists.");
                return;
            }
            users.push({ name, email, password });
            localStorage.setItem("users", JSON.stringify(users));
            alert("User registered successfully!");
            window.location.href = "login.html";
        });
    }
});