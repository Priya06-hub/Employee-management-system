document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();
    // const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorMsg = document.getElementById("errorMsg");

    // if (typeof(username) === "string") {
    //     errorMsg.textContent = "Enter emp id";
    // }
    // Password rules:
    // At least 8 characters
    // Must contain letters and numbers
    const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;


    if (!passwordPattern.test(password)) {
        errorMsg.textContent =
            "Password must be at least 8 characters and include letters & numbers.";
        return;
    }

    errorMsg.textContent = "";
    // alert("Login validation successful!");
});