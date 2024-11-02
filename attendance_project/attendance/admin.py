from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.forms import ValidationError
from .forms import EmployeeCreationForm, EmployeeChangeForm
from .models import Employee, Attendance


class EmployeeAdmin(UserAdmin):
    add_form = EmployeeCreationForm
    form = EmployeeChangeForm
    model = Employee
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active", "role",)
    search_fields = ('email', 'first_name', 'last_name', 'role') 
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name", "role")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "role", "first_name", "last_name",
                "is_staff", "is_active", "groups", "user_permissions"
            )}
        ),
    )


class AttendanceAdmin(admin.ModelAdmin):
    search_fields = ('check_in', 'check_out', 'employee')  # Enable searching by 
    list_filter = ('is_checked_out',) 
    readonly_fields=('check_in', 'check_out')
    list_display = ('employee', 'is_checked_out', 'check_in', 'check_out')
    def save_model(self, request, obj, form, change):
        if change:  # If the object is being changed
            original = Attendance.objects.get(pk=obj.pk)
            if original.is_checked_out != obj.is_checked_out and original.is_checked_out:
                # If the user is trying to change is_checked_out after it was already set
                raise ValidationError(_("You cannot change 'is checked out' once it's been set."))
        super().save_model(request, obj, form, change)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)

