document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("changePassForm");
    const errorMsg = document.getElementById("errorMsg");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const newPassword = document.getElementById("newPassword").value.trim();
        const confirmPassword = document.getElementById("confirmPassword").value.trim();

        const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;


        if (!passwordPattern.test(newPassword)) {
            errorMsg.textContent =
                "Password must be at least 8 characters and include letters & numbers.";
            return;
        }

        if (newPassword !== confirmPassword) {
            errorMsg.textContent = "Passwords do not match.";
            return;
        }

        errorMsg.textContent = "";
        alert("Password changed successfully!");
    });
});
