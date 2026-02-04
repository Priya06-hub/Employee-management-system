from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import monthly_attendance, attendance, leave
@receiver(post_save, sender=monthly_attendance)
def update_attendance_from_daily(sender, instance, created, **kwargs):
    if not created:
        return

    emp = instance.Emp_id
    month_start = instance.date.replace(day=1)

    att, created_att = attendance.objects.get_or_create(
        Emp_id=emp,
        month=month_start,
        defaults={
            'Present_days': 0,
            'absent_days': 0,
            'leave_days': 0,
            'Total_days': 0
        }
    )

    if instance.status.lower() == 'present':
        att.Present_days += 1

    elif instance.status.lower() == 'absent':
        att.absent_days += 1

    att.Total_days = att.Present_days + att.absent_days + att.leave_days
    att.save()
@receiver(post_save, sender=leave)
def update_attendance_from_leave(sender, instance, **kwargs):
    if instance.status.lower() != 'approved':
        return

    emp = instance.Emp_id
    month_start = instance.start_date.replace(day=1)

    att, created_att = attendance.objects.get_or_create(
        Emp_id=emp,
        month=month_start,
        defaults={
            'Present_days': 0,
            'absent_days': 0,
            'leave_days': 0,
            'Total_days': 0
        }
    )

    att.leave_days += instance.Total_days
    att.Total_days = att.Present_days + att.absent_days + att.leave_days
    att.save()
