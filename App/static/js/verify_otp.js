
document.getElementById("forgotForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const otp = document.querySelector('input[name="otp"]').value.trim();
    const newPassword = document.querySelector('input[name="new_password"]').value;
    const confirmPassword = document.querySelector('input[name="con_pwd"]').value;
    const errorMsg = document.getElementById("errorMsg");
    const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;

    errorMsg.style.color = "red";
    errorMsg.textContent = "";

    // OTP validation
    if (otp === "") {
        errorMsg.textContent = "OTP is required.";
        return;
    }

    if (!/^[0-9]{6}$/.test(otp)) {
        errorMsg.textContent = "OTP must be 6 digits only.";
        return;
    }

    // New password validation
    if (newPassword === "") {
        errorMsg.textContent = "New password is required.";
        return;
    }

    if (!passwordPattern.test(newPassword)) {
        errorMsg.textContent =
            "Password must be at least 8 characters and include letters & numbers.";
        return;
    }
    // Confirm password validation
    if (confirmPassword === "") {
        errorMsg.textContent = "Confirm password is required.";
        return;
    }
    if (!passwordPattern.test(confirmPassword)) {
        errorMsg.textContent =
            "Password must be at least 8 characters and include letters & numbers.";
        return;
    }

    if (newPassword !== confirmPassword) {
        errorMsg.textContent = "Passwords do not match.";
        return;
    }

    // ✅ All validations passed
    errorMsg.textContent = "";
    this.submit();
});

