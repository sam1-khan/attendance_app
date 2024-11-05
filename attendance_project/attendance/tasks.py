from .models import Attendance
from celery import shared_task
from datetime import timedelta
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.template.defaultfilters import pluralize
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils import timezone

@shared_task
def send_reminder():
    try:
        current_time = timezone.now()
        time_threshold = current_time - timedelta(hours=24)

        employees_to_remind = Attendance.objects.filter(
            is_checked_out=False,
            check_in__isnull=False,
            check_out__isnull=True,
            check_in__range=[time_threshold, current_time]
        )

        count = employees_to_remind.count()
        s = pluralize(count)

        for emp in employees_to_remind:
            subject = "Reminder: You have not checked out!"
            context = {
                'name': emp.employee.get_full_name() if emp.employee.first_name else emp.employee.get_username(),
                'domain': settings.DOMAIN_NAME,
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
    except Exception as e:
        return f'Could not Send {count} Email{s}, Error: {str(e)}'  


@shared_task
def send_password_update(user_id):
    Employee = get_user_model()
    try:
        new = Employee.objects.get(pk=user_id)
        subject = "Important: Set Up Your Password for Your New Account"

        # Generate the token and UID for the password reset link
        token = default_token_generator.make_token(new)
        uid = urlsafe_base64_encode(force_bytes(new.pk))
        password_reset_url = f"{settings.DOMAIN_NAME}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

        context = {
            'name': new.get_full_name() if new.first_name else new.get_username(),
            'username': new.get_username(),
            'password_reset_url': password_reset_url,
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
    except Exception as e:
        return f'Could not Send Email to new user, id: {user_id}, Error: {str(e)}'
        

@shared_task
def auto_check_out():
    try:
        current_time = timezone.now()
        time_threshold = current_time - timedelta(hours=24)

        employees_to_checkout = Attendance.objects.filter(
            is_checked_out=False,
            check_in__isnull=False,
            check_out__isnull=True,
            check_in__range=[time_threshold, current_time]
        )

        count = employees_to_checkout.count()
        s = pluralize(count)

        for emp in employees_to_checkout:
            emp.check_out = timezone.now()
            emp.is_checked_out = True
            emp.save()

        return f'Auto checked out {count} user{s}'
    except Exception as e:
        return f'Could not check out {count} user{s}, Error {str(e)}'
