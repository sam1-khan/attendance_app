from attendance.models import Attendance
from django.utils import timezone
from django.views import View, generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

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
        today = timezone.now().date()
        attendance_list = Attendance.objects.filter(owner=request.user, check_in=today) or []

        ctx = {'attendance_list' : attendance_list}
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
    fields = ['check_in']
    template_name = "attendance/form.html"


class AttendanceUpdateView(OwnerUpdateView):
    model = Attendance
    fields = ['check_out']
    template_name = "attendance/form.html"



