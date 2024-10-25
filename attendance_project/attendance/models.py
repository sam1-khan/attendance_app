from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


class Person(models.Model) :
    first_name = models.CharField(
            max_length=50,
            validators=[MinLengthValidator(2, "first name must be greater than 2 characters")])
    last_name = models.CharField(
            max_length=50,
            validators=[MinLengthValidator(2, "last name must be greater than 2 characters")])
    email = models.EmailField(max_length=254, unique=True)

    # Shows up in the admin list
    def __str__(self):
        return self.first_name + ' '  + self.last_name


class Status(models.Model) :
    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("UNACTIVE", "Unactive"),
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=8, default='ACTIVE')
   
    def __str__(self):
        return self.status


class Role(models.Model) :

    def __str__(self):
        return self.role


class Employee(models.Model) :
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("UNACTIVE", "Unactive"),
    )
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
    status = models.CharField(choices=STATUS_CHOICES, max_length=8, default='ACTIVE')
    
    #Shows up in the admin list
    def __str__(self):
        return self.person.first_name + ' - ' +  self.role + ' - '  + self.status


class Attendance(models.Model) :
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_owner')
    
    #Shows up in the admin list
    def __str__(self):
        local_check_in = timezone.localtime(check_in).strftime('%d-%m-%Y, %I:%M%p')
        local_check_out = str(check_out)

        if self.check_out:
            local_check_out = timezone.localtime(self.check_out).strftime('%d-%m-%Y, %I:%M%p')

        return local_check_in + ' - ' + local_check_out
