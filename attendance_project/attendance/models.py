from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.conf import settings
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

    #Shows up in the admin list
    def __str__(self):
        return f"{self.user.get_full_name() if self.user.first_name else self.user.get_username()}, {self.role}, {'Active' if self.user.is_active else 'Unactive'}"


class Attendance(models.Model) :
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_checked_out = models.BooleanField(default=False)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)

    #Shows up in the admin list
    def __str__(self):
        local_check_in = timezone.localtime(self.check_in).strftime('%d-%m-%Y, %I:%M%p')
        local_check_out = str(self.check_out)

        if self.check_out:
            local_check_out = timezone.localtime(self.check_out).strftime('%d-%m-%Y, %I:%M%p')

        return local_check_in + ' - ' + local_check_out

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
            original = Attendance.objects.get(pk=self.pk)
            if original.is_checked_out != self.is_checked_out:
                # If is_checked_out is being changed, ensure it's the first time
                if original.is_checked_out:
                    raise ValidationError("You cannot change is checked out once it's been set.")
                if self.is_checked_out:  # If being checked out
                    self.check_out = timezone.now()  # Set check_out to current time

    def save(self, *args, **kwargs):
        # Set check_out time if is_checked_out is being set to True
        if self.is_checked_out and self.check_out is None:
            self.check_out = timezone.now()
        super().save(*args, **kwargs)
