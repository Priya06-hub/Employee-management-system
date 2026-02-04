function loadAttendance() {
    const empId = document.getElementById("empId").value.trim();
    const date = document.getElementById("attendanceDate").value;

    if (!empId || !date) {
        alert("Please enter Employee ID and Date");
        return;
    }

    // Show attendance form
    document.getElementById("attendanceForm").style.display = "block";

    // Pre-fill values (simulated data – later replace with backend data)
    document.getElementById("fEmpId").value = empId;
    document.getElementById("fDate").value = date;

    const checkInField = document.getElementById("checkIn");
    const checkOutField = document.getElementById("checkOut");

    checkInField.value = "09:30";
    checkOutField.value = "18:00";

    // 🔓 Allow HR to edit both times
    checkInField.removeAttribute("readonly");
    checkOutField.removeAttribute("readonly");

    document.getElementById("status").value = "Absent";
}

function updateAttendance() {
    const checkIn = document.getElementById("checkIn").value;
    const checkOut = document.getElementById("checkOut").value;
    const status = document.getElementById("status").value;

    if (!checkIn || !checkOut) {
        alert("Please enter both Check-in and Check-out times");
        return;
    }

    // ⛔ Constraint: Check-out must be after Check-in
    if (checkOut <= checkIn) {
        alert("Check-out time must be after Check-in time");
        return;
    }

    // Optional validation: auto-mark present if times are valid
    if (status === "Absent") {
        const confirmChange = confirm(
            "Check-in and Check-out times are provided. Mark status as Present?"
        );
        if (confirmChange) {
            document.getElementById("status").value = "Present";
        }
    }

    alert("Attendance updated successfully!");
}
