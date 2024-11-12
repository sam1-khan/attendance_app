from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Employee


class EmployeeCreationForm(UserCreationForm):

    class Meta:
        model = Employee
        fields = ("email", "role", "first_name", "last_name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class EmployeeChangeForm(UserChangeForm):

    class Meta:
        model = Employee
        fields = ("email", "role", "first_name", "last_name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
