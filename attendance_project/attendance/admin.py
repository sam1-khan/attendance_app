from django.contrib import admin

# Register your models here.

from .models import Attendance, Employee, Person

admin.site.register(Attendance)
admin.site.register(Employee)
admin.site.register(Person)

