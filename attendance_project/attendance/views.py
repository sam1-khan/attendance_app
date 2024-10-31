from .models import Attendance
from django.utils import timezone
from django.shortcuts import render, redirect
from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView

class AttendanceListView(OwnerListView):
    model = Attendance
    template_name = "attendance/list.html"

    def get(self, request) :
        if not request.user.is_authenticated:
            return redirect('login')
        # Define the start and end of today
        start_of_today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)

        # Filter attendance records for the current user within today's date range
        attendance_list = Attendance.objects.filter(
            employee__user=request.user,
            check_in__range=(start_of_today, end_of_today)
        )
        ctx = {'attendance_list' : attendance_list }
        return render(request, self.template_name, ctx)


class AttendanceDetailView(OwnerDetailView):
    model = Attendance
    template_name = "attendance/detail.html"
    def get(self, request, pk) :
        x = get_object_or_404(Attendance, id=pk)
        context = { 'attendance' : x }
        return render(request, self.template_name, context)


class AttendanceCreateView(OwnerCreateView):
    model = Attendance
    template_name = "attendance/form.html"


class AttendanceUpdateView(OwnerUpdateView):
    model = Attendance
    template_name = "attendance/form.html"


def send_reminder(self):
    current_time = timezone.now()
    reminder_threshold = current_time - timedelta(minutes=0)
    employees_to_remind = Attendance.objects.filter(
        is_checked_out=False,
        check_in__lt=reminder_threshold  # Ensure the check_in is before the reminder threshold
    )

    for attendance in employees_to_remind:
        subject = "Reminder: You have not checked out!"
        message = (
            f"Hello {self.employee.user.get_full_name() if self.employee.user.first_name else self.employee.user.get_username()},\n\n"
            "This is a reminder that you have not marked your checkout for today. "
            "Please make sure to check out to complete your attendance record.\n\n"
            "Thank you!"
        )

        # Send email
        self.employee.user.email_user(
            subject,
            message
        )

