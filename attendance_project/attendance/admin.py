from django.contrib import admin
from .models import Employee, Attendance


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_active_display')  # Show user, role, status, and is_active
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'role')  # Enable searching by username and role
    list_filter = ('role',)  # Add filters for status and role

    def is_active_display(self, obj):
        return obj.user.is_active  # Access the is_active field from the User model

    is_active_display.boolean = True  # This will render the field as a boolean (checkmark) in the admin
    is_active_display.short_description = 'Active'  # Name to display in the admin list


class AttendanceAdmin(admin.ModelAdmin):
    readonly_fields=['check_in', 'check_out']


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)

