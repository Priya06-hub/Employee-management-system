from datetime import date
from django.utils.timezone import now
from .models import Employee, monthly_attendance, leave

def auto_mark_absent():
    today = date.today()

    employees = Employee.objects.all()

    for emp in employees:

        # 1️⃣ Check if attendance already exists
        attendance_exists = monthly_attendance.objects.filter(
            emp=emp,
            date=today
        ).exists()

        if attendance_exists:
            continue

        # 2️⃣ Check approved leave
        on_leave = leave.objects.filter(
            emp=emp,
            status="Approved",
            from_date__lte=today,
            to_date__gte=today
        ).exists()

        if on_leave:
            monthly_attendance.objects.create(
                emp=emp,
                date=today,
                status="Leave"
            )
        else:
            monthly_attendance.objects.create(
                emp=emp,
                date=today,
                status="Absent"
            )
