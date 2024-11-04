from .models import Attendance
from celery import shared_task
from django.contrib.auth import get_user_model
from django.template.defaultfilters import pluralize
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@shared_task
def send_reminder():
    employees_to_remind = Attendance.objects.filter(
        is_checked_out=False,
        check_in__isnull=False,
        check_out__isnull=True
    )

    count = employees_to_remind.count()
    s = pluralize(count)

    for emp in employees_to_remind:
        subject = "Reminder: You have not checked out!"
        context = {
            'name': emp.employee.get_full_name() if emp.employee.first_name else emp.employee.get_username(),
        }
        html_content = render_to_string('notification/reminder_email.html', context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            to=[emp.employee.email],
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

    return f'Sent Email{s} to {count} employee{s}'


@shared_task
def send_update_passwrd(user_id, passwrd):
    Employee = get_user_model()
    try:
        new = Employee.objects.get(pk=user_id)
        subject = "Important: Set Up Your Password for Your New Account"
        context = {
            'name': new.get_full_name() if new.first_name else new.get_username(),
            'username': new.get_username(),
            'temporary_password': passwrd,
        }

        html_content = render_to_string('registration/password_setup_email.html', context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            to=[new.email],
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

        return f'Sent Email to new user, id: {user_id}'
    except:
        return f'Could not Send Email to new user, id: {user_id}'
        