from django.contrib import admin
from .models import Employee, Attendance


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_active_display')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'role') 
    list_filter = ('role',)  # Add filters for and role

    def is_active_display(self, obj):
        return obj.user.is_active  # Access the is_active field from the User model

    is_active_display.boolean = True  # This will render the field as a boolean (checkmark) in the admin
    is_active_display.short_description = 'Active'  # Name to display in the admin list


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
                raise ValidationError("You cannot change is_checked_out once it's been set.")
        super().save_model(request, obj, form, change)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)

