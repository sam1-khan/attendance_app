from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone
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
        return f"{self.user.get_full_name()}, {self.role}, {'Active' if self.user.is_active else 'Unactive'}"


class Attendance(models.Model) :
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_checked_in = models.BooleanField(default=False)
    is_checked_out = models.BooleanField(default=False)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_owner')

    #Shows up in the admin list
    def __str__(self):
        local_check_in = timezone.localtime(self.check_in).strftime('%d-%m-%Y, %I:%M%p')
        local_check_out = str(self.check_out)

        if self.check_out:
            local_check_out = timezone.localtime(self.check_out).strftime('%d-%m-%Y, %I:%M%p')

        return local_check_in + ' - ' + local_check_out
