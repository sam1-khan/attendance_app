from .models import Attendance
from celery import shared_task
from django.contrib.auth.models import User
from django.template.defaultfilters import pluralize

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
    x = employees_to_remind.count()
    s = pluralize(x)
    return f'Sent Email{s} to {x} employees {s}'


@shared_task
def send_update_passwrd(user_id, passwrd):
    new = User.get(id=user_id)
    try:
        subject = "Important: Set Up Your Password for Your New Account"
        message = (
            f"Hello {new.get_full_name() if new.first_name else new.get_username()},\n\n"
            "Your HR has created an account for you on our attendance platform.\n\n"
            "Login Details:\n"
            f"Username: {new.get_username()}\n"
            f"Temporary Password: {passwrd}\n\n"
            "Next Steps:\n"
            "1. Log in with the temporary password.\n"
            "2. Go to “Account Settings” to set a new password.\n\n"
            "Thank you!"
        )

        # Send email
        new.email_user(
            subject,
            message
        )
        return f'Sent Email to new user: {user_id}'
    except:
        return f'Could not Send Email to new user: {user_id}'
        