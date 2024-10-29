from attendance.models import Attendance
from django.utils import timezone
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

from django.db.models import Q

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
            owner=request.user,
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
    fields = ['is_checked_in']

#class AttendanceCreateView(LoginRequiredMixin, View):
#    template_name = "attendance/form.html"
#    success_url = reverse_lazy('attendance:all')
#    format = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
#
#    def get(self, request) : 
#        ctx = {'attendance_form' : attendance_form, 'format' : self.format }
#        return render(request, self.template_name, ctx)
#
#    def post(self, request) :
#        if not attendance_form.is_valid():
#            ctx = {'attendance_form' : attendance_form, 'format' : self.format }
#            return render(request, self.template_name, ctx)
#
#        attendance = attendance_form.save()
#        return redirect(self.success_url)

class AttendanceUpdateView(OwnerUpdateView):
    model = Attendance
    fields = ['is_checked_out']
    template_name = "attendance/form.html"



