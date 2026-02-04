document.getElementById("forgotForm").addEventListener("submit", function (e) {
    e.preventDefault(); // stop default submit

    const empId = document.getElementById("emp_id").value.trim();
    const email = document.getElementById("email").value.trim();
    const errorMsg = document.getElementById("errorMsg");

    errorMsg.style.color = "red";
    errorMsg.textContent = "";

    // Employee ID validation
    if (empId === "") {
        errorMsg.textContent = "Please enter User ID.";
        return;
    }
    //    if (typeof(empId) === "string") {
    //     errorMsg.textContent = " emp id should be in number ";
    //     return;
    // }


    // Email validation
    if (email === "") {
        errorMsg.textContent = "Please enter Email address.";
        return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        errorMsg.textContent = "Please enter a valid Email address.";
        return;
    }

    // ✅ All validations passed
    errorMsg.textContent = "";
    this.submit(); // submit form to Django backend
});
