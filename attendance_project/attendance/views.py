from django.views import View
from django.views.generic import ListView
from django.forms import ValidationError
from .models import Attendance
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = "attendance/list.html"

    def get(self, request) :
        start_of_today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)

        # Filter attendance records for the current user within today's date range
        attendance_list = Attendance.objects.filter(
            employee=request.user,
            check_in__range=(start_of_today, end_of_today)
        )
        ctx = {'attendance_list' : attendance_list }
        return render(request, self.template_name, ctx)


class SetCheckoutView(LoginRequiredMixin, View):
    def post(self, request, pk):
        attendance = get_object_or_404(Attendance, pk=pk, employee=request.user)
        if not attendance.is_checked_out:
            attendance.is_checked_out = True
        attendance.save()

        return JsonResponse({'is_checked_out': attendance.is_checked_out})

class SetCheckinView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            attendance = Attendance(employee=request.user)
            attendance.full_clean()
            attendance.save()
            return JsonResponse({'check_in': attendance.check_in,})
        except ValidationError as e:
            return JsonResponse({'error': str(e),}, status=400)