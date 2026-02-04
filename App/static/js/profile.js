document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("employeeForm");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        // Get values
        const firstName = document.getElementById("firstName").value.trim();
        const lastName = document.getElementById("lastName").value.trim();
        const address = document.getElementById("address").value.trim();
        const email = document.getElementById("email").value.trim();
        const contact = document.getElementById("contact").value.trim();
        const type = document.getElementById("type").value;
        const dob = document.getElementById("dob").value;
        const doj = document.getElementById("doj").value;
        const designation = document.getElementById("designation").value;
        const salary = document.getElementById("salary").value;
        const password = document.getElementById("password").value;
        const department = document.getElementById("department").value;

        const genderChecked = document.querySelector('input[name="gender"]:checked');
        const statusChecked = document.querySelector('input[name="status"]:checked');

        /* ===============================
           1️⃣ Mandatory Field Validation
        ================================ */
        if (
            !firstName || !lastName || !address || !email || !contact ||
            !type || !dob || !doj || !designation || !salary ||
            !password || !department || !genderChecked || !statusChecked
        ) {
            alert("All fields are mandatory.");
            return;
        }

        /* ===============================
           2️⃣ First & Last Name Validation
        ================================ */
        if (firstName.length <= 1 || lastName.length <= 1) {
            alert("First Name and Last Name must contain more than one letter.");
            return;
        }

        /* ===============================
           3️⃣ Contact Number Validation
        ================================ */
        const contactPattern = /^[0-9]{10}$/;
        if (!contactPattern.test(contact)) {
            alert("Contact number must be exactly 10 digits and numeric.");
            return;
        }

        /* ===============================
           4️⃣ Email Validation
        ================================ */
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            alert("Please enter a valid email address.");
            return;
        }

        /* ===============================
           5️⃣ Date of Birth Validation
        ================================ */
        const dobDate = new Date(dob);
        const today = new Date();

        let age = today.getFullYear() - dobDate.getFullYear();
        const monthDiff = today.getMonth() - dobDate.getMonth();

        if (
            monthDiff < 0 ||
            (monthDiff === 0 && today.getDate() < dobDate.getDate())
        ) {
            age--;
        }

        if (age < 20) {
            alert("Employee must be at least 20 years old.");
            return;
        }

        /* ===============================
           6️⃣ Date of Joining Validation
        ================================ */
        const dojDate = new Date(doj);
        if (dojDate > today) {
            alert("Date of Joining cannot be greater than today.");
            return;
        }

        /* ===============================
           7️⃣ Password Validation//incomplete
        ================================ */
        const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8}$/;
        if (!passwordPattern.test(password)) {
            alert("Password must be 8 characters long and contain letters and numbers.");
            return;
        }

        /* ===============================
           ✅ All Validations Passed
        ================================ */
        alert("Employee Profile submitted successfully!");
        form.reset();
    });
});
