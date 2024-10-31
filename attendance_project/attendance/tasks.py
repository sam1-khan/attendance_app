import datetime
from .models import Attendance
from celery import shared_task

@shared_task
def send_reminder():
    employees_to_remind = Attendance.objects.filter(
        is_checked_out=False,
        check_in__isnull=False,
        check_out__isnull=True
    )

    for emp in employees_to_remind:
        subject = "Reminder: You have not checked out!"
        message = (
            f"Hello {emp.employee.user.get_full_name() if emp.employee.user.first_name else emp.employee.user.get_username()},\n\n"
            "This is a reminder that you have not marked your checkout for today. "
            "Please make sure to check out to complete your attendance record.\n\n"
            "Thank you!"
        )

        # Send email
        emp.employee.user.email_user(
            subject,
            message
        )

    return f'Sent Emails to {employees_to_remind.count()} employees'