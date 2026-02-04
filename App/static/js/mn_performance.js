const managerId = "MGR001"; // simulate logged-in manager

function loadEmployee() {
    const empInput = document.getElementById("employeeIdInput").value.trim();
    if (!empInput) {
        alert("Please enter Employee ID");
        return;
    }

    // Simulated fetched data
    const attendanceScore = Math.floor(70 + Math.random() * 30);
    const taskScore = Math.floor(65 + Math.random() * 35);

    document.getElementById("performanceFormSection").style.display = "block";

    document.getElementById("performanceId").value =
        "PERF-" + Math.floor(10000 + Math.random() * 90000);

    document.getElementById("employeeId").value = empInput;
    document.getElementById("attendanceScore").value = attendanceScore;
    document.getElementById("taskScore").value = taskScore;
    document.getElementById("reviewedBy").value = managerId;

    const today = new Date().toISOString().split("T")[0];
    document.getElementById("reviewedDate").value = today;

    calculatePerformance(attendanceScore, taskScore);
}

function calculatePerformance(attendance, task) {
    const performance = ((attendance + task) / 2).toFixed(2);
    document.getElementById("performanceScore").value = performance + " %";
}

document.getElementById("performanceForm").addEventListener("submit", function(e) {
    e.preventDefault();
    alert("Employee performance updated successfully!");
});
