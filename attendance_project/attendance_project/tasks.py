from datetime import timedelta, timezone
from ..attendance.models import Attendance

def send_reminder():
    current_time = timezone.now()
    reminder_threshold = current_time - timedelta(minutes=1)
    employees_to_remind = Attendance.objects.filter(
        is_checked_out=False,
        check_in__lt=reminder_threshold  # Ensure the check_in is before the reminder threshold
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
