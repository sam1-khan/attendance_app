from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Employee


class EmployeeCreationForm(UserCreationForm):

    class Meta:
        model = Employee
        fields = ("email", "role", "first_name", "last_name",)


class EmployeeChangeForm(UserChangeForm):

    class Meta:
        model = Employee
        fields = ("email", "role", "first_name", "last_name",)
