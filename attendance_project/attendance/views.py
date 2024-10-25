from attendance.models import Attendance

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
        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Attendance.objects.filter(title__contains=strval).select_related().distinct().order_by('-check_in')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval) 
            query.add(Q(text__icontains=strval), Q.OR)
            attendance_list = Attendance.objects.filter(query).select_related().distinct().order_by('-check_in')
        else :
            attendance_list = Attendance.objects.all().order_by('-check_in')

        # Augment the attendance_list
        for obj in attendance_list:
            obj.natural_updated = naturaltime(obj.check_in)

        ctx = {'attendance_list' : attendance_list, 'search': strval}
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



