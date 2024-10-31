from .models import Attendance
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
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

