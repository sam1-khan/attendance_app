from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

# namespace:route_name
app_name='attendance'

urlpatterns = [
    path('', views.AttendanceListView.as_view(), name='all'),
    path('attendance/<int:pk>', views.AttendanceDetailView.as_view(), name='attendance_detail'),
    path('attendance/create', 
        views.AttendanceCreateView.as_view(success_url=reverse_lazy('attendance:all')), name='attendance_create'),
    path('attendance/<int:pk>/update', 
        views.AttendanceUpdateView.as_view(success_url=reverse_lazy('attendance:all')), name='attendance_update'),
]

# We use reverse_lazy in urls.py to delay looking up the view until all the paths are defined
