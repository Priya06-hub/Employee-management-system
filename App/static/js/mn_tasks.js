// Auto-generate Task ID
document.getElementById("taskId").value = "TASK-" + Math.floor(10000 + Math.random() * 90000);

const form = document.getElementById("taskForm");

let total = 0;
let completed = 0;
let pending = 0;

form.addEventListener("submit", function (e) {
    e.preventDefault();

    const startDate = new Date(document.getElementById("startDate").value);
    const dueDate = new Date(document.getElementById("dueDate").value);
    const completedDate = new Date(document.getElementById("completedDate").value);

    if (dueDate <= startDate) {
        alert("Due date must be after Start date");
        return;
    }

    if (completedDate <= startDate) {
        alert("Completed date must be after Start date");
        return;
    }

    const status = document.querySelector('input[name="status"]:checked').value;

    total++;
    if (status === "completed") completed++;
    if (status === "pending") pending++;

    document.getElementById("totalTasks").innerText = total;
    document.getElementById("completedTasks").innerText = completed;
    document.getElementById("pendingTasks").innerText = pending;

    alert("Task Assigned Successfully!");

    form.reset();
    document.getElementById("taskId").value = "TASK-" + Math.floor(10000 + Math.random() * 90000);
});
