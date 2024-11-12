from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .managers import CustomUserManager
# Create your models here.


class Employee(AbstractUser):
    ROLE_CHOICES = (
        ('SWE', _('Software Engineer')),
        ('DE', _('Data Engineer')),
        ('DS', _('Data Scientist')),
        ('FE', _('Frontend Engineer')),
        ('BE', _('Backend Engineer')),
        ('FS', _('Full Stack Engineer')),
        ('ML', _('Machine Learning Engineer')),
        ('QA', _('Quality Assurance Engineer')),
    )

    username = None
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=3, default='SWE')


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name",]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.get_full_name() if self.first_name else self.get_username()}, {self.role}, {_('Active') if self.is_active else _('Unactive')}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if this is a new record
        super().save(*args, **kwargs)  # Save first so we have the user ID

        if is_new:  # If this was a new record
            from .tasks import send_password_update
            send_password_update.delay(self.id)


class Attendance(models.Model) :
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_checked_out = models.BooleanField(default=False)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        local_check_in = timezone.localtime(self.check_in).strftime('%d-%m-%Y, %I:%M%p')
        local_check_out = str(self.check_out)

        if self.check_out:
            local_check_out = timezone.localtime(self.check_out).strftime('%d-%m-%Y, %I:%M%p')

        return local_check_in + ' - ' + local_check_out

    def clean(self):
        if self.pk is None:  # This means we're creating a new attendance record
            try:
                current_time = timezone.now()
                time_threshold = current_time - timedelta(hours=24)

                existing_records = Attendance.objects.filter(
                    employee=self.employee,
                    check_in__range=[time_threshold, current_time]
                )

                if existing_records.exists():
                    raise ValidationError(_("An attendance record for this employee already exists within the last 24 hours."))
            except ObjectDoesNotExist:
                raise ValidationError(_("Employee field for the attendance record can't be empty."))

        if self.pk is not None:  # This means the object already exists
            original = get_object_or_404(Attendance, pk=self.pk)
            if original.is_checked_out != self.is_checked_out:
                if original.is_checked_out:
                    raise ValidationError(_("You cannot change is checked out once it's been set."))
                if self.is_checked_out:  # If being checked out
                    self.check_out = timezone.now()  # Set check_out to current time

    def save(self, *args, **kwargs):
        if self.is_checked_out and self.check_out is None:
            self.check_out = timezone.now()
        super().save(*args, **kwargs)