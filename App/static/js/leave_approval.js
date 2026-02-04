const leaveData = [
    {
        leaveId: 101,
        employeeId: "EMP001",
        leaveType: "Sick Leave (SL)",
        startDate: "2025-01-05",
        endDate: "2025-01-07",
        status: "Pending"
    },
    {
        leaveId: 102,
        employeeId: "EMP014",
        leaveType: "Casual Leave (CL)",
        startDate: "2025-01-10",
        endDate: "2025-01-12",
        status: "Pending"
    }
];

const tableBody = document.getElementById("leaveTable");

function renderLeaves() {
    tableBody.innerHTML = "";

    leaveData.forEach((leave, index) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${leave.leaveId}</td>
            <td>${leave.employeeId}</td>
            <td>${leave.leaveType}</td>
            <td>${leave.startDate}</td>
            <td>${leave.endDate}</td>
            <td>
                <input type="radio" name="status-${index}" value="Approved"> Approve
                <input type="radio" name="status-${index}" value="Rejected"> Reject
            </td>
            <td>
                <button onclick="updateStatus(${index})">
                    Submit Application
                </button>
            </td>
        `;

        tableBody.appendChild(row);
    });
}

function updateStatus(index) {
    const radios = document.getElementsByName(`status-${index}`);
    let selectedStatus = "";

    radios.forEach(radio => {
        if (radio.checked) {
            selectedStatus = radio.value;
        }
    });

    if (!selectedStatus) {
        alert("Please select Approve or Reject");
        return;
    }

    leaveData[index].status = selectedStatus;
    alert(`Leave ID ${leaveData[index].leaveId} ${selectedStatus}`);
}

renderLeaves();
