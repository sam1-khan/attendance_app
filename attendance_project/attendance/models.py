from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
# Create your models here.


class Employee(models.Model) :
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    ROLE_CHOICES = (
        ('SWE', 'Software Engineer'),
        ('DE', 'Data Engineer'),
        ('DS', 'Data Scientist'),
        ('FE', 'Frontend Engineer'),
        ('BE', 'Backend Engineer'),
        ('FS', 'Full Stack Engineer'),
        ('ML', 'Machine Learning Engineer'),
        ('QA', 'Quality Assurance Engineer'),
    )

    role = models.CharField(choices=ROLE_CHOICES, max_length=3, default='SWE')

    # Shows up in the admin list
    def __str__(self):
        return f"{self.user.get_full_name() if self.user.first_name else self.user.get_username()}, {self.role}, {'Active' if self.user.is_active else 'Unactive'}"


class Attendance(models.Model) :
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_checked_out = models.BooleanField(default=False)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)

    # Shows up in the admin list
    def __str__(self):
        local_check_in = timezone.localtime(self.check_in).strftime('%d-%m-%Y, %I:%M%p')
        local_check_out = str(self.check_out)

        if self.check_out:
            local_check_out = timezone.localtime(self.check_out).strftime('%d-%m-%Y, %I:%M%p')

        return local_check_in + ' - ' + local_check_out

    # Reminder Mails for checkout
    def send_reminder(self):
        current_time = timezone.now()
        reminder_threshold = current_time - timedelta(minutes=10)
        employees_to_remind = Attendance.objects.filter(
            is_checked_out=False,
            check_out__isnull=True,
            check_in__lt=reminder_threshold  # Ensure the check_in is before the reminder threshold
        )

        for attendance in employees_to_remind:
            subject = "Reminder: You have not checked out!"
            message = (
                f"Hello {self.employee.user.get_full_name() if self.employee.user.first_name else self.employee.user.get_username()},\n\n"
                "This is a reminder that you have not marked your checkout for today. "
                "Please make sure to check out to complete your attendance record.\n\n"
                "Thank you!"
            )
            recipient_list = [self.employee.user.email]
            
            # Send email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )

    def clean(self):
        # Check if an attendance record already exists for this employee on the same date
        if self.pk is None:  # This means we're creating a new attendance record
            # Get the current time
            current_time = timezone.now()
            # Calculate the time 24 hours ago
            time_threshold = current_time - timedelta(hours=24)

            existing_records = Attendance.objects.filter(
                employee=self.employee,
                check_in__range=[time_threshold, current_time]
            )

            if existing_records.exists():
                raise ValidationError("An attendance record for this employee already exists within the last 24 hours.")

        # Ensure is_checked_out can only be changed once
        if self.pk is not None:  # This means the object already exists
            original = get_object_or_404(Attendance, pk=self.pk)
            if original.is_checked_out != self.is_checked_out:
                # If is_checked_out is being changed, ensure it's the first time
                if original.is_checked_out:
                    raise ValidationError("You cannot change is checked out once it's been set.")
                if self.is_checked_out:  # If being checked out
                    self.check_out = timezone.now()  # Set check_out to current time

        if self.check_in:
            # Set a threshold to check for reminders
            reminder_threshold = self.check_in + timedelta(minutes=10)

            if not self.is_checked_out and timezone.now() >= reminder_threshold:
                self.send_reminder()  # Call the reminder function

    def save(self, *args, **kwargs):
        # Set check_out time if is_checked_out is being set to True
        if self.is_checked_out and self.check_out is None:
            self.check_out = timezone.now()
        super().save(*args, **kwargs)
